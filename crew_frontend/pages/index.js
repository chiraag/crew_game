import * as React from 'react';
import { useState } from 'react';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

import Copyright from '../src/Copyright';
import SettingsPane from '../src/SettingsPane';
import GoalGrid from '../src/GoalGrid';

export default function Index() {
  const [settings, setSettings] = useState({
    goals: 4,
    ordered: 0,
    players: 4,
  });
  const [goals, setGoals] = useState([]);

  return (
    <Container maxWidth="md" sx={{
      display: 'flex',
      flexDirection: 'column',
      minHeight: '100vh'
    }}>
      <Box sx={{mt: 2, flex: '1 1 auto'}}>
        <Typography variant="h4" component="h1" gutterBottom>
          Crew Goal Picker
        </Typography>

        <Typography variant="body1" paragraph> Pick settings to randomize goals </Typography>

        <SettingsPane settings={settings} settingsCallback={setSettings} goalsCallback={setGoals}/>
        <GoalGrid goals={goals} />
      </Box>
      <Box sx={{mb:2}}>
        <Copyright />
      </Box>
    </Container>
  );
}
