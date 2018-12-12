import pytest
from test_common import player, SAMPLE_PLAYER_DATA, ALT_SAMPLE_PLAYER_DATA


class TestPlayerData:
    
    def test_is_human(self):
        assert player.is_human(SAMPLE_PLAYER_DATA) == True
    
    def test_get_name(self):
        assert player.get_name(SAMPLE_PLAYER_DATA) == 'Player 1'

    def test_get_tag(self):
        assert player.get_tag(SAMPLE_PLAYER_DATA) == ''

    def test_get_character(self):
        assert player.get_character(SAMPLE_PLAYER_DATA) == player.Character.ORI

    def test_get_character_alt(self):
        assert player.get_character(ALT_SAMPLE_PLAYER_DATA[1]) == player.Character.ABSA

    def test_get_frame_data(self):
        actions_p1 = player.get_frame_data(SAMPLE_PLAYER_DATA)
        assert len(actions_p1) == 717
        assert actions_p1[0] == '1Z'
        assert actions_p1[1] == '101zy327R'
        assert actions_p1[24] == '148C'
        assert actions_p1[29] == '154Zy  0rc'
        assert actions_p1[394] == '1293zy143LU'
        assert actions_p1[714] == '2366zD'
        assert actions_p1[715] == '2384Zy180d'
        assert actions_p1[716] == '2385y  0'


class TestPlayer:

    @pytest.fixture
    def p(self):
        return player.Player(SAMPLE_PLAYER_DATA)

    def test_is_human(self, p):
        assert p.is_human == player.is_human(SAMPLE_PLAYER_DATA)
    
    def test_name(self, p):
        assert p.name == player.get_name(SAMPLE_PLAYER_DATA)

    def test_tag(self, p):
        assert p.tag == player.get_tag(SAMPLE_PLAYER_DATA)

    def test_character(self, p):
        assert p.character == player.get_character(SAMPLE_PLAYER_DATA)
