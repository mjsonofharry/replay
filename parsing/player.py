import enum
import functools
import re
from . import frame


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

    
REGEX = r'(\d+[a-x|z|A-X|Z]+y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d*y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d+[a-x|z|A-X|Z]+)'
PATTERN = re.compile(REGEX)

def is_human(buffer):
    return buffer[0] == 'H'

def get_name(buffer):
    return buffer[1:34].rstrip()

def get_tag(buffer):
    return buffer[34:39].rstrip()

def get_character(buffer):
    return Character(int(buffer[39:41]))

def get_frame_data(buffer):
    return [
        x for x in PATTERN.split(
            buffer.split('\n')[1].rstrip()) 
        if x
    ]


class Player:
    
    def __init__(self, buffer):
        self._buffer = buffer

    @property
    @functools.lru_cache(maxsize=32)
    def _frame_data(self):
        return get_frame_data(self._buffer)

    @property
    def is_human(self):
        return is_human(self._buffer)

    @property
    def name(self):
        return get_name(self._buffer)

    @property
    def tag(self):
        return get_tag(self._buffer)

    @property
    def character(self):
        return get_character(self._buffer)

    @property
    @functools.lru_cache(maxsize=32)
    def actions(self):
        return frame.get_action_map(self._frame_data)

    @property
    @functools.lru_cache(maxsize=32)
    def states(self):
        return frame.get_state_table(self._frame_data)