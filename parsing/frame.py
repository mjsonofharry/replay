import bisect
import enum
import re


class Action:

    JUMP_PRESS = 'JUMP_PRESS'
    JUMP_RELEASE = 'JUMP_RELEASE'
    ATTACK_PRESS = 'ATTACK_PRESS'
    ATTACK_RELEASE = 'ATTACK_RELEASE'
    SPECIAL_PRESS = 'SPECIAL_PRESS'
    SPECIAL_RELEASE = 'SPECIAL_RELEASE'
    STRONG_PRESS = 'STRONG_PRESS'
    STRONG_RELEASE = 'STRONG_RELEASE'
    STRONG_LEFT_PRESS = 'STRONG_LEFT_PRESS'
    STRONG_LEFT_RELEASE = 'STRONG_LEFT_RELEASE'
    STRONG_RIGHT_PRESS = 'STRONG_RIGHT_PRESS'
    STRONG_RIGHT_RELEASE = 'STRONG_RIGHT_RELEASE'
    STRONG_UP_PRESS = 'STRONG_UP_PRESS'
    STRONG_UP_RELEASE = 'STRONG_UP_RELEASE'
    STRONG_DOWN_PRESS = 'STRONG_DOWN_PRESS'
    STRONG_DOWN_RELEASE = 'STRONG_DOWN_RELEASE'
    DODGE_PRESS = 'DODGE_PRESS'
    DODGE_RELEASE = 'DODGE_RELEASE'
    UP_PRESS = 'UP_PRESS'
    UP_RELEASE = 'UP_RELEASE'
    UP_TAP = 'UP_TAP'
    DOWN_PRESS = 'DOWN_PRESS'
    DOWN_RELEASE = 'DOWN_RELEASE'
    DOWN_TAP = 'DOWN_TAP'
    LEFT_PRESS = 'LEFT_PRESS'
    LEFT_RELEASE = 'LEFT_RELEASE'
    LEFT_TAP = 'LEFT_TAP'
    RIGHT_PRESS = 'RIGHT_PRESS'
    RIGHT_RELEASE = 'RIGHT_RELEASE'
    RIGHT_TAP = 'RIGHT_TAP'
    ANGLES_ENABLED = 'ANGLES_ENABLED'
    ANGLES_DISABLED = 'ANGLES_DISABLED'

    from_token = {
        'J': JUMP_PRESS,
        'j': JUMP_RELEASE,
        'A': ATTACK_PRESS,
        'a': ATTACK_RELEASE,
        'B': SPECIAL_PRESS,
        'b': SPECIAL_RELEASE,
        'C': STRONG_PRESS,
        'c': STRONG_RELEASE,
        'F': STRONG_LEFT_PRESS,
        'f': STRONG_LEFT_RELEASE,
        'G': STRONG_RIGHT_PRESS,
        'g': STRONG_RIGHT_RELEASE,
        'X': STRONG_UP_PRESS,
        'x': STRONG_UP_RELEASE,
        'W': STRONG_DOWN_PRESS,
        'w': STRONG_DOWN_RELEASE,
        'S': DODGE_PRESS,
        's': DODGE_RELEASE,
        'U': UP_PRESS,
        'u': UP_RELEASE,
        'M': UP_TAP,
        'P': UP_TAP,
        'D': DOWN_PRESS,
        'd': DOWN_RELEASE,
        'O': DOWN_TAP,
        'L': LEFT_PRESS,
        'l': LEFT_RELEASE,
        'E': LEFT_TAP,
        'R': RIGHT_PRESS,
        'r': RIGHT_RELEASE,
        'I': RIGHT_TAP,
        'Z': ANGLES_ENABLED,
        'z': ANGLES_DISABLED
    }

    to_boolean = {
        JUMP_PRESS: True,
        JUMP_RELEASE: False,
        ATTACK_PRESS: True,
        ATTACK_RELEASE: False,
        SPECIAL_PRESS: True,
        SPECIAL_RELEASE: False,
        STRONG_PRESS: True,
        STRONG_RELEASE: False,
        STRONG_LEFT_PRESS: True,
        STRONG_LEFT_RELEASE: False,
        STRONG_RIGHT_PRESS: True,
        STRONG_RIGHT_RELEASE: False,
        STRONG_UP_PRESS: True,
        STRONG_UP_RELEASE: False,
        STRONG_DOWN_PRESS: True,
        STRONG_DOWN_RELEASE: False,
        DODGE_PRESS: True,
        DODGE_RELEASE: False,
        UP_PRESS: True,
        UP_RELEASE: False,
        UP_TAP: True,
        DOWN_PRESS: True,
        DOWN_RELEASE: False,
        DOWN_TAP: True,
        LEFT_PRESS: True,
        LEFT_RELEASE: False,
        LEFT_TAP: True,
        RIGHT_PRESS: True,
        RIGHT_RELEASE: False,
        RIGHT_TAP: True,
        ANGLES_ENABLED: True,
        ANGLES_DISABLED: False
    }


class StateKey:

    FRAME = "Frame"
    JUMP = "Jump"
    ATTACK = "Attack"
    SPECIAL = "Special"
    STRONG = "Strong"
    STRONG_UP = "Strong Up"
    STRONG_DOWN = "Strong Down"
    STRONG_LEFT = "Strong Left"
    STRONG_RIGHT = "Strong Right"
    DODGE = "Dodge"
    UP = "Up"
    DOWN = "Down"
    LEFT = "Left"
    RIGHT = "Right"
    TAP_UP = "Tap Up"
    TAP_DOWN = "Tap Down"
    TAP_LEFT = "Tap Left"
    TAP_RIGHT = "Tap Right"
    ANGLES_ENABLED = "Angles Enabled"
    ANGLE = "Angle"

    # TODO: Return a tuple and remove Action.to_boolean
    from_action = {
        Action.JUMP_PRESS: JUMP,
        Action.JUMP_RELEASE: JUMP,
        Action.ATTACK_PRESS: ATTACK,
        Action.ATTACK_RELEASE: ATTACK,
        Action.SPECIAL_PRESS: SPECIAL,
        Action.SPECIAL_RELEASE: SPECIAL,
        Action.STRONG_PRESS: STRONG,
        Action.STRONG_RELEASE: STRONG,
        Action.STRONG_LEFT_PRESS: STRONG_LEFT,
        Action.STRONG_LEFT_RELEASE: STRONG_LEFT,
        Action.STRONG_RIGHT_PRESS: STRONG_RIGHT,
        Action.STRONG_RIGHT_RELEASE: STRONG_RIGHT,
        Action.STRONG_UP_PRESS: STRONG_UP,
        Action.STRONG_UP_RELEASE: STRONG_UP,
        Action.STRONG_DOWN_PRESS: STRONG_DOWN,
        Action.STRONG_DOWN_RELEASE: STRONG_DOWN,
        Action.DODGE_PRESS: DODGE,
        Action.DODGE_RELEASE: DODGE,
        Action.UP_PRESS: UP,
        Action.UP_RELEASE: UP,
        Action.UP_TAP: UP,
        Action.UP_TAP: UP,
        Action.DOWN_PRESS: DOWN,
        Action.DOWN_RELEASE: DOWN,
        Action.DOWN_TAP: DOWN,
        Action.LEFT_PRESS: LEFT,
        Action.LEFT_RELEASE: LEFT,
        Action.LEFT_TAP: LEFT,
        Action.RIGHT_PRESS: RIGHT,
        Action.RIGHT_RELEASE: RIGHT,
        Action.RIGHT_TAP: RIGHT,
        Action.ANGLES_ENABLED: ANGLES_ENABLED,
        Action.ANGLES_DISABLED: ANGLES_ENABLED,
    }


class FrameData:
    
    action_regex = r'(^\d+)|([a-x|z|A-X|Z])|(y[\d| ]{3})'
    action_pattern = re.compile(action_regex)

    @classmethod
    def _convert_token_to_action(cls, t):
        if t[0] == 'y':
            return int(t[1:])
        else:
            return Action.from_token[t]
    
    @classmethod
    def _convert_multiple_tokens_to_actions(cls, ts):
        return [cls._convert_token_to_action(t) for t in ts]

    @classmethod
    def _split_frames_into_tokens(cls, frame_data):
        return [
            [x1 for x1 in FrameData.action_pattern.split(x) if x1] 
            for x in frame_data
        ]

    @classmethod
    def get_action_map(cls, frame_data, raw=False):
        return {
            int(x[0]): (
                x[1:] if raw 
                else cls._convert_multiple_tokens_to_actions(x[1:])
            )
            for x in cls._split_frames_into_tokens(frame_data)
        }

    # TODO: Test this!
    @classmethod
    def get_state_table(cls, frame_data):
        table = []
        state = {
            StateKey.FRAME: None,
            StateKey.JUMP: False,
            StateKey.ATTACK: False,
            StateKey.SPECIAL: False,
            StateKey.STRONG: False,
            StateKey.STRONG_LEFT: False,
            StateKey.STRONG_RIGHT: False,
            StateKey.STRONG_UP: False,
            StateKey.STRONG_DOWN: False,
            StateKey.DODGE: False,
            StateKey.UP: False,
            StateKey.DOWN: False,
            StateKey.LEFT: False,
            StateKey.RIGHT: False,
            StateKey.TAP_UP: False,
            StateKey.TAP_DOWN: False,
            StateKey.TAP_LEFT: False,
            StateKey.TAP_RIGHT: False,
            StateKey.ANGLES_ENABLED: False,
            StateKey.ANGLE: None
        }

        for current_frame in cls._split_frames_into_tokens(frame_data):
            state[StateKey.ANGLE] = None
            state[StateKey.FRAME] = int(current_frame[0])
            tokens = current_frame[1:]
            actions = cls._convert_multiple_tokens_to_actions(tokens)
            for a in actions:
                if isinstance(a, str):
                    state[StateKey.from_action[a]] = Action.to_boolean[a]
                else:
                    state[StateKey.ANGLE] = a
            table.append(dict(state))
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
