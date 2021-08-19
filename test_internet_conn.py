import unittest
from logger import logger
from network_data import NetworkData
class TestNetworkConnection(unittest.TestCase):

    
    def test_got_ip(self):
        """
        Test used to check if the device has a valid IP for streaming. 
        """
        timeout=180
        network_data = NetworkData()
        private_ip = network_data.get_private_ip(timeout=timeout)
        assert private_ip, "Failed to find an IP for streaming"    
    
    def test_internet_conn(self):
        """
        Test to check internet connection through pinging
        """
        network_data = NetworkData()
        
        logger.info("Running network connection test")
        received_packs = ""
        count = 30
        ip = '8.8.8.8'
        command_list = ['ping', '-c', str(count), ip]
        
        result = network_data.verify_received_packs(command_list=command_list,
                                                    ip=ip, count=count,
                                                    received_packs=received_packs)

        assert result > 0 , "Failed to connect to the internet. The stream cannot start!"
        logger.info("Network connection obtained. The stream can start")
        
    