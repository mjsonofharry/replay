from test_common import ReplayBuffer, PlayerBuffer, FrameData, InputEvent, ActionType, SAMPLE_PLAYER_DATA
import pytest


@pytest.fixture
def action_table():
    return FrameData.get_action_map(PlayerBuffer.get_frame_data(SAMPLE_PLAYER_DATA))


@pytest.fixture
def raw_action_table():
    return FrameData.get_action_map(PlayerBuffer.get_frame_data(SAMPLE_PLAYER_DATA), raw=True)


class TestFrameData:
    
    def test_convert_token_to_action(self):
        assert FrameData._convert_token_to_action('Z') == InputEvent.ANGLES_ENABLED
        assert FrameData._convert_token_to_action('y327') == 327
        assert FrameData._convert_token_to_action('R') == InputEvent.RIGHT_PRESS

    def test_convert_multiple_tokens_to_actions(self):
        assert FrameData._convert_multiple_tokens_to_actions(['Z']) == [InputEvent.ANGLES_ENABLED]
        assert FrameData._convert_multiple_tokens_to_actions(['z', 'y327', 'R']) == [InputEvent.ANGLES_DISABLED, 327, InputEvent.RIGHT_PRESS]
        assert FrameData._convert_multiple_tokens_to_actions(['C']) == [InputEvent.STRONG_PRESS]
        assert FrameData._convert_multiple_tokens_to_actions(['Z', 'y  0', 'r', 'c']) == [InputEvent.ANGLES_ENABLED, 0, InputEvent.RIGHT_RELEASE, InputEvent.STRONG_RELEASE]
        assert FrameData._convert_multiple_tokens_to_actions(['z', 'y143', 'L', 'U']) == [InputEvent.ANGLES_DISABLED, 143, InputEvent.LEFT_PRESS, InputEvent.UP_PRESS]
        assert FrameData._convert_multiple_tokens_to_actions(['y  0']) == [0]
        assert FrameData._convert_multiple_tokens_to_actions(['Z', 'y180', 'd']) == [InputEvent.ANGLES_ENABLED, 180, InputEvent.DOWN_RELEASE]
        assert FrameData._convert_multiple_tokens_to_actions(['z', 'D']) == [InputEvent.ANGLES_DISABLED, InputEvent.DOWN_PRESS]

    def test_split_frames_into_tokens(self):
        split_frames = FrameData._split_frames_into_tokens(PlayerBuffer.get_frame_data(SAMPLE_PLAYER_DATA))
        assert split_frames[0] == ['1', 'Z']
        assert split_frames[1] == ['101', 'z', 'y327', 'R']
        assert split_frames[-2] == ['2384', 'Z', 'y180', 'd']
        assert split_frames[-1] == ['2385', 'y  0']

    def test_get_action_table(self, action_table):
        assert len(action_table.keys()) == 717
        assert action_table[1] == [InputEvent.ANGLES_ENABLED]
        assert action_table[101] == [InputEvent.ANGLES_DISABLED, 327, InputEvent.RIGHT_PRESS]
        assert action_table[148] == [InputEvent.STRONG_PRESS]
        assert action_table[154] == [InputEvent.ANGLES_ENABLED, 0, InputEvent.RIGHT_RELEASE, InputEvent.STRONG_RELEASE]
        assert action_table[1293] == [InputEvent.ANGLES_DISABLED, 143, InputEvent.LEFT_PRESS, InputEvent.UP_PRESS]
        assert action_table[2366] == [InputEvent.ANGLES_DISABLED, InputEvent.DOWN_PRESS]
        assert action_table[2384] == [InputEvent.ANGLES_ENABLED, 180, InputEvent.DOWN_RELEASE]
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
        state_p1 = FrameData.get_state_table(PlayerBuffer.get_frame_data(SAMPLE_PLAYER_DATA))
        state = {
            ActionType.FRAME: 1,
            ActionType.JUMP: False,
            ActionType.ATTACK: False,
            ActionType.SPECIAL: False,
            ActionType.STRONG: False,
            ActionType.STRONG_LEFT: False,
            ActionType.STRONG_RIGHT: False,
            ActionType.STRONG_UP: False,
            ActionType.STRONG_DOWN: False,
            ActionType.DODGE: False,
            ActionType.UP: False,
            ActionType.DOWN: False,
            ActionType.LEFT: False,
            ActionType.RIGHT: False,
            ActionType.TAP_UP: False,
            ActionType.TAP_DOWN: False,
            ActionType.TAP_LEFT: False,
            ActionType.TAP_RIGHT: False,
            ActionType.ANGLES_ENABLED: True,
            ActionType.ANGLE: None
        }
        assert state_p1[0] == state
        state[ActionType.FRAME] = 101
        state[ActionType.ANGLES_ENABLED] = False
        state[ActionType.RIGHT] = True
        state[ActionType.ANGLE] = 327
        assert state_p1[1] == state
        state[ActionType.FRAME] = 102
        state[ActionType.ANGLE] = 333
        assert state_p1[2] == state
        state[ActionType.FRAME] = 103
        state[ActionType.ANGLE] = 338
        state[ActionType.TAP_RIGHT] = True
        assert state_p1[3] == state
        state[ActionType.FRAME] = 104
        state[ActionType.ANGLE] = 341
        assert state_p1[4] == state
        state[ActionType.FRAME] = 105
        state[ActionType.ANGLE] = 344
        state[ActionType.TAP_RIGHT] = False
        assert state_p1[5] == state
        state[ActionType.FRAME] = 106
        state[ActionType.ANGLE] = 345
        state[ActionType.TAP_RIGHT] = False
        assert state_p1[6] == state


    def test_snap_frame(self, action_table):
        assert FrameData.snap_frame(action_table, 1) == 1
        assert FrameData.snap_frame(action_table, 100) == 1
        assert FrameData.snap_frame(action_table, 101) == 101
        assert FrameData.snap_frame(action_table, 112) == 112
        assert FrameData.snap_frame(action_table, 114) == 112
        assert FrameData.snap_frame(action_table, 115) == 115
        assert FrameData.snap_frame(action_table, 118) == 115
        assert FrameData.snap_frame(action_table, 2385) == 2385
        assert FrameData.snap_frame(action_table, 9999) == 2385

    def test_snap_frame_error(self, action_table):
        with pytest.raises(ValueError): FrameData.snap_frame(action_table, -1)

    def test_snap_frame_transitive(self, raw_action_table):
        assert raw_action_table[FrameData.snap_frame(raw_action_table, 100)] == ['Z']
        assert raw_action_table[FrameData.snap_frame(raw_action_table, 101)] == ['z', 'y327', 'R']

    def test_snap_multiple_frames(self, action_table):
        snapped = FrameData.snap_multiple_frames(action_table, [1, 100, 101, 112, 114, 115, 118, 2385, 9999])
        assert snapped == [1, 1, 101, 112, 112, 115, 115, 2385, 2385]

    def test_snap_angle(self):
        assert FrameData.snap_angle(0) == 0
        assert FrameData.snap_angle(23) == 45
        assert FrameData.snap_angle(45) == 45
        assert FrameData.snap_angle(67) == 45
        assert FrameData.snap_angle(68) == 90
        assert FrameData.snap_angle(180) == 180
        assert FrameData.snap_angle(360) == 0

    def test_get_closest_frame(self, raw_action_table):
        assert FrameData.get_closest_action(raw_action_table, 100) == ['Z']
        assert FrameData.get_closest_action(raw_action_table, 101) == ['z', 'y327', 'R']

    def test_snap_angle_error(self):
        with pytest.raises(ValueError): FrameData.snap_angle(-1)
        with pytest.raises(ValueError): FrameData.snap_angle(361)
