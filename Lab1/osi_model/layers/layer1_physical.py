from osi_model.layers import Layer
from osi_model.utils import debug_layer
import socket
import struct
import binascii

class PhysicalLayer(Layer):
    """
    Physical Layer (Layer 1) of the OSI model
    Handles the actual transmission of bits over the network medium
    """
    
    def __init__(self, host='127.0.0.1', port=8000, is_server=False):
        super().__init__("Physical Layer")
        self.host = host
        self.port = port
        self.is_server = is_server
        self.socket = None
        
    def initialize(self):
        """Initialize the physical connection (socket)"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            if self.is_server:
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.socket.bind((self.host, self.port))
                self.socket.listen(1)
                print(f"Server listening on {self.host}:{self.port}")
            else:
                print(f"Client initialized, ready to connect to {self.host}:{self.port}")
                
        except socket.error as e:
            print(f"Socket error: {e}")
            if self.socket:
                self.socket.close()
            self.socket = None
            
    def connect(self):
        """For client: Connect to the server"""
        if not self.is_server and self.socket:
            try:
                self.socket.connect((self.host, self.port))
                print(f"Connected to {self.host}:{self.port}")
                return True
            except socket.error as e:
                print(f"Connection error: {e}")
                return False
        return False
        
    def accept(self):
        """For server: Accept a client connection"""
        if self.is_server and self.socket:
            try:
                client_socket, client_address = self.socket.accept()
                print(f"Accepted connection from {client_address}")
                return client_socket
            except socket.error as e:
                print(f"Accept error: {e}")
                return None
        return None
        
    @debug_layer
    def send_down(self, data, **kwargs):
        """
        Transmits data as a stream of bits:
        1. Adds a frame delimiter for synchronization
        2. Adds the data length for framing
        """
        # Get the target socket
        target_socket = kwargs.get('socket', self.socket)
        
        if not target_socket:
            print("No socket available for transmission")
            return False
            
        try:
            # Convert data to bytes if it's a string
            if isinstance(data, str):
                data = data.encode('utf-8')
                
            # Create a physical frame with:
            # - 4 bytes delimiter (0xAA55AA55)
            # - 4 bytes length
            # - data
            delimiter = struct.pack('!I', 0xAA55AA55)
            length = struct.pack('!I', len(data))
            
            # Send the frame
            target_socket.sendall(delimiter + length + data)
            
            print(f"Transmitted {len(data)} bytes")
            return True
            
        except (socket.error, struct.error) as e:
            print(f"Transmission error: {e}")
            return False
    
    @debug_layer
    def send_up(self, data=None, **kwargs):
        """
        Receives data from the physical medium:
        1. Synchronizes using frame delimiter
        2. Extracts the data based on length field
        
        Returns:
            Received data for data link layer
        """
        # Get the source socket
        source_socket = kwargs.get('socket_to_read', self.socket)
        
        if not source_socket:
            print("No socket available for reception")
            return None
            
        try:
            # Read the 4-byte delimiter
            delimiter_bytes = source_socket.recv(4)
            if not delimiter_bytes or len(delimiter_bytes) < 4:
                return None
                
            delimiter = struct.unpack('!I', delimiter_bytes)[0]
            if delimiter != 0xAA55AA55:
                print(f"Invalid frame delimiter: {hex(delimiter)}")
                return None
                
            # Read the 4-byte length
            length_bytes = source_socket.recv(4)
            if not length_bytes or len(length_bytes) < 4:
                return None
                
            length = struct.unpack('!I', length_bytes)[0]
            
            # Read the actual data
            data = b''
            remaining = length
            while remaining > 0:
                chunk = source_socket.recv(min(4096, remaining))
                if not chunk:
                    break
                data += chunk
                remaining -= len(chunk)
                
            if len(data) < length:
                print(f"Incomplete data received: {len(data)}/{length} bytes")
                return None
                
            # Convert bytes back to string (JSON)
            try:
                return data.decode('utf-8')
            except UnicodeDecodeError:
                # If it's not valid UTF-8, return raw bytes
                return data
                
        except (socket.error, struct.error) as e:
            print(f"Reception error: {e}")
            return None

