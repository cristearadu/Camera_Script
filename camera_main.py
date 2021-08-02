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
    #todo
    """
    pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

    @app.route('/')
    def index():
        return render_template('index.html')

    def gen(camera):
        #get camera frame
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    @app.route('/video_feed')
    def video_feed():
        return Response(gen(pi_camera),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

def run_test():
    """
    Function to run unit_test for camera. First verification in our process
    """
    test_suite =  TestLoader().loadTestsFromModule(test_camera)
    TextTestRunner(verbosity=2).run(test_suite)


if __name__ == '__main__':
    
    #run_test()
    network_data = NetworkData()
    private_ip = network_data.get_private_ip()
    camera_configuration(app)
    import pdb; pdb.set_trace()
    app.run(host=private_ip, debug=False)
