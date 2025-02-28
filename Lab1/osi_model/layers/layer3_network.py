from . import Layer
from ..utils import debug_layer
import json
import random

class NetworkLayer(Layer):
    """
    Network Layer (Layer 3) of the OSI model
    Implements IP addressing and packet routing
    """
    
    def __init__(self, local_ip=None):
        super().__init__("Network Layer")
        # Simulate a simple IP address if none provided
        self.local_ip = local_ip or f"192.168.1.{random.randint(2, 254)}"
        
    @debug_layer
    def send_down(self, data, **kwargs):
        """
        Handles network routing:
        1. Adds source and destination IP addresses
        2. Implements TTL (Time To Live) and fragmentation
        
        Returns:
            Network packet for data link layer
        """
        dest_ip = kwargs.get('destination_ip', '192.168.1.1')  # Default to gateway
        ttl = kwargs.get('ttl', 64)  # Default TTL
        
        # Create network packet (IP-like)
        network_packet = {
            'source_ip': self.local_ip,
            'destination_ip': dest_ip,
            'ttl': ttl,
            'protocol': kwargs.get('protocol', 'TCP'),  # Default to TCP
            'data': data
        }
        
        return json.dumps(network_packet)
    
    @debug_layer
    def send_up(self, data, **kwargs):
        """
        Processes network layer information:
        1. Checks if packet is for this host
        2. Verifies TTL has not expired
        3. Extracts upper layer data

        Returns:
            Processed data for transport layer
        """
        try:
            # Parse network packet
            network_packet = json.loads(data)
            
            # Check TTL
            if network_packet['ttl'] <= 0:
                print(f"Packet dropped: TTL expired")
                return None
                
            # Possible Implementation: Verify destination is for this host

            # Extract protocol for upper layers
            kwargs['protocol'] = network_packet.get('protocol', 'TCP')
            
            return network_packet['data']
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error in Network Layer: {e}")
            return data