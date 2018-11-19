from test_common import ReplayBuffer, PlayerBuffer, FrameData, InputEvent, ActionType, SAMPLE_REPLAY_DATA, SAMPLE_PLAYER_DATA


class TestBenchmarks:
    
    def test_get_player_data(self, benchmark):
        result = benchmark(ReplayBuffer.get_player_data, SAMPLE_REPLAY_DATA)
        assert len(result) == 1
        assert result[0] == SAMPLE_PLAYER_DATA

    def test_get_frame_data(self, benchmark):
        result = benchmark(PlayerBuffer.get_frame_data, SAMPLE_PLAYER_DATA)
        assert len(result) == 717
        assert result[0] == '1Z'
        assert result[716] == '2385y  0'

    def test_get_action_table(self, benchmark):
        frame_data = PlayerBuffer.get_frame_data(SAMPLE_PLAYER_DATA)
        result = benchmark(FrameData.get_action_map, frame_data)
        assert isinstance(result, dict)
        assert len(result.keys()) == 717
        assert result[1] == [InputEvent.ANGLES_ENABLED]
        assert result[2385] == [0]

    def test_get_state_table(self, benchmark):
        frame_data = PlayerBuffer.get_frame_data(SAMPLE_PLAYER_DATA)
        result = benchmark(FrameData.get_state_table, frame_data)
        assert isinstance(result, list)
        assert len(result) == 717
        assert isinstance(result[0], dict)
        assert result[0][ActionType.ANGLES_ENABLED] == True
        assert result[716][ActionType.FRAME] == 2385
        assert result[716][ActionType.ANGLE] == 0
