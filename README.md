# Description
A functional API that uses regular expressions to parse replay (.roa) files from Rivals of Aether.

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
