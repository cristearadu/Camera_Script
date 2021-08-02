import random
import socket
import netifaces as ni
from ipaddress import ip_address
from logger import logger

class NetworkData():
    
    def __init__(self):
        self._ip = ""
   
    def get_network_data(self):
        """
        Function to get network data. Loopback address not included!
            
            Returns:
                a dictionary containing the interface as a key and the IP as value
        """
        
        ip_interfaces = ni.interfaces()
        interf_dict = {}
        
        for interface in ip_interfaces:
            interface_ip_address = ""
         
            if ni.AF_INET in ni.ifaddresses(interface):
                interface_ip_address = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
            
            if not interface_ip_address or not ip_address(interface_ip_address).is_loopback:
                interf_dict[interface]= interface_ip_address
        
        return interf_dict
    
    def get_private_ip(self):
        """
        Function to get the device's private IP.
        Public IPs and Loopback IP not included.
        """
        
        network_dict = self.get_network_data()
        interface = ""
        reason = ""
        network_dict_final = network_dict.copy()
        
        for interf, ip_addr in network_dict.items():
                try:
                    streamable = True if (ip_address(ip_addr).is_private) else False
                    
                except ValueError:
                    streamable = False
                    reason = "invalid IP"
                
                if not streamable:
                    reason = reason if reason else "public IP"
                    logger.info(f"Removing IP address \'{ip_addr}\' from list, reason: {reason}")
                    network_dict_final.pop(interf)
        
        logger.info(f"Found the following IPs for the server: {network_dict.values()}")
        interface = random.choice(list(network_dict_final))
        self._ip = network_dict_final[interface]
        
        logger.info(f"The IP selected for stream is: \'{self._ip}\'. The inferface is: {interface}")
        
        return self._ip
        

