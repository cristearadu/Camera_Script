import random
import socket
import netifaces as ni
from ipaddress import ip_address
from logger import logger

class NetworkData():
    
    def __init__(self):
        self._ip = ""
            
        
    def get_private_ip(self):
        """
        Function to get the device's private IP.
        """
        
        ip_interfaces = ni.interfaces()
        ip_list = []
        ip = ""
        reason_dict = {"reason_invalid": "Invalid IP address",
                       "reason_loopback": "Loopback IP address",
                       "reason_public": "Public IP address"}

        for interface in ip_interfaces:
            if ni.AF_INET in ni.ifaddresses(interface):
                ip_list.append(ni.ifaddresses(interface)[ni.AF_INET][0]['addr'])
        
        for element in ip_list:
            reason = ""
            
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
        
        ip = self._ip = random.choice(ip_list)
        logger.info(f"The IP selected for stream is: {element}")
        return ip

