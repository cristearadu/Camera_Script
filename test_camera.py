import unittest
import os.path
from picamera import PiCamera
from time import sleep
from datetime import datetime
from logger import logger 
OUTPUT_FILE = "/home/pi/Desktop/"

class TestCamera(unittest.TestCase):
    def test_camera(self):
        logger.info("Running camera test")
        
        date_time = datetime.now()
        date_time = date_time.strftime("%Y-%b-%w-%X")
        
        logger.info("Starting camera test.")
        camera = PiCamera()
        
        #alpha represents the transparence level: 0-255
        assert camera.start_preview(alpha=0), "Failed to load the camera. Check if it's connected."
        logger.info("Starting camera preview..")
        sleep(2) 
        file_name = f"{OUTPUT_FILE}{date_time}_camera_test.jpg"
        camera.capture(file_name), "Failed to save the image. The camera might be broken."
        
        camera.stop_preview()
        logger.info("Closing the camera")
        camera.close()

        logger.info(f"Searching for file \'{file_name}\'")
        assert os.path.isfile(file_name), f"Failed to find the file at the expected location \'{file_name}\'."
        logger.info(f"Successfully found the file \'{file_name}\'")
        assert os.path.getsize(file_name), f"The file either has been corrupted or the camera is broken. The file exists, but the senzor did not send any file."
        
        sleep(2)
