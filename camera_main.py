import time
import threading
import os
import test_camera
from logger import logger
from flask import Flask, render_template, Response, request
from camera_stream import VideoCamera
from unittest import TextTestRunner, TestLoader
from network_data import NetworkData

# App Globals (do not edit)
app = Flask(__name__)

def camera_configuration(app):
    """
    Function that creates and streams through the camera
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
        #get camera frame
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

def run_test_camera():
    """
    Function to run unit_test for camera. First verification in our process
    """
    test_suite =  TestLoader().loadTestsFromModule(test_camera)
    TextTestRunner(verbosity=2).run(test_suite)


if __name__ == '__main__':
    
    run_test_camera()
    network_data = NetworkData()
    private_ip = network_data.get_private_ip()
    camera_configuration(app)
    app.run(host=private_ip, debug=False, port=5000)
