from test_common import ReplayData, PlayerData, FrameData, Action, SAMPLE_REPLAY_DATA, SAMPLE_PLAYER_DATA

class TestBenchmarks:
    def test_get_player_data(self, benchmark):
        result = benchmark(ReplayData.get_player_data, SAMPLE_REPLAY_DATA)
        assert len(result) == 1
        assert result[0] == SAMPLE_PLAYER_DATA

    def test_get_frame_data(self, benchmark):
        result = benchmark(PlayerData.get_frame_data, SAMPLE_PLAYER_DATA)
        assert len(result) == 717
        assert result[0] == '1Z'
        assert result[716] == '2385y  0'

    def test_get_lookup_table(self, benchmark):
        frame_data = PlayerData.get_frame_data(SAMPLE_PLAYER_DATA)
        result = benchmark(FrameData.get_lookup_table, frame_data)
        assert isinstance(result, dict)
        assert len(result.keys()) == 717
        assert result[1] == [Action.ANGLES_ENABLED]
        assert result[2385] == [0]

    def test_get_state_table(self, benchmark):
        frame_data = PlayerData.get_frame_data(SAMPLE_PLAYER_DATA)
        result = benchmark(FrameData.get_state_table, frame_data)
        assert isinstance(result, dict)
        assert len(result.keys()) == 717
        assert isinstance(result[1], list)
        assert result[1][0] == False
