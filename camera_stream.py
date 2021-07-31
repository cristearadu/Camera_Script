import cv2
import imutils
import numpy as np
from time import sleep
from imutils.video.pivideostream import PiVideoStream
from logger import logger

class VideoCamera(object):
    def __init__(self, flip = False):
        logger.info("Starting camera streaming..")
        self.vs = PiVideoStream().start()
        self.flip = flip
        sleep(2)

    def __del__(self):
        logger.info("Stopping camera streaming..")
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()