import datetime as dt
import os
import re
from typing import List, Tuple

class Replay:
    human_regex: str = r"H.*\n.*\n"
    human_pattern = re.compile(human_regex)
    action_regex: str = r"(\d+[a-x|z|A-X|Z]+y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d*y[\d| ]{3}[a-x|z|A-X|Z]*)|(\d+[a-x|z|A-X|Z]+)"
    action_pattern = re.compile(action_regex)
    frame_regex: str = r"(^\d+)|([a-x|z|A-X|Z])|(y[\d| ]{3}[A-z]*)"
    frame_pattern = re.compile(frame_regex)
    date_fmtstr: str = "%H%M%S%d%m%Y"

    @staticmethod
    def read_data(replay_file_path: str) -> str:
        fin = open(replay_file_path)
        data = fin.read()
        fin.close()
        return data

    @staticmethod
    def get_name(replay_data: str) -> str:
        return replay_data.split("\n", 1)[0].split(' ', 1)[0]

    @staticmethod
    def get_version(replay_data: str) -> Tuple[str]:
        ln = replay_data.split("\n", 1)[0]
        return int(ln[1:3]), int(ln[3:5]), int(ln[5:7])

    @classmethod
    def get_datetime(cls, replay_data: str) -> dt.datetime:
        return dt.datetime.strptime(replay_data[7:21], cls.date_fmtstr)

    @classmethod
    def _split_actions(cls, ln: str) -> List[str]:
        return [x for x in cls.action_pattern.split(ln.rstrip()) if x]

    @classmethod
    def _split_frame(cls, ln: str) -> List[str]:
        return [x for x in cls.frame_pattern.split(ln.rstrip()) if x]

    @classmethod
    def get_actions(cls, replay_data: str) -> List[List[str]]:
        return [
            cls._split_actions(a) for a in [
                h.split("\n")[1] for h in cls.human_pattern.findall(replay_data)
            ]
        ]

    @staticmethod
    def get_duration(all_actions: List[List[str]]) -> dt.datetime:
        return max([
            max([int(re.findall(r"^\d+", a)[0]) for a in actions])
            for actions in all_actions
        ])
