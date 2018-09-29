import cv2
import mss
import numpy as np
import time
import win32gui


TITLE = 'Rivals of Aether'
DEFAULT_WIDTH = 976
DEFAULT_HEIGHT = 579


class Rect:
    def __init__(self, rect):
        self.x0, self.y0, self.x1, self.y1 = rect
        self.upper_left = (self.x0, self.y0)
        self.lower_right = (self.x1, self.y1)
        self.width = self.x1 - self.x0
        self.height = self.y1 - self.y0
        self.size = (self.width, self.height)


class WindowHandler:
    def __init__(self):
        self.__hwnd = win32gui.FindWindow(None, TITLE)

    def get_rect(self):
        return Rect(win32gui.GetWindowRect(self.__hwnd))

    def focus(self):
        win32gui.SetForegroundWindow(self.__hwnd)

    def translate(self, position=None):
        if not position:
            position = (0, 0)
        rect = self.get_rect()
        win32gui.MoveWindow(
            self.__hwnd,
            *position, rect.width, rect.height,
            True)

    def scale(self, size=None):
        if not size:
            size = (DEFAULT_WIDTH, DEFAULT_HEIGHT)
        rect = self.get_rect()
        win32gui.MoveWindow(
            self.__hwnd,
            rect.x0, rect.y0, *size,
            True)


class FrameCollector():
    def __init__(self, window_rect):
        self.__sct = mss.mss()
        self.__target = window_rect

    def get_frame(self):
        return self.__sct.grab({
            'left': self.__target.x0,
            'top': self.__target.y0,
            'width': self.__target.width,
            'height': self.__target.height
        })
    
    def get_frame_loop(self, duration, fps=60):
        delta_threshold = 1/fps
        time_start = time.time()
        time_previous = time_start
        while True:
            time_now = time.time()
            delta = time_now - time_previous
            if delta >= delta_threshold:
                time_previous = time_now
                yield self.get_frame()
            if time_now - time_start >= duration:
                break

    def display_frame(self):
        cv2.imshow('Frame', np.array(self.get_frame()))
        key = cv2.waitKey(0) & 0xFF
        if key == ord("q"):
            cv2.destroyAllWindows()
