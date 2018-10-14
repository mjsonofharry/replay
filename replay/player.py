import enum
import functools
import re
from .frame import FrameData, ActionTable


class Character(enum.Enum):
    
    INVALID = -1
    ERROR_1 = 0
    ERROR_2 = 1
    ZETTERBURN = 2
    ORCANE = 3
    WRASTOR = 4
    KRAGG = 5
    FORSBURN = 6
    MAYPUL = 7
    ABSA = 8
    ETALUS = 9
    ORI = 10
    RANNO = 11
    CLAIREN = 12


class PlayerData:
    
    frame_regex= r'(\d+[a-x|z|A-X|Z]+y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d*y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d+[a-x|z|A-X|Z]+)'
    frame_pattern = re.compile(frame_regex)

    @staticmethod
    def is_human(player_data):
        return player_data[0] == 'H'

    @staticmethod
    def get_name(player_data):
        return player_data[1:34].rstrip()

    @staticmethod
    def get_tag(player_data):
        return player_data[34:39].rstrip()

    @staticmethod
    def get_character(player_data):
        return Character(int(player_data[39:41]))

    @classmethod
    def get_frame_data(cls, player_data):
        return [
            x for x in cls.frame_pattern.split(
                player_data.split('\n')[1].rstrip()) 
            if x
        ]


class Player:
    
    def __init__(self, player_data):
        self._player_data = player_data

    @property
    @functools.lru_cache(maxsize=32)
    def _frame_data(self):
        return PlayerData.get_frame_data(self._player_data)

    @property
    def is_human(self):
        return PlayerData.is_human(self._player_data)

    @property
    def name(self):
        return PlayerData.get_name(self._player_data)

    @property
    def tag(self):
        return PlayerData.get_tag(self._player_data)

    @property
    def character(self):
        return PlayerData.get_character(self._player_data)

    @property
    @functools.lru_cache(maxsize=32)
    def lookup_table(self):
        return ActionTable(FrameData.get_lookup_table(self._frame_data))

    @property
    @functools.lru_cache(maxsize=32)
    def state_table(self):
        return ActionTable(FrameData.get_state_table(self._frame_data))