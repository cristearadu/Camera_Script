import cv2
import imutils
import numpy as np
from time import sleep
from imutils.video.pivideostream import PiVideoStream
from logger import logger

class VideoCamera(object):
    def __init__(self, flip = False):
        logger.info("Starting camera streaming..")
        self._video_streaming = PiVideoStream().start()
        sleep(2)

    def __del__(self):
        logger.info("Stopping camera streaming..")
        self._video_streaming.stop()

    def get_frame(self):
        """
        Function to return the current convertes frames from strings to bytes
        """
        frame = self._video_streaming.read()
        jpeg = cv2.imencode('.jpg', frame)[1].tobytes()
        return jpeg
