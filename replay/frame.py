import bisect
import re
from .utilities import ActionType, Action

class FrameData:
    action_regex = r'(^\d+)|([a-x|z|A-X|Z])|(y[\d| ]{3})'
    action_pattern = re.compile(action_regex)
    token_to_action = {
        'J': Action.JUMP_PRESS,
        'j': Action.JUMP_RELEASE,
        'A': Action.ATTACK_PRESS,
        'a': Action.ATTACK_RELEASE,
        'B': Action.SPECIAL_PRESS,
        'b': Action.SPECIAL_RELEASE,
        'C': Action.STRONG_PRESS,
        'c': Action.STRONG_RELEASE,
        'F': Action.STRONG_LEFT_PRESS,
        'f': Action.STRONG_LEFT_RELEASE,
        'G': Action.STRONG_RIGHT_PRESS,
        'g': Action.STRONG_RIGHT_RELEASE,
        'X': Action.STRONG_UP_PRESS,
        'x': Action.STRONG_UP_RELEASE,
        'W': Action.STRONG_DOWN_PRESS,
        'w': Action.STRONG_DOWN_RELEASE,
        'S': Action.DODGE_PRESS,
        's': Action.DODGE_RELEASE,
        'U': Action.UP_PRESS,
        'u': Action.UP_RELEASE,
        'M': Action.UP_TAP,
        'P': Action.UP_TAP,
        'D': Action.DOWN_PRESS,
        'd': Action.DOWN_RELEASE,
        'O': Action.DOWN_TAP,
        'L': Action.LEFT_PRESS,
        'l': Action.LEFT_RELEASE,
        'E': Action.LEFT_TAP,
        'R': Action.RIGHT_PRESS,
        'r': Action.RIGHT_RELEASE,
        'I': Action.RIGHT_TAP,
        'Z': Action.ANGLES_ENABLED,
        'z': Action.ANGLES_DISABLED
    }
    action_to_boolean = {
        Action.JUMP_PRESS: True,
        Action.JUMP_RELEASE: False,
        Action.ATTACK_PRESS: True,
        Action.ATTACK_RELEASE: False,
        Action.SPECIAL_PRESS: True,
        Action.SPECIAL_RELEASE: False,
        Action.STRONG_PRESS: True,
        Action.STRONG_RELEASE: False,
        Action.STRONG_LEFT_PRESS: True,
        Action.STRONG_LEFT_RELEASE: False,
        Action.STRONG_RIGHT_PRESS: True,
        Action.STRONG_RIGHT_RELEASE: False,
        Action.STRONG_UP_PRESS: True,
        Action.STRONG_UP_RELEASE: False,
        Action.STRONG_DOWN_PRESS: True,
        Action.STRONG_DOWN_RELEASE: False,
        Action.DODGE_PRESS: True,
        Action.DODGE_RELEASE: False,
        Action.UP_PRESS: True,
        Action.UP_RELEASE: False,
        Action.UP_TAP: True,
        Action.DOWN_PRESS: True,
        Action.DOWN_RELEASE: False,
        Action.DOWN_TAP: True,
        Action.LEFT_PRESS: True,
        Action.LEFT_RELEASE: False,
        Action.LEFT_TAP: True,
        Action.RIGHT_PRESS: True,
        Action.RIGHT_RELEASE: False,
        Action.RIGHT_TAP: True,
        Action.ANGLES_ENABLED: True,
        Action.ANGLES_DISABLED: False
    }
    action_to_action_type = {
        Action.JUMP_PRESS: ActionType.JUMP,
        Action.JUMP_RELEASE: ActionType.JUMP,
        Action.ATTACK_PRESS: ActionType.ATTACK,
        Action.ATTACK_RELEASE: ActionType.ATTACK,
        Action.SPECIAL_PRESS: ActionType.SPECIAL,
        Action.SPECIAL_RELEASE: ActionType.SPECIAL,
        Action.STRONG_PRESS: ActionType.STRONG,
        Action.STRONG_RELEASE: ActionType.STRONG,
        Action.STRONG_LEFT_PRESS: ActionType.STRONG_LEFT,
        Action.STRONG_LEFT_RELEASE: ActionType.STRONG_LEFT,
        Action.STRONG_RIGHT_PRESS: ActionType.STRONG_RIGHT,
        Action.STRONG_RIGHT_RELEASE: ActionType.STRONG_RIGHT,
        Action.STRONG_UP_PRESS: ActionType.STRONG_UP,
        Action.STRONG_UP_RELEASE: ActionType.STRONG_UP,
        Action.STRONG_DOWN_PRESS: ActionType.STRONG_DOWN,
        Action.STRONG_DOWN_RELEASE: ActionType.STRONG_DOWN,
        Action.DODGE_PRESS: ActionType.DODGE,
        Action.DODGE_RELEASE: ActionType.DODGE,
        Action.UP_PRESS: ActionType.UP,
        Action.UP_RELEASE: ActionType.UP,
        Action.UP_TAP: ActionType.UP,
        Action.UP_TAP: ActionType.UP,
        Action.DOWN_PRESS: ActionType.DOWN,
        Action.DOWN_RELEASE: ActionType.DOWN,
        Action.DOWN_TAP: ActionType.DOWN,
        Action.LEFT_PRESS: ActionType.LEFT,
        Action.LEFT_RELEASE: ActionType.LEFT,
        Action.LEFT_TAP: ActionType.LEFT,
        Action.RIGHT_PRESS: ActionType.RIGHT,
        Action.RIGHT_RELEASE: ActionType.RIGHT,
        Action.RIGHT_TAP: ActionType.RIGHT,
        Action.ANGLES_ENABLED: ActionType.ANGLES,
        Action.ANGLES_DISABLED: ActionType.ANGLES,
    }
    angle_to_action_type = {
        0: (ActionType.ANGLE_RIGHT,),
        45: (ActionType.ANGLE_RIGHT, ActionType.ANGLE_UP),
        90: (ActionType.ANGLE_UP,),
        135: (ActionType.ANGLE_UP, ActionType.ANGLE_LEFT,),
        180: (ActionType.ANGLE_LEFT,),
        225: (ActionType.ANGLE_LEFT, ActionType.ANGLE_DOWN),
        270: (ActionType.ANGLE_DOWN,),
        315: (ActionType.ANGLE_DOWN, ActionType.ANGLE_RIGHT),
        360: (ActionType.ANGLE_RIGHT,)
    }

    @classmethod
    def convert_token_to_action(cls, t):
        if t[0] == 'y':
            return int(t[1:])
        else:
            return cls.token_to_action.get(t, Action.INVALID)
    
    @classmethod
    def convert_multiple_tokens_to_actions(cls, ts):
        return [cls.convert_token_to_action(t) for t in ts]

    @classmethod
    def split_frames_into_tokens(cls, frame_data):
        return [
            [x1 for x1 in FrameData.action_pattern.split(x) if x1] 
            for x in frame_data
        ]

    @classmethod
    def get_lookup_table(cls, frame_data, raw=False):
        return {
            int(x[0]): (
                x[1:] if raw 
                else cls.convert_multiple_tokens_to_actions(x[1:])
            )
            for x in cls.split_frames_into_tokens(frame_data)
        }

    @classmethod
    def get_state_table(cls, frame_data):
        table = {}
        state = [False]*18
        for x in cls.split_frames_into_tokens(frame_data):
            state[-8:] = [False]*8
            n = int(x[0])
            tokens = x[1:]
            actions = cls.convert_multiple_tokens_to_actions(tokens)
            for a in actions:
                if isinstance(a, Action):
                    state[cls.action_to_action_type[a]] = cls.action_to_boolean[a]
                else:
                    for x in cls.angle_to_action_type[cls.snap_angle(a)]:
                        state[x] = True
            table[n] = list(state)
        return table

    @staticmethod
    def snap_frame(lookup_table, n):
        keys = list(lookup_table.keys())
        i = bisect.bisect_right(keys, n)
        if i:
            return keys[i-1]
        raise ValueError
    
    @classmethod
    def snap_multiple_frames(cls, lookup_table, ns):
        return [cls.snap_frame(lookup_table, n) for n in ns]

    @classmethod
    def get_closest_action(cls, lookup_table, n):
        return lookup_table[cls.snap_frame(lookup_table, n)]

    @staticmethod
    def snap_angle(n):
        if n < 0 or n > 360:
            raise ValueError
        result = 45 * round(float(n) / 45)
        if result == 360:
            return 0
        return result
