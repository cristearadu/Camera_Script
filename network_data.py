import random
import netifaces as ni
from ipaddress import ip_address
from logger import logger


class NetworkData():
    
    def get_private_ip(self):
        """
        Function to get the device's private IP.
            
        Returns:
            String containing the streaming IP.
        """
        ip = self.parse_ip()
        
        if not ip:
            logger.error("Loopback address does not count as a streamable address")
            return
        
        return ip
    
    
    def parse_ip(self):
        """
        Function to parse ip from the dictionary returned by __get_network_data().

        Returns:
            a random IP from a random interface 'eth0' or 'wlan0' if exists or None
        """

        network_dict = self.__get_network_data()
        interface = ""
        network_dict_final = self.__check_streamable_ips(network_dict)
        
        logger.info(f"Found the following IPs for the server: {network_dict_final.values()}")
    
        if network_dict_final:
            interface = random.choice(list(network_dict_final))
            ip = network_dict_final[interface]
            logger.info(f"The IP selected for stream is: \'{ip}\'. The inferface is: {interface}")
            return network_dict_final[interface]
        else:
            return
    
    def __get_network_data(self):
        """
        Private function to get network data. Loopback address not included!
            
        Returns:
            a dictionary containing the interface as a key and the IP as value
        """
    
        ip_interfaces = ni.interfaces()
        interf_dict = {}
        
        for interface in ip_interfaces:
            interface_ip_address = ""

            if ni.AF_INET in ni.ifaddresses(interface):
                interface_ip_address = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
            interf_dict[interface]= interface_ip_address
        
        return interf_dict
    
    
    def __check_streamable_ips(self, network_dict):
        """
        Private function that parses the streamable IP network dictionary
        
        Parameters:
            network_dict (dictionary) - original dictionary with IPs and their interfaces
        
        Returns:
            a final dictionary containing the IPs and the interfaces available for streaming
        """
        reason = ""
        network_dict_final = network_dict.copy()
        network_dict_final.pop('lo')
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

        return network_dict_final
