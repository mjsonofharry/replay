# Description
A functional API that uses regular expressions to parse replay (.roa) files from Rivals of Aether.

# Explanations

* Replay data: A string buffer containing the entire contents of a replay (.roa) file.
* Player data: A string buffer extracted from replay data, consisting of a singular player's information.
* Frame data: A string buffer extracted from player data, enumerating that player's inputs by frame number.
* Lookup table: A dictionary representation of frame data, in which the keys are frame numbers and the values are the player's inputs.
* State table: A more complicated variation of the lookup table, in which the keys are frame numbers and the values are Boolean flags representing the current state for each type of input.

# Example

```
from replay import FrameData, PlayerData, ReplayData

with open('test.roa') as f:
    replay = f.read()
    game_version = ReplayData.get_version(replay)
    match_duration = ReplayData.get_duration(ReplayData.get_frame_data_all_players(replay))
    players = ReplayData.get_player_data(replay)
    state_table = FrameData.get_state_table(PlayerData.get_frame_data(players[0]))
```

# Credits

[lazerzes](https://github.com/ContentsMayBeHot/RivalsofAetherReplayParser)

[MatthewMJV](https://www.reddit.com/r/RivalsOfAether/comments/5sxvw2/what_i_have_learned_from_looking_through_replays/)
