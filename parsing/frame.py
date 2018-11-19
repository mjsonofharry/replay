import bisect
import enum
import re


class InputEvent:

    INVALID = 'INVALID'
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

    _token_to_input_event = {
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

    @classmethod
    def from_token(cls, t):
        result = cls._token_to_input_event.get(t)
        if not result:
            raise ValueError('Encountered unknown token: "{}"'.format(t))
        return result


class ActionType:

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

    _input_event_to_action_type = {
        InputEvent.JUMP_PRESS: (True, JUMP),
        InputEvent.JUMP_RELEASE: (False, JUMP),
        InputEvent.ATTACK_PRESS: (True, ATTACK),
        InputEvent.ATTACK_RELEASE: (False, ATTACK),
        InputEvent.SPECIAL_PRESS: (True, SPECIAL),
        InputEvent.SPECIAL_RELEASE: (False, SPECIAL),
        InputEvent.STRONG_PRESS: (True, STRONG),
        InputEvent.STRONG_RELEASE: (False, STRONG),
        InputEvent.STRONG_LEFT_PRESS: (True, STRONG_LEFT),
        InputEvent.STRONG_LEFT_RELEASE: (False, STRONG_LEFT),
        InputEvent.STRONG_RIGHT_PRESS: (True, STRONG_RIGHT),
        InputEvent.STRONG_RIGHT_RELEASE: (False, STRONG_RIGHT),
        InputEvent.STRONG_UP_PRESS: (True, STRONG_UP),
        InputEvent.STRONG_UP_RELEASE: (False, STRONG_UP),
        InputEvent.STRONG_DOWN_PRESS: (True, STRONG_DOWN),
        InputEvent.STRONG_DOWN_RELEASE: (False, STRONG_DOWN),
        InputEvent.DODGE_PRESS: (True, DODGE),
        InputEvent.DODGE_RELEASE: (False, DODGE),
        InputEvent.UP_PRESS: (True, UP),
        InputEvent.UP_RELEASE: (False, UP),
        InputEvent.UP_TAP: (True, TAP_UP),
        InputEvent.DOWN_PRESS: (True, DOWN),
        InputEvent.DOWN_RELEASE: (False, DOWN),
        InputEvent.DOWN_TAP: (True, TAP_DOWN),
        InputEvent.LEFT_PRESS: (True, LEFT),
        InputEvent.LEFT_RELEASE: (False, LEFT),
        InputEvent.LEFT_TAP: (True, TAP_LEFT),
        InputEvent.RIGHT_PRESS: (True, RIGHT),
        InputEvent.RIGHT_RELEASE: (False, RIGHT),
        InputEvent.RIGHT_TAP: (True, TAP_RIGHT),
        InputEvent.ANGLES_ENABLED: (True, ANGLES_ENABLED),
        InputEvent.ANGLES_DISABLED: (False, ANGLES_ENABLED)
    }

    @classmethod
    def from_input_event(cls, a):
        if isinstance(a, str):
            result = cls._input_event_to_action_type[a]
            if not result:
                raise ValueError('Unknown input event: "{}"'.format(a))
            return result
        if isinstance(a, int):
            return (a, cls.ANGLE)
        raise ValueError('Input event must be int or str but instead found {}'.format(type(a)))


class FrameData:
    
    action_regex = r'(^\d+)|([a-x|z|A-X|Z])|(y[\d| ]{3})'
    action_pattern = re.compile(action_regex)

    @classmethod
    def _convert_token_to_action(cls, t):
        if t[0] == 'y':
            return int(t[1:])
        else:
            return InputEvent.from_token(t)
    
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

    @classmethod
    def get_state_table(cls, frame_data):
        table = []
        state = {
            ActionType.FRAME: None,
            ActionType.JUMP: False,
            ActionType.ATTACK: False,
            ActionType.SPECIAL: False,
            ActionType.STRONG: False,
            ActionType.STRONG_LEFT: False,
            ActionType.STRONG_RIGHT: False,
            ActionType.STRONG_UP: False,
            ActionType.STRONG_DOWN: False,
            ActionType.DODGE: False,
            ActionType.UP: False,
            ActionType.DOWN: False,
            ActionType.LEFT: False,
            ActionType.RIGHT: False,
            ActionType.TAP_UP: False,
            ActionType.TAP_DOWN: False,
            ActionType.TAP_LEFT: False,
            ActionType.TAP_RIGHT: False,
            ActionType.ANGLES_ENABLED: False,
            ActionType.ANGLE: None
        }

        for current_frame in cls._split_frames_into_tokens(frame_data):
            state.update({
                ActionType.FRAME: int(current_frame[0]),
                ActionType.TAP_UP: False,
                ActionType.TAP_DOWN: False,
                ActionType.TAP_LEFT: False,
                ActionType.TAP_RIGHT: False,
                ActionType.ANGLE: None
            })
            actions = cls._convert_multiple_tokens_to_actions(current_frame[1:])
            for a in actions:
                v, at = ActionType.from_input_event(a)
                state[at] = v
            table.append(dict(state))
        return table

    @staticmethod
    def snap_frame(lookup_table, n):
        keys = list(lookup_table.keys())
        i = bisect.bisect_right(keys, n)
        if i:
            return keys[i-1]
        raise ValueError('Frame snapping failed. Do not snap negative values.')
    
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
