import * as React from 'react';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Chip from '@mui/material/Chip';

export default function GoalGrid({goals}) {
  const textHeight = "132px";
  const colors = ["#ef51a1", "#e4b435", "#268bd2", "#88b50a"];

  return (
    <Grid container spacing={2} sx={{my: 2}}>
      {goals.map(
        (goal, idx) => (
          <Grid item key={"goal-card-"+String(idx)} xs={4}>

          <Paper elevation={4} sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: textHeight,
            position: "relative",
            border: 6,
            borderColor: "primary.contrastText",
            backgroundColor: colors[goal[1]],
          }}>
              <Typography 
                variant="h3"
                component="p"
                sx={{
                  color: "primary.contrastText",
                }}
              > {goal[0]} 
              </Typography>
              {
                (goal[2] != 0) &&
                <Chip label={goal[2]} size="small" sx={{
                  bgcolor: "#586e75", 
                  color: "primary.contrastText",
                  border: 3,
                  position: "absolute", 
                  bottom: 6, 
                  }}
                />
              }
          </Paper>
          </Grid>
        )
      )}
    </Grid>
  );
}

