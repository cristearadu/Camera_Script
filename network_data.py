import random
import socket
import netifaces as ni
import time
import subprocess
import re
from ipaddress import ip_address
from logger import logger


class NetworkData():
    
    def get_private_ip(self, timeout=None):
        """
        Function to get the device's private IP.

            Parameters:
                timeout (int): timeout in seconds. Default value is 0
            
            Return:
                String containing the streaming IP.
        """
        start_time = time.time()
        ip = self._timeout_function(self._parse_ip, timeout)
        
        if not ip:
            logger.error("Loopback address does not count as a streamable address")
            return
        
        return ip
    
    def _get_network_data(self):
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


    def _parse_ip(self):
        """
        Private function to parse ip from the dictionary returned by _get_network_data().

            Returns:
                a random IP from a random interface 'eth0' or 'wlan0' if exists or None
        """

        network_dict = self._get_network_data()
        interface = ""
        network_dict_final = self._check_streamable_ips(network_dict)
        
        logger.info(f"Found the following IPs for the server: {network_dict_final.values()}")
    
        if network_dict_final:
            interface = random.choice(list(network_dict_final))
            ip = network_dict_final[interface]
            logger.info(f"The IP selected for stream is: \'{ip}\'. The inferface is: {interface}")
            return network_dict_final[interface]
        else:
            return
    
    
    def _check_streamable_ips(self, network_dict):
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
    
    def verify_received_packs(self, command_list, ip, count, received_packs, timeout=300):
        """
        Private function to verify received packets from pinging
        
        Parameters:
            command_list (list): commands that are put inside a list
            ip ():
            count ():
            received_packs():
            timeout (int): Timeout value
        Returns:
            received_packs (int): number of received packets from pining a source. 0 returned for not receiving any packets
        """
        received_packs = self._timeout_function(self._verify_ping_output, timeout, command_list, ip, count)
        logger.info(f"{received_packs}/{count} packets received.")

        return received_packs

    def _verify_ping_output(self, command_list, ip, count):
        """
        Private function to run a subprocess command and process the output of pinging
        
        Parameters:
            command_list
            ip
            count
        
        Returns:
            received_packs (int): number of received packets from pining a source
        """
        pass_rate = 70

        try:
            logger.info(f"Pinging {ip} for {count} times")
            output = subprocess.run(command_list, capture_output=True,
					 timeout=60)
            received_packs = self._check_matches(output)
        except subprocess.TimeoutExpired:        
            received_packs = self._check_matches(output)

        if not received_packs:
            received_packs = 0

        current_rate = 100 * received_packs / count
        if current_rate >= pass_rate:
            logger.info("Good connection. The stream can start!")
            return received_packs
        
        elif current_rate <= pass_rate and current_rate != 0:
            logger.error("Connection is not stable. The stream might not start. Trying again")
            return 
         

    def _check_matches(self, output):
        """
        Private function to parse the number of matches for received packets
        
        Parameters:
            output (bits): Received response from ping, bits object
        
        Returns:
            received_packs (int): number of received packets from pining a source
        """
        output = output.stdout.decode()
        pattern = r"(\d+)\s+received"
        
        match = re.search(pattern, output)
        received_packs = None
        
        if match:
            try:
                received_packs = int(match.group(1))
            except ValueError:
                raise ValueError(f"Failed to convert {match.group(1)}")
        
        if received_packs:
            return received_packs
       	return

    
    @staticmethod
    def _timeout_function(running_function, timeout=30, *args):
        """
        Static function used to give a timeout to any function.
        
        Parameters:
            running_function (function): function given to an object to be called
            timeout (int): value for timeout. 
        Returns:
            specified object, either a string containing an IP, either an int
        """
        start_time = time.time()
        
        while True:
            output = running_function(*args) if args else running_function()
            if output:
                return output

            end_time = time.time()
            if end_time - start_time > timeout:
                return
