import time

import numpy as np
import urx
import logging
import asyncio
from aiolimiter import AsyncLimiter


class Robot:
    def __init__(self, config):
        self.config = config
        self.robot = urx.Robot(self.config.get('ur.host'))
        self.initial_pos = np.copy(np.array(self.robot.getl()))
        self.num_axes = 6
        self.target_pos = np.copy(self.initial_pos)
        self.scale = np.array(list(map(lambda d: d.get("scaling_factor"), config.get('axis'))))
        self.rate_limit = AsyncLimiter(1, 3)
        self.logger = logging.getLogger(__name__)

    # TODO: Make this configurable
    def setup(self):
        tcp = (0, 0, 0.1, 0, 0, 0)
        self.robot.set_tcp(tcp)

        weight = 2  # In kg
        cog = (0, 0.1, 0)  # Vector
        self.robot.set_payload(weight=weight, cog=cog)

        # Leave some time for the robot to process the setup
        self.logger.info("Setting up robot, this might take a few seconds")
        time.sleep(2)

    def _scale_pos(self, pos, initial_pos):
        return np.around(np.multiply(
            np.array(pos) - initial_pos,
            self.scale
        ), decimals=0)

    def _unscale_pos(self, pos, initial_pos):
        return (pos / self.scale) + initial_pos

    def get_pos(self):
        # Meters * scale, e.g. scale = 1000 => mm
        return self._scale_pos(self.robot.getl(), self.initial_pos).astype(int)

    def update_target_pos(self, axis, new_value):
        self.target_pos[axis] = new_value

    def _move_to_target_pos(self):
        pose = self._unscale_pos(self.target_pos, self.initial_pos)
        self.robot.movel(pose, 0.1, 0.1, wait=True)

    async def move_to_target_pos(self, direct=False):
        if direct:
            self._move_to_target_pos()
        else:
            async with self.rate_limit:
                await asyncio.sleep(2)
                self._move_to_target_pos()

    def stop(self, axis=None):
        if axis is None:
            self.robot.stop()
        else:
            current_pos = self.get_pos()
            self.update_target_pos(axis, current_pos[axis])
            self.move_to_target_pos()

    def zero_motor_pos(self, axis):
        self.initial_pos[axis] = self.robot.getl()[axis]

    def set_motor_pos(self, axis, value):
        self.initial_pos[axis] += value

    def set_freedrive(self, val):
        self.robot.set_freedrive(val)



