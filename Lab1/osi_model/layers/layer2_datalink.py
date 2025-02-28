from . import Layer
from ..utils import debug_layer, generate_id, calculate_checksum
import json
import struct
import random

class DataLinkLayer(Layer):
    """
    Data Link Layer (Layer 2) of the OSI model
    Implements MAC addressing and frame transmission
    """
    
    def __init__(self, mac_address=None):
        super().__init__("Data Link Layer")
        # Generate a simulated MAC address if none provided
        self.mac_address = mac_address or self._generate_mac()
        
    def _generate_mac(self):
        """Generate a random MAC address string"""
        return ':'.join([f'{random.randint(0, 255):02x}' for _ in range(6)])
        
    @debug_layer
    def send_down(self, data, **kwargs):
        """
        Creates data link frames:
        1. Adds source and destination MAC addresses
        2. Implements frame check sequence for error detection
        
        Returns:
            Framed data for physical layer
        """
        dest_mac = kwargs.get('destination_mac', 'FF:FF:FF:FF:FF:FF')  # Default to broadcast
        
        # Create ethernet-like frame
        frame = {
            'source_mac': self.mac_address,
            'destination_mac': dest_mac,
            'ethertype': kwargs.get('ethertype', 0x0800),  # Default to IPv4
            'data': data,
            'fcs': calculate_checksum(data)  # Frame Check Sequence
        }
        
        return json.dumps(frame)
    
    @debug_layer
    def send_up(self, data, **kwargs):
        """
        Processes data link frames:
        1. Verifies frame integrity using FCS
        2. Checks if frame is for this host
        3. Extracts network layer data
        
        Returns:
            Processed data for network layer
        """
        try:
            # Parse ethernet frame
            frame = json.loads(data)
            
            # Verify frame check sequence
            calculated_fcs = calculate_checksum(frame['data'])
            if calculated_fcs != frame['fcs']:
                print(f"Frame error: FCS mismatch")
                return None
                
            # Check if frame is for this host (or broadcast)
            if frame['destination_mac'] != self.mac_address and frame['destination_mac'] != 'FF:FF:FF:FF:FF:FF':
                print(f"Frame not for this host, ignoring")
                return None
            
            # Pass ethertype to upper layers
            kwargs['ethertype'] = frame.get('ethertype')
            
            return frame['data']
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error in Data Link Layer: {e}")
            return data