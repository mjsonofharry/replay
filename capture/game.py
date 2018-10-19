import functools
import win32gui

CORNER = (-8, -31)
DEFAULT_WIDTH = 976
DEFAULT_HEIGHT = 579
TITLE = 'Rivals of Aether'


class Rect:

    def __init__(self, rect):
        self._x0, self._y0, self._x1, self._y1 = rect
        self.upper_left = (self._x0, self._y0)
        self.lower_right = (self._x1, self._y1)
        self.width = self._x1 - self._x0
        self.height = self._y1 - self._y0
        self.size = (self.width, self.height)

win32gui.GetDesktopWindow
class GameWindow:

    def __init__(self):
        self._hwnd = win32gui.FindWindow(None, TITLE)

    def _get_rect(self, client=False):
        if not client:
            return Rect(win32gui.GetWindowRect(self._hwnd))
        else:
            return Rect(win32gui.GetClientRect(self._hwnd))

    def focus(self):
        win32gui.SetForegroundWindow(self._hwnd)

    def translate(self, position):
        rect = self._get_rect()
        win32gui.MoveWindow(
            self._hwnd,
            *position, rect.width, rect.height,
            True)

    def move_to_corner(self):
        rect = self._get_rect()
        x = rect._x0
        y = rect._y0
        dx, dy = win32gui.ScreenToClient(self._hwnd, (0, 0))
        self.translate((x + dx, y + dy))

    def scale(self, size):
        rect = self._get_rect()
        win32gui.MoveWindow(
            self._hwnd,
            rect._x0, rect._y0, *size,
            True)
