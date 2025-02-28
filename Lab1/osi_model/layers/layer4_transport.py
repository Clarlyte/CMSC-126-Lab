from . import Layer
from ..utils import debug_layer, calculate_checksum
import json
import random

class TransportLayer(Layer):
    """
    Transport Layer (Layer 4) of the OSI model
    Implements TCP-like packet sequencing and error handling
    """
    
    def __init__(self):
        super().__init__("Transport Layer")
        self.sequence_counter = random.randint(1000, 9999)
        self.received_packets = {}  # To store received packets for reordering
        
    @debug_layer
    def send_down(self, data, **kwargs):
        """
        Implements reliable data transport:
        1. Breaks data into segments if needed
        2. Adds sequence numbers
        3. Calculates checksums for error detection
            
        Returns:
            Segmented data with transport headers for network layer
        """
        protocol = kwargs.get('protocol', 'TCP')
        segment_size = kwargs.get('segment_size', 1024)  # Maximum bytes per segment
        
        # Determine if we need to segment the data
        segments = []
        if len(data) > segment_size:
            # Segment the data
            for i in range(0, len(data), segment_size):
                segments.append(data[i:i+segment_size])
        else:
            segments = [data]
            
        # Create transport packets
        transport_packets = []
        for segment in segments:
            # Increment sequence number
            self.sequence_counter += 1
            
            # Create packet with TCP-like header
            packet = {
                'protocol': protocol,
                'sequence': self.sequence_counter,
                'checksum': calculate_checksum(segment),
                'data': segment
            }
            
            transport_packets.append(packet)
            
        # Return serialized packets
        return json.dumps(transport_packets)
    
    @debug_layer
    def send_up(self, data, **kwargs):
        """
        Reassembles segmented data:
        1. Verifies checksums
        2. Reorders packets based on sequence numbers
        3. Handles any missing packets or errors
        
        Returns:
            Reassembled data for session layer
        """
        try:
            # Parse transport packets
            transport_packets = json.loads(data)
            
            # Process packets
            valid_packets = []
            for packet in transport_packets:
                # Verify checksum
                calculated_checksum = calculate_checksum(packet['data'])
                if calculated_checksum != packet['checksum']:
                    print(f"Checksum error for packet {packet['sequence']}")
                    continue
                    
                # Store valid packet
                valid_packets.append(packet)
                
            # Sort packets by sequence number
            valid_packets.sort(key=lambda p: p['sequence'])
            
            # Reassemble data
            reassembled_data = ''.join(packet['data'] for packet in valid_packets)
            
            return reassembled_data
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error in Transport Layer: {e}")
            return data
