import time
import threading
import os
import unittest
import test_camera
from logger import logger
from flask import Flask, render_template, Response, request
from camera_stream import VideoCamera
from unittest import TextTestRunner, TestLoader
from network_data import NetworkData

app = Flask(__name__)

def camera_configuration(app):
    """
    Function that creates the camera and streams live video
    """
    pi_camera = VideoCamera()

    @app.route('/')
    def index():
        """
        Home html page for web streaming page 
        """
        logger.info("Opening web site.. ")
        return render_template('index.html')

    def gen(camera):
        """
        Function to get camera frame
        """
        # get camera frame
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    @app.route('/video_feed')
    def video_feed():
        """
        Function that returns the videofeed for streaming
        """
        return Response(gen(pi_camera),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

def run_tests():
    """
    Function to run unit_test for camera. First verification in our process
    """
    classes_to_run = [test_camera]
    suite_list = []
    for test_class in classes_to_run:
        test_suite =  TestLoader().loadTestsFromModule(test_class)
        suite_list.append(test_suite)
    
    big_suite = unittest.TestSuite(suite_list)
    runner = TextTestRunner(verbosity=2).run(big_suite)
    return runner.wasSuccessful()

if __name__ == '__main__':
    assert run_tests(), "The tests have failed. The stream cannot start"
    network_data = NetworkData()
    private_ip = network_data.get_private_ip()

    camera_configuration(app)
    app.run(host=private_ip, debug=False, port=5000)
