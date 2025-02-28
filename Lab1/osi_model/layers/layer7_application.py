from . import Layer
from ..utils import debug_layer, generate_id
import json

class ApplicationLayer(Layer):
    """
    Application Layer (Layer 7) of the OSI model
    Implements an HTTP-like request-response communication
    """
    
    def __init__(self):
        super().__init__("Application Layer")
        
    @debug_layer
    def send_down(self, data, **kwargs):
        """
        Encapsulates application data in an HTTP-like format
            
        Returns:
            HTTP-like formatted message ready for the presentation layer
        """
        # Default values
        method = kwargs.get('method', 'GET')
        path = kwargs.get('path', '/')
        headers = kwargs.get('headers', {})
        
        # Add request ID if not present
        if 'request_id' not in headers:
            headers['request_id'] = generate_id()
            
        # Create HTTP-like request
        http_message = {
            'method': method,
            'path': path,
            'headers': headers,
            'body': data
        }
        
        # Serialize to JSON-like format
        return json.dumps(http_message)
    
    @debug_layer
    def send_up(self, data, **kwargs):
        """
        Processes incoming HTTP-like messages
        
        Returns:
            Extracted body content and metadata
        """
        try:
            # Parse the HTTP-like message
            http_message = json.loads(data)
            
            # Extract useful information
            result = {
                'body': http_message['body'],
                'request_id': http_message['headers'].get('request_id'),
                'method': http_message.get('method'),
                'path': http_message.get('path')
            }
            
            return result
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error in Application Layer: {e}")
            return {'body': data, 'error': str(e)}