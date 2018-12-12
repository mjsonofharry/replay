from test_common import replay, player, frame, SAMPLE_REPLAY_DATA, SAMPLE_PLAYER_DATA


class TestBenchmarks:
    
    def test_get_player_data(self, benchmark):
        result = benchmark(replay.get_player_data, SAMPLE_REPLAY_DATA)
        assert len(result) == 1
        assert result[0] == SAMPLE_PLAYER_DATA

    def test_get_frame_data(self, benchmark):
        result = benchmark(player.get_frame_data, SAMPLE_PLAYER_DATA)
        assert len(result) == 717
        assert result[0] == '1Z'
        assert result[716] == '2385y  0'

    def test_get_action_table(self, benchmark):
        frame_data = player.get_frame_data(SAMPLE_PLAYER_DATA)
        result = benchmark(frame.get_action_map, frame_data)
        assert isinstance(result, dict)
        assert len(result.keys()) == 717
        assert result[1] == [frame.InputEvent.ANGLES_ENABLED]
        assert result[2385] == [0]

    def test_get_state_table(self, benchmark):
        frame_data = player.get_frame_data(SAMPLE_PLAYER_DATA)
        result = benchmark(frame.get_state_table, frame_data)
        assert isinstance(result, list)
        assert len(result) == 717
        assert isinstance(result[0], dict)
        assert result[0][frame.ActionType.ANGLES_ENABLED] == True
        assert result[716][frame.ActionType.FRAME] == 2385
        assert result[716][frame.ActionType.ANGLE] == 0
