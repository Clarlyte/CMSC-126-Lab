from . import Layer
from ..utils import debug_layer, generate_id
import json
import time

class SessionLayer(Layer):
    """
    Session Layer (Layer 5) of the OSI model
    Manages connection states and synchronization
    """
    
    def __init__(self):
        super().__init__("Session Layer")
        self.sessions = {}  # Store active sessions
        
    @debug_layer
    def send_down(self, data, **kwargs):
        """
        Establishes and maintains session information:
        1. Creates a session if none exists
        2. Adds session control information to the data
        
        Returns:
            Data with session information for transport layer
        """
        # Get or create session ID
        session_id = kwargs.get('session_id')
        if not session_id:
            session_id = generate_id()
            
        command = kwargs.get('command', 'DATA')
        
        # Create a new session if it's an OPEN command or if session doesn't exist
        if command == 'OPEN' or session_id not in self.sessions:
            self.sessions[session_id] = {
                'created_at': time.time(),
                'last_activity': time.time(),
                'status': 'OPEN'
            }
        else:
            # Update existing session
            self.sessions[session_id]['last_activity'] = time.time()
            if command == 'CLOSE':
                self.sessions[session_id]['status'] = 'CLOSED'
            
        # Create session wrapper
        session_data = {
            'session_id': session_id,
            'command': command,
            'timestamp': time.time(),
            'data': data
        }
        
        return json.dumps(session_data)
    
    @debug_layer
    def send_up(self, data, **kwargs):
        """
        Processes session information:
        1. Validates the session
        2. Updates session state
        3. Extracts the actual data
        
        Returns:
            Processed data for presentation layer and session metadata
        """
        try:
            # Parse the session data
            session_data = json.loads(data)
            
            session_id = session_data.get('session_id')
            command = session_data.get('command', 'DATA')
            
            # Process according to command
            if command == 'OPEN':
                # Create new session if it doesn't exist
                if session_id not in self.sessions:
                    self.sessions[session_id] = {
                        'created_at': time.time(),
                        'last_activity': time.time(),
                        'status': 'OPEN'
                    }
            elif command == 'CLOSE':
                # Mark session as closed if it exists
                if session_id in self.sessions:
                    self.sessions[session_id]['status'] = 'CLOSED'
            
            # Update session activity if it exists
            if session_id in self.sessions:
                self.sessions[session_id]['last_activity'] = time.time()
            
            # Pass session_id to upper layers
            kwargs['session_id'] = session_id
            return session_data.get('data')
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error in Session Layer: {e}")
            return data