import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    maxWidth: 752,
  },
  demo: {
    backgroundColor: theme.palette.background.paper,
  },
  title: {
    margin: theme.spacing(4, 0, 2),
  },
}));

function generate(element) {
  return [0, 1, 2].map((value) =>
    React.cloneElement(element, {
      key: value,
    }),
  );
}

export default function LoggerMessages() {
  const classes = useStyles();
  const [dense, setDense] = React.useState(false);
  const [secondary, setSecondary] = React.useState(false);

  return (
    <div className={classes.root}>
  
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Typography variant="h6" className={classes.title}>
            Log Messages
          </Typography>
          <div className={classes.demo}>
              <table>
                  <tr>
                      <th>Date</th>
                      <th>Level</th>
                      <th>Message</th>
                    </tr>
                    <tr>
                        <td>heute</td>
                        <td>critical</td>
                        <td>we need coffee</td>
                    </tr>
                    <tr>
                        <td>Morgen</td>
                        <td>Info</td>
                        <td>gratis Glühwein</td>
                    </tr>
              </table>
      
          </div>
      </Grid>
       
      </Grid>
    </div>
  );
}
