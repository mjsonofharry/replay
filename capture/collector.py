import cv2
import mss
import numpy as np
import time


class FrameCollector():

    def __init__(self, game_window):
        self._sct = mss.mss()
        self._target = game_window._get_rect(client=True)

    def get_frame(self):
        return self._sct.grab({
            'left': self._target._x0,
            'top': self._target._y0,
            'width': self._target.width,
            'height': self._target.height
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
