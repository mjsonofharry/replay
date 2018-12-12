from test_common import replay, player, frame, SAMPLE_PLAYER_DATA
import pytest


@pytest.fixture
def action_table():
    return frame.get_action_map(player.get_frame_data(SAMPLE_PLAYER_DATA))


@pytest.fixture
def raw_action_table():
    return frame.get_action_map(player.get_frame_data(SAMPLE_PLAYER_DATA), raw=True)


class Testframe:
    
    def test_convert_token_to_action(self):
        assert frame._convert_token_to_action('Z') == frame.InputEvent.ANGLES_ENABLED
        assert frame._convert_token_to_action('y327') == 327
        assert frame._convert_token_to_action('R') == frame.InputEvent.RIGHT_PRESS

    def test_convert_multiple_tokens_to_actions(self):
        assert frame._convert_multiple_tokens_to_actions(['Z']) == [frame.InputEvent.ANGLES_ENABLED]
        assert frame._convert_multiple_tokens_to_actions(['z', 'y327', 'R']) == [frame.InputEvent.ANGLES_DISABLED, 327, frame.InputEvent.RIGHT_PRESS]
        assert frame._convert_multiple_tokens_to_actions(['C']) == [frame.InputEvent.STRONG_PRESS]
        assert frame._convert_multiple_tokens_to_actions(['Z', 'y  0', 'r', 'c']) == [frame.InputEvent.ANGLES_ENABLED, 0, frame.InputEvent.RIGHT_RELEASE, frame.InputEvent.STRONG_RELEASE]
        assert frame._convert_multiple_tokens_to_actions(['z', 'y143', 'L', 'U']) == [frame.InputEvent.ANGLES_DISABLED, 143, frame.InputEvent.LEFT_PRESS, frame.InputEvent.UP_PRESS]
        assert frame._convert_multiple_tokens_to_actions(['y  0']) == [0]
        assert frame._convert_multiple_tokens_to_actions(['Z', 'y180', 'd']) == [frame.InputEvent.ANGLES_ENABLED, 180, frame.InputEvent.DOWN_RELEASE]
        assert frame._convert_multiple_tokens_to_actions(['z', 'D']) == [frame.InputEvent.ANGLES_DISABLED, frame.InputEvent.DOWN_PRESS]

    def test_split_frames_into_tokens(self):
        split_frames = frame._split_frames_into_tokens(player.get_frame_data(SAMPLE_PLAYER_DATA))
        assert split_frames[0] == ['1', 'Z']
        assert split_frames[1] == ['101', 'z', 'y327', 'R']
        assert split_frames[-2] == ['2384', 'Z', 'y180', 'd']
        assert split_frames[-1] == ['2385', 'y  0']

    def test_get_action_table(self, action_table):
        assert len(action_table.keys()) == 717
        assert action_table[1] == [frame.InputEvent.ANGLES_ENABLED]
        assert action_table[101] == [frame.InputEvent.ANGLES_DISABLED, 327, frame.InputEvent.RIGHT_PRESS]
        assert action_table[148] == [frame.InputEvent.STRONG_PRESS]
        assert action_table[154] == [frame.InputEvent.ANGLES_ENABLED, 0, frame.InputEvent.RIGHT_RELEASE, frame.InputEvent.STRONG_RELEASE]
        assert action_table[1293] == [frame.InputEvent.ANGLES_DISABLED, 143, frame.InputEvent.LEFT_PRESS, frame.InputEvent.UP_PRESS]
        assert action_table[2366] == [frame.InputEvent.ANGLES_DISABLED, frame.InputEvent.DOWN_PRESS]
        assert action_table[2384] == [frame.InputEvent.ANGLES_ENABLED, 180, frame.InputEvent.DOWN_RELEASE]
        assert action_table[2385] == [0]

    def test_get_action_table_raw(self, raw_action_table):
        assert len(raw_action_table.keys()) == 717
        assert raw_action_table[1] == ['Z']
        assert raw_action_table[101] == ['z', 'y327', 'R']
        assert raw_action_table[148] == ['C']
        assert raw_action_table[154] == ['Z', 'y  0', 'r', 'c']
        assert raw_action_table[1293] == ['z', 'y143', 'L', 'U']
        assert raw_action_table[2366] == ['z', 'D']
        assert raw_action_table[2384] == ['Z', 'y180', 'd']
        assert raw_action_table[2385] == ['y  0']

    def test_get_state_table(self):
        state_p1 = frame.get_state_table(player.get_frame_data(SAMPLE_PLAYER_DATA))
        state = {
            frame.ActionType.FRAME: 1,
            frame.ActionType.JUMP: False,
            frame.ActionType.ATTACK: False,
            frame.ActionType.SPECIAL: False,
            frame.ActionType.STRONG: False,
            frame.ActionType.STRONG_LEFT: False,
            frame.ActionType.STRONG_RIGHT: False,
            frame.ActionType.STRONG_UP: False,
            frame.ActionType.STRONG_DOWN: False,
            frame.ActionType.DODGE: False,
            frame.ActionType.UP: False,
            frame.ActionType.DOWN: False,
            frame.ActionType.LEFT: False,
            frame.ActionType.RIGHT: False,
            frame.ActionType.TAP_UP: False,
            frame.ActionType.TAP_DOWN: False,
            frame.ActionType.TAP_LEFT: False,
            frame.ActionType.TAP_RIGHT: False,
            frame.ActionType.ANGLES_ENABLED: True,
            frame.ActionType.ANGLE: None
        }
        assert state_p1[0] == state
        state[frame.ActionType.FRAME] = 101
        state[frame.ActionType.ANGLES_ENABLED] = False
        state[frame.ActionType.RIGHT] = True
        state[frame.ActionType.ANGLE] = 327
        assert state_p1[1] == state
        state[frame.ActionType.FRAME] = 102
        state[frame.ActionType.ANGLE] = 333
        assert state_p1[2] == state
        state[frame.ActionType.FRAME] = 103
        state[frame.ActionType.ANGLE] = 338
        state[frame.ActionType.TAP_RIGHT] = True
        assert state_p1[3] == state
        state[frame.ActionType.FRAME] = 104
        state[frame.ActionType.ANGLE] = 341
        assert state_p1[4] == state
        state[frame.ActionType.FRAME] = 105
        state[frame.ActionType.ANGLE] = 344
        state[frame.ActionType.TAP_RIGHT] = False
        assert state_p1[5] == state
        state[frame.ActionType.FRAME] = 106
        state[frame.ActionType.ANGLE] = 345
        state[frame.ActionType.TAP_RIGHT] = False
        assert state_p1[6] == state


    def test_snap_frame(self, action_table):
        assert frame.snap_frame(action_table, 1) == 1
        assert frame.snap_frame(action_table, 100) == 1
        assert frame.snap_frame(action_table, 101) == 101
        assert frame.snap_frame(action_table, 112) == 112
        assert frame.snap_frame(action_table, 114) == 112
        assert frame.snap_frame(action_table, 115) == 115
        assert frame.snap_frame(action_table, 118) == 115
        assert frame.snap_frame(action_table, 2385) == 2385
        assert frame.snap_frame(action_table, 9999) == 2385

    def test_snap_frame_error(self, action_table):
        with pytest.raises(ValueError): frame.snap_frame(action_table, -1)

    def test_snap_frame_transitive(self, raw_action_table):
        assert raw_action_table[frame.snap_frame(raw_action_table, 100)] == ['Z']
        assert raw_action_table[frame.snap_frame(raw_action_table, 101)] == ['z', 'y327', 'R']

    def test_snap_multiple_frames(self, action_table):
        snapped = frame.snap_multiple_frames(action_table, [1, 100, 101, 112, 114, 115, 118, 2385, 9999])
        assert snapped == [1, 1, 101, 112, 112, 115, 115, 2385, 2385]

    def test_snap_angle(self):
        assert frame.snap_angle(0) == 0
        assert frame.snap_angle(23) == 45
        assert frame.snap_angle(45) == 45
        assert frame.snap_angle(67) == 45
        assert frame.snap_angle(68) == 90
        assert frame.snap_angle(180) == 180
        assert frame.snap_angle(360) == 0

    def test_get_closest_frame(self, raw_action_table):
        assert frame.get_closest_action(raw_action_table, 100) == ['Z']
        assert frame.get_closest_action(raw_action_table, 101) == ['z', 'y327', 'R']

    def test_snap_angle_error(self):
        with pytest.raises(ValueError): frame.snap_angle(-1)
        with pytest.raises(ValueError): frame.snap_angle(361)
