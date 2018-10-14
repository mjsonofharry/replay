import datetime as dt
import pytest
from test_common import ReplayData, Replay, Stage, StageType, SAMPLE_REPLAY_DATA, SAMPLE_PLAYER_DATA


class TestReplayData:
    
    @pytest.mark.skip
    def test_is_starred_true(self):
        pytest.fail('Test case not covered')

    def test_is_starred_false(self):
        assert ReplayData.is_starred(SAMPLE_REPLAY_DATA) == False

    def test_get_version(self):
        assert ReplayData.get_version(SAMPLE_REPLAY_DATA) == (1, 3, 5)

    def test_get_date(self):
        assert ReplayData.get_date(SAMPLE_REPLAY_DATA) == dt.datetime(
            year=2018, month=7, day=31,
            hour=21, minute=21, second=18)

    def test_get_name(self):
        assert ReplayData.get_name(SAMPLE_REPLAY_DATA) == 'SAMPLE REPLAY'

    def test_get_description(self):
        assert ReplayData.get_description(SAMPLE_REPLAY_DATA) == 'This is a replay I recorded to use as a sample in my replay parser.'

    def test_get_stage_type(self):
        assert ReplayData.get_stage_type(SAMPLE_REPLAY_DATA) == StageType.AETHER

    def test_get_stage(self):
        assert ReplayData.get_stage(SAMPLE_REPLAY_DATA) == Stage.SPIRIT_TREE

    def test_get_stock(self):
        assert ReplayData.get_stock(SAMPLE_REPLAY_DATA) == 1

    def test_get_time(self):
        assert ReplayData.get_time(SAMPLE_REPLAY_DATA) == 8

    def test_is_teams_enabled_true(self):
        assert ReplayData.is_teams_enabled(SAMPLE_REPLAY_DATA) == False
    
    @pytest.mark.skip
    def test_is_teams_enabled_false(self):
        pytest.fail('Test case not covered')

    def test_is_friendly_fire_enabled_true(self):
        assert ReplayData.is_friendly_fire_enabled(SAMPLE_REPLAY_DATA) == False

    @pytest.mark.skip
    def test_is_friendly_fire_enabled_false(self):
        pytest.fail('Test case not covered')

    @pytest.mark.skip
    def test_is_online_true(self):
        pytest.fail('Test case not covered')

    def test_is_online_false(self):
        assert ReplayData.is_online(SAMPLE_REPLAY_DATA) == False

    def test_get_player_data(self):
        players = ReplayData.get_player_data(SAMPLE_REPLAY_DATA)
        assert len(players) == 1
        assert players[0] == SAMPLE_PLAYER_DATA

    def test_get_all_frame_data(self):
        all_actions = ReplayData.get_all_frame_data(SAMPLE_REPLAY_DATA)
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
        assert ReplayData.get_duration(ReplayData.get_all_frame_data(SAMPLE_REPLAY_DATA)) == 2385


class TestReplay:

    @pytest.fixture
    def replay(self):
        return Replay(SAMPLE_REPLAY_DATA)

    def test_player_data(self, replay):
        assert replay._player_data == ReplayData.get_player_data(SAMPLE_REPLAY_DATA)

    def test_is_starred(self, replay):
        assert replay.is_starred == ReplayData.is_starred(SAMPLE_REPLAY_DATA)

    def test_version(self, replay):
        assert replay.version == ReplayData.get_version(SAMPLE_REPLAY_DATA)

    def test_date(self, replay):
        assert replay.date == ReplayData.get_date(SAMPLE_REPLAY_DATA)

    def test_name(self, replay):
        assert replay.name == ReplayData.get_name(SAMPLE_REPLAY_DATA)

    def test_description(self, replay):
        assert replay.description == ReplayData.get_description(SAMPLE_REPLAY_DATA)

    def test_stage_type(self, replay):
        assert replay.stage_type == ReplayData.get_stage_type(SAMPLE_REPLAY_DATA)
    
    def test_stock(self, replay):
        assert replay.stock == ReplayData.get_stock(SAMPLE_REPLAY_DATA)

    def test_time(self, replay):
        assert replay.time == ReplayData.get_time(SAMPLE_REPLAY_DATA)

    def test_is_teams_enabled(self, replay):
        assert replay.is_teams_enabled == ReplayData.is_teams_enabled(SAMPLE_REPLAY_DATA)

    def test_is_friendly_fire_enabled(self, replay):
        assert replay.is_friendly_fire_enabled == ReplayData.is_friendly_fire_enabled(SAMPLE_REPLAY_DATA)

    def test_is_online(self, replay):
        assert replay.is_online == ReplayData.is_online(SAMPLE_REPLAY_DATA)

    def test_duration(self, replay):
        assert replay.duration == ReplayData.get_duration(ReplayData.get_all_frame_data(SAMPLE_REPLAY_DATA))