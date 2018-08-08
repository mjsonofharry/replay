import enum
import bisect
import datetime
import os
import re

class Action(enum.IntEnum):
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
    action_regex= r"(\d+[a-x|z|A-X|Z]+y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d*y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d+[a-x|z|A-X|Z]+)"
    action_pattern = re.compile(action_regex)
    frame_regex = r"(^\d+)|([a-x|z|A-X|Z])|(y[\d| ]{3}[A-z]*)"
    frame_pattern = re.compile(frame_regex)
    date_fmtstr = "%H%M%S%d%m%Y"

    # Based on work by /u/MatthewMJV
    # Source: https://www.reddit.com/r/RivalsOfAether/comments/5sxvw2/what_i_have_learned_from_looking_through_replays/
    token_action_lookup = {
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
    def read_data(replay_file_path):
        fin = open(replay_file_path)
        data = fin.read()
        fin.close()
        return data

    @staticmethod
    def get_name(replay_data):
        return replay_data.split("\n", 1)[0].split(" ", 1)[0]

    @staticmethod
    def get_version(replay_data):
        ln = replay_data.split("\n", 1)[0]
        return int(ln[1:3]), int(ln[3:5]), int(ln[5:7])

    @classmethod
    def get_date(cls, replay_data):
        return datetime.datetime.strptime(replay_data[7:21], cls.date_fmtstr)

    @classmethod
    def get_players(cls, replay_data):
        return cls.player_pattern.findall(replay_data)

    @classmethod
    def get_actions(cls, player_data):
        return [
            x for x in 
            cls.action_pattern.split(player_data.split("\n")[1].rstrip()) if x
        ]

    @classmethod
    def get_actions_all_players(cls, replay_data):
        return [
            cls.get_actions(player_data) 
            for player_data in cls.get_players(replay_data)
        ]

    @staticmethod
    def get_duration(actions_all_players):
        return max([
            max([
                int(re.findall(r"^\d+", action)[0])
                for action in actions_one_player])
            for actions_one_player in actions_all_players
        ])

    @staticmethod
    def get_lookup(action_data):
        return {
            int(x[0]): x[1:] 
            for x in [
                [a for a in Replay.frame_pattern.split(action) if a]
                for action in action_data
            ]
        }
    
    @staticmethod
    def snap_index_to_lookup(lookup, n):
        keys = list(lookup.keys())
        i = bisect.bisect_right(keys, n)
        if i: return keys[i-1]
        raise ValueError
    
    @staticmethod
    def snap_angle_to_eighth(n):
        result = min(
            [0, 45, 90, 135, 180, 225, 270, 315, 360],
            key=lambda x: abs(x - n))
        if result == 360:
            return 0
        return result