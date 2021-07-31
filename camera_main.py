import time
import threading
import os
from logger import logger
from flask import Flask, render_template, Response, request
from camera_stream import VideoCamera
import test_camera
from unittest import TextTestRunner, TestLoader

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
    Function to run unit_test for camera
    """
    test_suite =  TestLoader().loadTestsFromModule(test_camera)
    TextTestRunner(verbosity=2).run(test_suite)

def get_private_ip():
    """
    Function to get the device's private IP.
    """
    import random
    import socket
    import netifaces as ni
    from ipaddress import ip_address
    
    ip_interfaces = ni.interfaces()
    ip_list = []
    ip = ""
    reason_invalid = "Invalid IP address"
    reason_loopback = "Loopback IP address"
    reason_public = "Public IP address"
    
    for interface in ip_interfaces:
        if ni.AF_INET in ni.ifaddresses(interface):
            ip_list.append(ni.ifaddresses(interface)[ni.AF_INET][0]['addr'])
    
    for element in ip_list:
        reason_dict = {}
        
        try:
            streamable = True if (ip_address(element).is_private) else False
            
            if ip_address(element).is_loopback:
                streamable = False
    
        except ValueError:
            logger.error(f"Removing IP address, reason: {reason_invalid} {element}")
            streamable = False
            ip_list.remove(element)
        

        if not streamable:
            logger.info(f"Removing IP: {element} from list")
            ip_list.remove(element)
    
        logger.info(f"Found valid and private IP address: {element}")
    
    ip = random.choice(ip_list)
    logger.info(f"The IP selected for stream is: {element}")
    return ip

if __name__ == '__main__':
    run_test()
    private_ip = get_private_ip()
    camera_configuration(app)
    app.run(host=private_ip, debug=False)
    
