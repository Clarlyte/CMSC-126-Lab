from . import Layer
from ..utils import debug_layer
import base64
import json
import zlib

class PresentationLayer(Layer):
    """
    Presentation Layer (Layer 6) of the OSI model
    Handles encryption, compression, and encoding
    """
    
    def __init__(self):
        super().__init__("Presentation Layer")
        
    @debug_layer
    def send_down(self, data, **kwargs):
        """
        Prepares data by:
        1. Compressing it using zlib
        2. Encoding it to ensure safe transmission
        
        Returns:
            Processed data ready for the session layer
        """
        encoding_type = kwargs.get('encoding', 'base64')
        compression = kwargs.get('compression', True)
        
        # Step 1: Convert to bytes if it's a string
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        # Step 2: Compress data if requested
        if compression:
            data = zlib.compress(data)
            
        # Step 3: Encode data for transmission
        if encoding_type == 'base64':
            data = base64.b64encode(data)
        
        # Create a metadata wrapper
        presentation_data = {
            'encoding': encoding_type,
            'compression': compression,
            'data': data.decode('latin-1')  # Store binary data as Latin-1 string for JSON compatibility
        }
        
        return json.dumps(presentation_data)
    
    @debug_layer
    def send_up(self, data, **kwargs):
        """
        Reverses the presentation layer operations:
        1. Decodes the data based on the specified encoding
        2. Decompresses if it was compressed
        
        Returns:
            Processed data for the application layer
        """
        try:
            # Parse the presentation layer wrapper
            presentation_data = json.loads(data)
            
            # Get processing information
            encoding_type = presentation_data.get('encoding', 'base64')
            compression = presentation_data.get('compression', True)
            
            # Get the actual data and convert back to bytes
            processed_data = presentation_data['data'].encode('latin-1')
            
            # Decode according to the specified encoding
            if encoding_type == 'base64':
                processed_data = base64.b64decode(processed_data)
            
            # Decompress if it was compressed
            if compression:
                processed_data = zlib.decompress(processed_data)
            
            # Convert back to string if it's UTF-8 decodable
            try:
                return processed_data.decode('utf-8')
            except UnicodeDecodeError:
                return processed_data  # Return as bytes if not a valid UTF-8
                
        except (json.JSONDecodeError, KeyError, zlib.error, base64.Error) as e:
            print(f"Error in Presentation Layer: {e}")
            return data  # Return original data on error