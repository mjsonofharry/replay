import enum
import bisect
import datetime
import os
import re

class Replay:
    player_regex = r"H.*\n.*\n"
    player_pattern = re.compile(player_regex)
    action_regex= r"(\d+[a-x|z|A-X|Z]+y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d*y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d+[a-x|z|A-X|Z]+)"
    action_pattern = re.compile(action_regex)
    frame_regex = r"(^\d+)|([a-x|z|A-X|Z])|(y[\d| ]{3}[A-z]*)"
    frame_pattern = re.compile(frame_regex)
    date_fmtstr = "%H%M%S%d%m%Y"

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
                [ a for a in Replay.frame_pattern.split(action) if a ]
                for action in action_data
            ]
        }
    
    @staticmethod
    def snap_index_to_lookup(lookup, n):
        keys = list(lookup.keys())
        i = bisect.bisect_right(keys, n)
        if i: return keys[i-1]
        raise ValueError