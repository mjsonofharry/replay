import datetime as dt
import pytest
from test_common import replay, SAMPLE_REPLAY_DATA, SAMPLE_PLAYER_DATA, ALT_SAMPLE_REPLAY_DATA, ALT_SAMPLE_PLAYER_DATA


class TestReplayData:
    
    def test_is_starred_true(self):
        assert replay.is_starred(ALT_SAMPLE_REPLAY_DATA) == True

    def test_is_starred_false(self):
        assert replay.is_starred(SAMPLE_REPLAY_DATA) == False

    def test_get_version(self):
        assert replay.get_version(SAMPLE_REPLAY_DATA) == (1, 3, 5)

    def test_get_date(self):
        assert replay.get_date(SAMPLE_REPLAY_DATA) == dt.datetime(
            year=2018, month=7, day=31,
            hour=21, minute=21, second=18)

    def test_get_name(self):
        assert replay.get_name(SAMPLE_REPLAY_DATA) == 'SAMPLE REPLAY'

    def test_get_description(self):
        assert replay.get_description(SAMPLE_REPLAY_DATA) == 'This is a replay I recorded to use as a sample in my replay parser.'

    def test_get_stage_type(self):
        assert replay.get_stage_type(SAMPLE_REPLAY_DATA) == replay.StageType.AETHER

    def test_get_stage(self):
        assert replay.get_stage(SAMPLE_REPLAY_DATA) == replay.Stage.SPIRIT_TREE

    def test_get_stock(self):
        assert replay.get_stock(SAMPLE_REPLAY_DATA) == 1

    def test_get_time(self):
        assert replay.get_time(SAMPLE_REPLAY_DATA) == 8

    def test_is_teams_enabled_true(self):
        assert replay.is_teams_enabled(SAMPLE_REPLAY_DATA) == False
    
    def test_is_teams_enabled_false(self):
        assert replay.is_teams_enabled(ALT_SAMPLE_REPLAY_DATA)

    def test_is_friendly_fire_enabled_true(self):
        assert replay.is_friendly_fire_enabled(SAMPLE_REPLAY_DATA) == False

    @pytest.mark.skip
    def test_is_friendly_fire_enabled_false(self):
        pytest.fail('Test case not covered')

    @pytest.mark.skip
    def test_is_online_true(self):
        pytest.fail('Test case not covered')

    def test_is_online_false(self):
        assert replay.is_online(SAMPLE_REPLAY_DATA) == False

    def test_get_player_data(self):
        players = replay.get_player_data(SAMPLE_REPLAY_DATA)
        assert len(players) == 1
        assert players[0] == SAMPLE_PLAYER_DATA

    def test_get_player_data_multiplayer(self):
        players = replay.get_player_data(ALT_SAMPLE_REPLAY_DATA)
        assert len(players) == 2
        assert players[0] == ALT_SAMPLE_PLAYER_DATA[0]
        assert players[1] == ALT_SAMPLE_PLAYER_DATA[1]

    def test_get_all_frame_data(self):
        all_actions = replay.get_all_frame_data(SAMPLE_REPLAY_DATA)
        assert len(all_actions) == 1
        actions_p1 = all_actions[0]
        assert len(actions_p1) == 717
        assert actions_p1[0] == '1Z'
        assert actions_p1[1] == '101zy327R'
        assert actions_p1[24] == '148C'
        assert actions_p1[29] == '154Zy  0rc'
        assert actions_p1[394] == '1293zy143LU'
        assert actions_p1[716] == '2385y  0'
        assert actions_p1[715] == '2384Zy180d'
        assert actions_p1[714] == '2366zD'

    def test_get_duration(self):
        assert replay.get_duration(replay.get_all_frame_data(SAMPLE_REPLAY_DATA)) == 2385

    def test_get_duration_multiplayer(self):
        assert replay.get_duration(replay.get_all_frame_data(ALT_SAMPLE_REPLAY_DATA)) == 2208


class TestReplay:

    @pytest.fixture
    def r(self):
        return replay.Replay(SAMPLE_REPLAY_DATA)

    def test_player_data(self, r):
        assert r._player_data == replay.get_player_data(SAMPLE_REPLAY_DATA)

    def test_is_starred(self, r):
        assert r.is_starred == replay.is_starred(SAMPLE_REPLAY_DATA)

    def test_version(self, r):
        assert r.version == replay.get_version(SAMPLE_REPLAY_DATA)

    def test_date(self, r):
        assert r.date == replay.get_date(SAMPLE_REPLAY_DATA)

    def test_name(self, r):
        assert r.name == replay.get_name(SAMPLE_REPLAY_DATA)

    def test_description(self, r):
        assert r.description == replay.get_description(SAMPLE_REPLAY_DATA)

    def test_stage_type(self, r):
        assert r.stage_type == replay.get_stage_type(SAMPLE_REPLAY_DATA)
    
    def test_stock(self, r):
        assert r.stock == replay.get_stock(SAMPLE_REPLAY_DATA)

    def test_time(self, r):
        assert r.time == replay.get_time(SAMPLE_REPLAY_DATA)

    def test_is_teams_enabled(self, r):
        assert r.is_teams_enabled == replay.is_teams_enabled(SAMPLE_REPLAY_DATA)

    def test_is_friendly_fire_enabled(self, r):
        assert r.is_friendly_fire_enabled == replay.is_friendly_fire_enabled(SAMPLE_REPLAY_DATA)

    def test_is_online(self, r):
        assert r.is_online == replay.is_online(SAMPLE_REPLAY_DATA)

    def test_duration(self, r):
        assert r.duration == replay.get_duration(replay.get_all_frame_data(SAMPLE_REPLAY_DATA))

    def test_actions_caching(self, r):
        assert id(r.players[0].actions) == id(r.actions[0])
    
    def test_states_caching(self, r):
        assert id(r.players[0].states == id(r.states[0]))