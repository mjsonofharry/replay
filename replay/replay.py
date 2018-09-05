import bisect
import datetime
import os
import re
from .utilities import Action, Character, Stage, StageType


class FrameData:
    action_regex = r"(^\d+)|([a-x|z|A-X|Z])|(y[\d| ]{3})"
    action_pattern = re.compile(action_regex)
    action_lookup = {
        "J": Action.JUMP_PRESS,
        "j": Action.JUMP_RELEASE,
        "A": Action.ATTACK_PRESS,
        "a": Action.ATTACK_RELEASE,
        "B": Action.SPECIAL_PRESS,
        "b": Action.SPECIAL_RELEASE,
        "C": Action.STRONG_PRESS,
        "c": Action.STRONG_RELEASE,
        "F": Action.STRONG_LEFT_PRESS,
        "f": Action.STRONG_LEFT_RELEASE,
        "G": Action.STRONG_RIGHT_PRESS,
        "g": Action.STRONG_RIGHT_RELEASE,
        "X": Action.STRONG_UP_PRESS,
        "x": Action.STRONG_UP_RELEASE,
        "W": Action.STRONG_DOWN_PRESS,
        "w": Action.STRONG_DOWN_RELEASE,
        "S": Action.DODGE_PRESS,
        "s": Action.DODGE_RELEASE,
        "U": Action.UP_PRESS,
        "u": Action.UP_RELEASE,
        "M": Action.UP_TAP,
        "P": Action.UP_TAP,
        "D": Action.DOWN_PRESS,
        "d": Action.DOWN_RELEASE,
        "O": Action.DOWN_TAP,
        "L": Action.LEFT_PRESS,
        "l": Action.LEFT_RELEASE,
        "E": Action.LEFT_TAP,
        "R": Action.RIGHT_PRESS,
        "r": Action.RIGHT_RELEASE,
        "I": Action.RIGHT_TAP,
        "Z": Action.ANGLES_ENABLED,
        "z": Action.ANGLES_DISABLED
    }

    @classmethod
    def convert_token_to_action(cls, token):
        if token[0] == "y": return int(token[1:])
        else: return cls.action_lookup.get(token, Action.INVALID)
    
    @classmethod
    def convert_multiple_tokens_to_actions(cls, tokens):
        return [
            cls.convert_token_to_action(t) 
            for t in tokens
        ]

    @classmethod
    def get_raw_lookup_table(cls, frame_data):
        split_frames = [
            [x1 for x1 in FrameData.action_pattern.split(x) if x1] 
            for x in frame_data
        ]
        return {
            int(x[0]): x[1:]
            for x in split_frames
        }

    @classmethod
    def get_lookup_table(cls, frame_data):
        split_frames = [
            [x1 for x1 in FrameData.action_pattern.split(x) if x1] 
            for x in frame_data
        ]
        return {
            int(x[0]): cls.convert_multiple_tokens_to_actions(x[1:])
            for x in split_frames
        }

    @staticmethod
    def snap_frame(lookup_table, n):
        keys = list(lookup_table.keys())
        i = bisect.bisect_right(keys, n)
        if i: return keys[i-1]
        raise ValueError
    
    @classmethod
    def get_closest_action(cls, lookup_table, n):
        return lookup_table[cls.snap_frame(lookup_table, n)]

    @staticmethod
    def snap_angle(n):
        if n < 0 or n > 360: raise ValueError
        result = min(
            [0, 45, 90, 135, 180, 225, 270, 315, 360],
            key=lambda x: abs(x - n))
        if result == 360:
            return 0
        return result


class PlayerData:
    frame_regex= r"(\d+[a-x|z|A-X|Z]+y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d*y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d+[a-x|z|A-X|Z]+)"
    frame_pattern = re.compile(frame_regex)

    @staticmethod
    def is_human(player_data):
        return player_data[0] == "H"

    @staticmethod
    def get_player_name(player_data):
        return player_data[1:34].rstrip()

    @staticmethod
    def get_player_tag(player_data):
        return player_data[34:39].rstrip()

    @staticmethod
    def get_character(player_data):
        return Character(int(player_data[39:41]))

    @classmethod
    def get_frame_data(cls, player_data):
        return [
            x for x in cls.frame_pattern.split(
                player_data.split("\n")[1].rstrip()) 
            if x
        ]


class ReplayData:
    player_regex = r"H.*\n.*\n"
    player_pattern = re.compile(player_regex)
    date_fmtstr = "%H%M%S%d%m%Y"

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
            max([int(re.findall(r"^\d+", x)[0]) for x in frames])
            for frames in frame_data_all_players
        ])
