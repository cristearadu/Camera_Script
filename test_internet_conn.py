import unittest
import subprocess
import re
import time
from logger import logger

class TestNetworkConnection(unittest.TestCase):

    
    
    def test_internet_conn(self):
        logger.info("Running network connection test")
        received_packs = ""
        self.count = 30
        self.three_quarters = 75/100 * self.count
        self.ip = '8.8.8.8'
        self.command_list = ['ping', '-c', str(self.count), self.ip]
        
        result = self.verify_received_packs()
        assert result, "Failed to connect to the internet. The stream cannot start!"
        
    def verify_received_packs(self):
        """
        TODO
        """
        start_time = time.time()
        
        while True:
            received_packs = self._verify_ping_output(self.command_list)
        
            if received_packs:
                logger.info(f"{received_packs}/{self.count} packets received.")
                
                if received_packs == self.count or \
                    received_packs >= self.three_quarters and received_packs < self.count:
                    
                    logger.info("Network connection obtained. The stream can start")
                    return received_packs
                
                else:
                    logger.error("Failed to connect to the internet. Increase the count variable")
        
            end_time = time.time()
            if end_time - start_time > 300:
                return
    
    def _verify_ping_output(self,command_list):
        """
        TODO
        """
        try:
            output = subprocess.run(command_list, capture_output=True,timeout=60)
            received_packs = self._check_matches(output)
        except subprocess.TimeoutExpired:        
            received_packs = self._check_matches(output)
        return received_packs   
            

    def _check_matches(self, output):
        """
        TODO
        """
        output = output.stdout.decode()
        
        logger.info("Checking matches.")
        pattern = r"(\d+)\s+received"
        
        match = re.search(pattern, output)
        if match:
            try:
                received_packs = int(match.group(1))
            except ValueError:
                raise ValueError(f"Failed to convert {match.group(1)}")
    
            return received_packs
        else:
            return