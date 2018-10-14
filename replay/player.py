import re
from .utilities import Character

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
