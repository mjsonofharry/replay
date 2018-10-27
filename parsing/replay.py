import datetime
import enum
import functools
import re
from .player import PlayerData, Player


class Stage(enum.IntEnum):
    
    INVALID = -1
    MENU = 0
    TREETOP_LODGE = 1
    FIRE_CAPITOL = 2
    AIR_ARMADA = 3
    ROCK_WALL = 4
    MERCHANT_PORT = 5
    CRASH_GAME = 6
    BLAZING_HIDEOUT = 7
    TOWER_HEAVEN = 8
    TEMPEST_PEAK = 9
    FROZEN_FORTRESS = 10
    AETHERIAL_GATES = 11
    ENDLESS_ABYSS = 12
    UNAVAILABLE = 13
    CEO_RING = 14
    SPIRIT_TREE = 15
    STAGE_NAME = 16
    NEO_FIRE_CAPITAL = 17
    SWAMPY_ESTUARY = 18


class StageType(enum.IntEnum):

    INVALID = -1
    BASIC = 0
    AETHER = 1


class ReplayData:

    player_regex = r'H.*\n.*\n'
    player_pattern = re.compile(player_regex)
    date_fmtstr = '%H%M%S%d%m%Y'

    @staticmethod
    def is_starred(replay_data):
        return bool(int(replay_data[0]))

    @staticmethod
    def get_version(replay_data):
        return (
            int(replay_data[1:3]), 
            int(replay_data[3:5]),
            int(replay_data[5:7])
        )

    @classmethod
    def get_date(cls, replay_data):
        return datetime.datetime.strptime(
            replay_data[7:21], cls.date_fmtstr)

    @staticmethod
    def get_name(replay_data):
        return replay_data[21:53].rstrip()

    @staticmethod
    def get_description(replay_data):
        return replay_data[53:193].rstrip()
    
    @staticmethod
    def _get_unidentified_metadata_1(replay_data):
        return replay_data[194:204]

    @staticmethod
    def get_stage_type(replay_data):
        return StageType(int(replay_data[204]))

    @staticmethod
    def get_stage(replay_data):
        return Stage(int(replay_data[205:207]))

    @staticmethod
    def get_stock(replay_data):
        return int(replay_data[207:209])

    @staticmethod
    def get_time(replay_data):
        return int(replay_data[209:211])

    @staticmethod
    def is_teams_enabled(replay_data):
        return bool(int(replay_data[212]))

    @staticmethod
    def is_friendly_fire_enabled(replay_data):
        return bool(int(replay_data[213]))

    @staticmethod
    def is_online(replay_data):
        return bool(int(replay_data[214]))

    @staticmethod
    def _get_unidentified_metadata_2(replay_data):
        return int(replay_data[215:218]), int(replay_data[218:222])

    @classmethod
    def get_player_data(cls, replay_data):
        return cls.player_pattern.findall(replay_data)

    @classmethod
    def get_all_frame_data(cls, replay_data):
        return [
            PlayerData.get_frame_data(x) for x in cls.get_player_data(replay_data)
        ]

    @staticmethod
    def get_duration(all_frame_data):
        return max([
            max([int(re.findall(r'^\d+', x)[0]) for x in frames])
            for frames in all_frame_data
        ])


class Replay:

    def __init__(self, replay_data):
        self._replay_data = replay_data

    @property
    @functools.lru_cache(maxsize=32)
    def _player_data(self):
        return ReplayData.get_player_data(self._replay_data)

    @property
    @functools.lru_cache(maxsize=32)
    def players(self):
        return [Player(x) for x in self._player_data]

    @property
    @functools.lru_cache(maxsize=32)
    def actions(self):
        return [x.actions for x in self.players]

    @property
    @functools.lru_cache(maxsize=32)
    def states(self):
        return [x.states for x in self.players]

    @property
    def is_starred(self):
        return ReplayData.is_starred(self._replay_data)

    @property
    def version(self):
        return ReplayData.get_version(self._replay_data)

    @property
    def date(self):
        return ReplayData.get_date(self._replay_data)
    
    @property
    def name(self):
        return ReplayData.get_name(self._replay_data)
    
    @property
    def description(self):
        return ReplayData.get_description(self._replay_data)
    
    @property
    def _unknown_1(self):
        return ReplayData._get_unidentified_metadata_1(self._replay_data)

    @property
    def stage_type(self):
        return ReplayData.get_stage_type(self._replay_data)
    
    @property
    def stage(self):
        return ReplayData.get_stage(self._replay_data)

    @property
    def stock(self):
        return ReplayData.get_stock(self._replay_data)
    
    @property
    def time(self):
        return ReplayData.get_time(self._replay_data)

    @property
    def is_teams_enabled(self):
        return ReplayData.is_teams_enabled(self._replay_data)
    
    @property
    def is_friendly_fire_enabled(self):
        return ReplayData.is_friendly_fire_enabled(self._replay_data)
    
    @property
    def is_online(self):
        return ReplayData.is_online(self._replay_data)

    @property
    def _unknown_2(self):
        return ReplayData._get_unidentified_metadata_2(self._replay_data)

    @property
    @functools.lru_cache(maxsize=32)
    def duration(self):
        return ReplayData.get_duration([x._frame_data for x in self.players])