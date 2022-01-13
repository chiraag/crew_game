import * as React from 'react';
import Stack from '@mui/material/Stack';
import MenuItem from '@mui/material/MenuItem';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import CasinoIcon from '@mui/icons-material/Casino';

function range(start, end) {
  return Array.from({length:(end-start+1)}, (_,i) => start + i)
}

function IntSelect(props) {
  const {title, start, end, value, callback} = props;
  const getKey = (option) => (title.toLowerCase()+"-"+String(option));

  return (
    <TextField
      label={title}
      name={title.toLowerCase()}
      value={value}
      onChange={callback}
      select
      fullWidth
      variant="standard"
    >
      {range(start, end).map(
        (option) => (<MenuItem key={getKey(option)} value={option}> {option} </MenuItem>)
      )}
    </TextField>
  );
}

export default function SettingsPane({settings, settingsCallback, goalsCallback}) {
  const updateSettings = (event) => {
    if (event.target.name == "goals") {
      settingsCallback({...settings, goals: event.target.value});
    } else if (event.target.name == "ordered") {
      settingsCallback({...settings, ordered: event.target.value});
    } else {
      settingsCallback({...settings, players: event.target.value});
    }
  };

  const updateGoals = (event) => {
    // Iterative rejection sampling. Can hash for speed but not trying
    var nxtGoals = [];
    const maxSuits = {3: 3, 4:4, 5:4}[settings.players];
    const randInt = (min, max) => (min+Math.floor(Math.random()*(max-min+1)));

    for(var idx=0; idx<settings.goals; idx++) {
      while(true) {
        let cardVal = randInt(1, 9);
        let cardSuit = randInt(0, maxSuits-1);

        let seen = nxtGoals.some((goal) => (goal[0] == cardVal && goal[1] == cardSuit));
        if (!seen) {
          nxtGoals.push([cardVal, cardSuit, (idx < settings.ordered) ? (idx+1) : 0]);
          break;
        }
      };
    }

    goalsCallback(nxtGoals);
  }

  return (
    <Stack direction="row" spacing={2}>
      <IntSelect title="Goals" start={1} end={9} value={settings.goals} callback={updateSettings}/>
      <IntSelect title="Ordered" start={0} end={settings.goals} value={settings.ordered} callback={updateSettings}/>
      <IntSelect title="Players" start={3} end={5} value={settings.players} callback={updateSettings}/>
      <Button variant="contained" endIcon={<CasinoIcon />} onClick={updateGoals} fullWidth sx={{maxWidth: "96px"}}> Pick </Button>
    </Stack>
  );
}

