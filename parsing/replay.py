import datetime
import enum
import functools
import re
from . import player


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


REGEX = r'H.*\n.*\n'
PATTERN = re.compile(REGEX)
DATE_FORMAT = '%H%M%S%d%m%Y'

def is_starred(buffer):
    return bool(int(buffer[0]))

def get_version(buffer):
    return (
        int(buffer[1:3]), 
        int(buffer[3:5]),
        int(buffer[5:7])
    )

def get_date(buffer):
    return datetime.datetime.strptime(
        buffer[7:21], DATE_FORMAT)

def get_name(buffer):
    return buffer[21:53].rstrip()

def get_description(buffer):
    return buffer[53:193].rstrip()

def _get_unidentified_metadata_1(buffer):
    return buffer[194:204]

def get_stage_type(buffer):
    return StageType(int(buffer[204]))

def get_stage(buffer):
    return Stage(int(buffer[205:207]))

def get_stock(buffer):
    return int(buffer[207:209])

def get_time(buffer):
    return int(buffer[209:211])

def is_teams_enabled(buffer):
    return bool(int(buffer[212]))

def is_friendly_fire_enabled(buffer):
    return bool(int(buffer[213]))

def is_online(buffer):
    return bool(int(buffer[214]))

def _get_unidentified_metadata_2(buffer):
    return int(buffer[215:218]), int(buffer[218:222])

def get_player_data(buffer):
    return PATTERN.findall(buffer)

def get_all_frame_data(buffer):
    return [
        player.get_frame_data(x) for x in get_player_data(buffer)
    ]

def get_duration(all_frame_data):
    return max([
        max([int(re.findall(r'^\d+', x)[0]) for x in frames])
        for frames in all_frame_data
    ])


class Replay:

    def __init__(self, buffer):
        self._buffer = buffer

    @property
    @functools.lru_cache(maxsize=32)
    def _player_data(self):
        return get_player_data(self._buffer)

    @property
    @functools.lru_cache(maxsize=32)
    def players(self):
        return [player.Player(x) for x in self._player_data]

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
        return is_starred(self._buffer)

    @property
    def version(self):
        return get_version(self._buffer)

    @property
    def date(self):
        return get_date(self._buffer)
    
    @property
    def name(self):
        return get_name(self._buffer)
    
    @property
    def description(self):
        return get_description(self._buffer)
    
    @property
    def _unknown_1(self):
        return _get_unidentified_metadata_1(self._buffer)

    @property
    def stage_type(self):
        return get_stage_type(self._buffer)
    
    @property
    def stage(self):
        return get_stage(self._buffer)

    @property
    def stock(self):
        return get_stock(self._buffer)
    
    @property
    def time(self):
        return get_time(self._buffer)

    @property
    def is_teams_enabled(self):
        return is_teams_enabled(self._buffer)
    
    @property
    def is_friendly_fire_enabled(self):
        return is_friendly_fire_enabled(self._buffer)
    
    @property
    def is_online(self):
        return is_online(self._buffer)

    @property
    def _unknown_2(self):
        return _get_unidentified_metadata_2(self._buffer)

    @property
    @functools.lru_cache(maxsize=32)
    def duration(self):
        return get_duration([x._frame_data for x in self.players])
