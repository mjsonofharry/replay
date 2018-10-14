import datetime
import enum
import re
from .player import PlayerData


class Stage(enum.Enum):
    
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


class StageType(enum.Enum):

    INVALID = -1
    BASIC = 0
    AETHER = 1


class ReplayData:

    player_regex = r'H.*\n.*\n'
    player_pattern = re.compile(player_regex)
    date_fmtstr = '%H%M%S%d%m%Y'

    @staticmethod
    def is_starred(replay_data):
        return replay_data[0] == 1

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
    def __get_unidentified_metadata_1(replay_data):
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
    def __get_unidentified_metadata_2(replay_data):
        return int(replay_data[215:218]), int(replay_data[218:222])

    @classmethod
    def get_player_data(cls, replay_data):
        return cls.player_pattern.findall(replay_data)

    @classmethod
    def get_frame_data_all_players(cls, replay_data):
        return [
            PlayerData.get_frame_data(x) for x in cls.get_player_data(replay_data)
        ]

    @staticmethod
    def get_duration(frame_data_all_players):
        return max([
            max([int(re.findall(r'^\d+', x)[0]) for x in frames])
            for frames in frame_data_all_players
        ])
