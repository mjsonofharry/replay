from test_common import ReplayData, PlayerData, Action, FrameData, SAMPLE_REPLAY_DATA

class TestBenchmarks:
    def test_get_lookup_table(self, benchmark):
        result = benchmark(FrameData.get_lookup_table, PlayerData.get_frame_data(ReplayData.get_player_data(SAMPLE_REPLAY_DATA)[0]))
        assert isinstance(result, dict)
        assert len(result.keys()) == 717
        assert result[1] == [Action.ANGLES_ENABLED]
        assert result[2385] == [0]

    def test_get_state_table(self, benchmark):
        result = benchmark(FrameData.get_state_table, PlayerData.get_frame_data(ReplayData.get_player_data(SAMPLE_REPLAY_DATA)[0]))
        assert isinstance(result, dict)
        assert len(result.keys()) == 717
        assert isinstance(result[1], list)
        assert result[1][0] == False
