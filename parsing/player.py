import enum
import functools
import re
from .frame import FrameData


class Character(enum.IntEnum):
    
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


class PlayerBuffer:
    
    frame_regex= r'(\d+[a-x|z|A-X|Z]+y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d*y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d+[a-x|z|A-X|Z]+)'
    frame_pattern = re.compile(frame_regex)

    @staticmethod
    def is_human(buffer):
        return buffer[0] == 'H'

    @staticmethod
    def get_name(buffer):
        return buffer[1:34].rstrip()

    @staticmethod
    def get_tag(buffer):
        return buffer[34:39].rstrip()

    @staticmethod
    def get_character(buffer):
        return Character(int(buffer[39:41]))

    @classmethod
    def get_frame_data(cls, buffer):
        return [
            x for x in cls.frame_pattern.split(
                buffer.split('\n')[1].rstrip()) 
            if x
        ]


class Player:
    
    def __init__(self, buffer):
        self._buffer = buffer

    @property
    @functools.lru_cache(maxsize=32)
    def _frame_data(self):
        return PlayerBuffer.get_frame_data(self._buffer)

    @property
    def is_human(self):
        return PlayerBuffer.is_human(self._buffer)

    @property
    def name(self):
        return PlayerBuffer.get_name(self._buffer)

    @property
    def tag(self):
        return PlayerBuffer.get_tag(self._buffer)

    @property
    def character(self):
        return PlayerBuffer.get_character(self._buffer)

    @property
    @functools.lru_cache(maxsize=32)
    def actions(self):
        return FrameData.get_action_map(self._frame_data)

    @property
    @functools.lru_cache(maxsize=32)
    def states(self):
        return FrameData.get_state_table(self._frame_data)