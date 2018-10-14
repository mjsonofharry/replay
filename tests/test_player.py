from test_common import PlayerData, Character, SAMPLE_PLAYER_DATA

class TestPlayerData:
    def test_is_human(self):
        assert PlayerData.is_human(SAMPLE_PLAYER_DATA) == True
    
    def test_get_name(self):
        assert PlayerData.get_name(SAMPLE_PLAYER_DATA) == 'Player 1'

    def test_get_tag(self):
        assert PlayerData.get_tag(SAMPLE_PLAYER_DATA) == ''

    def test_get_character(self):
        assert PlayerData.get_character(SAMPLE_PLAYER_DATA) == Character.ORI

    def test_get_frame_data(self):
        actions_p1 = PlayerData.get_frame_data(SAMPLE_PLAYER_DATA)
        assert len(actions_p1) == 717
        assert actions_p1[0] == '1Z'
        assert actions_p1[1] == '101zy327R'
        assert actions_p1[24] == '148C'
        assert actions_p1[29] == '154Zy  0rc'
        assert actions_p1[394] == '1293zy143LU'
        assert actions_p1[714] == '2366zD'
        assert actions_p1[715] == '2384Zy180d'
        assert actions_p1[716] == '2385y  0'

    def test_get_frame_data_performance(self, benchmark):
        result = benchmark(PlayerData.get_frame_data, SAMPLE_PLAYER_DATA)
        assert len(result) == 717
        assert result[0] == '1Z'
        assert result[716] == '2385y  0'
