import random
import socket
import netifaces as ni
from ipaddress import ip_address
from logger import logger

class NetworkData():
    
    def __init__(self):
        self._ip = ""
        self.reason_dict = {"reason_invalid": "Invalid IP address",
                            "reason_loopback": "Loopback IP address",
                            "reason_public": "Public IP address"}

   
    def get_ip_or_network_address(self, ip_list_flag=False, network_address_flag=False):
        """
        Function to return an interface list or a network address dictionary
        
            Parameters:
                ip_list_flag - boolean: True to return a list of available IPs
                network_address_flag - boolean: True to return a dictionary of interfaces with
                                                 their network addresses 
                
            Returns:
                interface_list: list with available interfaces
                interf_dict: dictionary with networks of the available interfaces
        """
        
        ip_interfaces = ni.interfaces()
        ip_list = []
        interf_dict = {}
        
        for interface in ip_interfaces:
            interface_ip_address = ""
         
            if ni.AF_INET in ni.ifaddresses(interface):
                interface_ip_address = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
                ip_list.append(interface_ip_address)
            
            if network_address_flag:
                if not interface_ip_address or not ip_address(interface_ip_address).is_loopback:
                    import pdb; pdb.set_trace()
                    interf_dict[interface]= interface_ip_address
    
        if ip_list_flag:
            return ip_list
        
        elif network_address_flag:
            return interf_dict
            
    def add_static_ip(self, eth=False, wlan=False):
        """
        TODO
        """
        interf_dict = self.get_ip_or_network_address(network_address_flag=True)
        
        logger.info("Verifying if any connection has been made up so far")
        aplha_list = self.get_ip_or_network_address(ip_list_flag=True)
        ip_list = [elem for elem in aplha_list if not ip_address(elem).is_loopback]
            
        if not ip_list:
            logger.info("Not a single connection is UP. Connect your raspberry to a Wifi or Eth Cable!")
            exit()
        elif ip_list:
            for interf, ip in interf_dict.items():
                logger.info(f"Found interface \'{interf}\' with IP \'{ip}\'")    
                if ip:
                    a = int(ip_address(ip))
                    a = struct.unpack('!I', socket.inet_pton(socket.AF_INET, ip))[0]
                    a = struct.unpack('!I', socket.inet_aton('192.0.43.10'))[0]  # IPv4 only
                    import pdb; pdb.set_trace()
        
    def get_private_ip(self):
        """
        Function to get the device's private IP.
        Public IPs and Loopback IP not included.
        """
        
        ip_list = self.get_ip_or_network_address(ip_list_flag=True)
        
        for element in ip_list:
            reason = ""
            print(element)
            try:
                streamable = True if (ip_address(element).is_private) else False
                
                if ip_address(element).is_loopback:
                    streamable = False
                    reason = self.reason_dict['reason_loopback']
        
            except ValueError:
                streamable = False
                reason = self.reason_dict['reason_invalid']
            

            if not streamable:
                reason = reason if reason else self.reason_dict['reason_public']
                logger.info(f"Removing IP address \'{element}\' from list, reason: {reason}")
                ip_list.remove(element)
        
        logger.info(f"Found the following IPs for the server: {ip_list}")
        self._ip = random.choice(ip_list)
        logger.info(f"The IP selected for stream is: {self._ip}")
        return self._ip

