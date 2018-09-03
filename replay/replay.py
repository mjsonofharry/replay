import enum
import bisect
import datetime
import os
import re

class Action(enum.IntEnum):
    INVALID = -1
    JUMP_PRESS = 0
    JUMP_RELEASE = 1
    ATTACK_PRESS = 2
    ATTACK_RELEASE = 3
    SPECIAL_PRESS = 4
    SPECIAL_RELEASE = 5
    STRONG_PRESS = 6
    STRONG_RELEASE = 7
    STRONG_LEFT_PRESS = 8
    STRONG_LEFT_RELEASE = 9
    STRONG_RIGHT_PRESS = 10
    STRONG_RIGHT_RELEASE = 11
    STRONG_UP_PRESS = 12
    STRONG_UP_RELEASE = 13
    STRONG_DOWN_PRESS = 14
    STRONG_DOWN_RELEASE = 15
    DODGE_PRESS = 16
    DODGE_RELEASE = 17
    UP_PRESS = 18
    UP_RELEASE = 19
    UP_TAP = 20
    DOWN_PRESS = 21
    DOWN_RELEASE = 22
    DOWN_TAP = 23
    LEFT_PRESS = 24
    LEFT_RELEASE = 25
    LEFT_TAP = 26
    RIGHT_PRESS = 27
    RIGHT_RELEASE = 28
    RIGHT_TAP = 29
    ANGLES_ENABLED = 30
    ANGLES_DISABLED = 31

class Replay:
    player_regex = r"H.*\n.*\n"
    player_pattern = re.compile(player_regex)
    frame_regex= r"(\d+[a-x|z|A-X|Z]+y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d*y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d+[a-x|z|A-X|Z]+)"
    frame_pattern = re.compile(frame_regex)
    action_regex = r"(^\d+)|([a-x|z|A-X|Z])|(y[\d| ]{3})"
    action_pattern = re.compile(action_regex)
    date_fmtstr = "%H%M%S%d%m%Y"

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

    @staticmethod
    def read_replay_buffer(replay_file_path):
        fin = open(replay_file_path)
        data = fin.read()
        fin.close()
        return data

    @staticmethod
    def is_starred(replay_buffer):
        return replay_buffer[0] == 1

    @staticmethod
    def get_name(replay_buffer):
        return replay_buffer[21:53].rstrip()

    @staticmethod
    def get_description(replay_buffer):
        return replay_buffer[53:193].rstrip()

    @staticmethod
    def get_version(replay_buffer):
        return int(replay_buffer[1:3]), int(replay_buffer[3:5]), int(replay_buffer[5:7])

    @classmethod
    def get_date(cls, replay_buffer):
        return datetime.datetime.strptime(replay_buffer[7:21], cls.date_fmtstr)

    @classmethod
    def get_players(cls, replay_buffer):
        return cls.player_pattern.findall(replay_buffer)

    @classmethod
    def get_frames(cls, player_buffer):
        return [
            x for x in 
            cls.frame_pattern.split(player_buffer.split("\n")[1].rstrip()) if x
        ]

    @classmethod
    def get_frames_all_players(cls, replay_buffer):
        return [
            cls.get_frames(x) for x in cls.get_players(replay_buffer)
        ]

    @staticmethod
    def get_duration(frames_all_players):
        return max([
            max([int(re.findall(r"^\d+", x)[0]) for x in frames])
            for frames in frames_all_players
        ])

    @staticmethod
    def get_frame_lookup_table(frames):
        return {
            int(x[0]): x[1:] for x in [
                [y for y in Replay.action_pattern.split(z) if y] for z in frames
            ]
        }

    @classmethod
    def convert_frame_tokens_to_actions(cls, frame):
        return [
            cls.action_lookup.get(x, Action.INVALID)
            if x[0] != "y" else int(x[1:]) for x in frame
        ]

    @classmethod
    def get_parsed_frame_lookup_table(cls, frames):
        return {
            int(x[0]): cls.convert_frame_tokens_to_actions(x[1:]) for x in [
                [y for y in Replay.action_pattern.split(z) if y] for z in frames
            ]
        }
    
    @staticmethod
    def snap_frame(lookup, n):
        keys = list(lookup.keys())
        i = bisect.bisect_right(keys, n)
        if i: return keys[i-1]
        raise ValueError
    
    @classmethod
    def get_closest_frame(cls, lookup, n):
        return lookup[cls.snap_frame(lookup, n)]

    @staticmethod
    def snap_angle(n):
        if n < 0 or n > 360: raise ValueError
        result = min(
            [0, 45, 90, 135, 180, 225, 270, 315, 360],
            key=lambda x: abs(x - n))
        if result == 360:
            return 0
        return result

    def __init__(self, replay_buffer):
        self.name = self.get_name(replay_buffer)
        self.description = self.get_description(replay_buffer)
        self.version = self.get_version(replay_buffer)

        frames_all = self.get_frames_all_players(replay_buffer)
        self.duration = self.get_duration(frames_all)
        self.lookups = [self.get_parsed_frame_lookup_table(x) for x in frames_all]
