import win32gui

TITLE = 'Rivals of Aether'
DEFAULT_WIDTH = 976
DEFAULT_HEIGHT = 579


class Rect:

    def __init__(self, rect):
        self._x0, self._y0, self._x1, self._y1 = rect
        self.upper_left = (self._x0, self._y0)
        self.lower_right = (self._x1, self._y1)
        self.width = self._x1 - self._x0
        self.height = self._y1 - self._y0
        self.size = (self.width, self.height)


class Game:

    def __init__(self):
        self._hwnd = win32gui.FindWindow(None, TITLE)

    def get_rect(self):
        return Rect(win32gui.GetWindowRect(self._hwnd))

    def focus(self):
        win32gui.SetForegroundWindow(self._hwnd)

    def translate(self, position=None):
        if not position:
            position = (0, 0)
        rect = self.get_rect()
        win32gui.MoveWindow(
            self._hwnd,
            *position, rect.width, rect.height,
            True)

    def scale(self, size=None):
        if not size:
            size = (DEFAULT_WIDTH, DEFAULT_HEIGHT)
        rect = self.get_rect()
        win32gui.MoveWindow(
            self._hwnd,
            rect._x0, rect._y0, *size,
            True)
