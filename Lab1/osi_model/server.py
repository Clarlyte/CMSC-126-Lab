from osi_model.layers.layer1_physical import PhysicalLayer
from osi_model.layers.layer2_datalink import DataLinkLayer
from osi_model.layers.layer3_network import NetworkLayer
from osi_model.layers.layer4_transport import TransportLayer
from osi_model.layers.layer5_session import SessionLayer
from osi_model.layers.layer6_presentation import PresentationLayer
from osi_model.layers.layer7_application import ApplicationLayer

class OSIServer:
    """Server implementation using the OSI model"""
    
    def __init__(self, host='127.0.0.1', port=8000):
        # Initialize all layers
        self.physical = PhysicalLayer(host, port, is_server=True)
        self.datalink = DataLinkLayer()
        self.network = NetworkLayer()
        self.transport = TransportLayer()
        self.session = SessionLayer()
        self.presentation = PresentationLayer()
        self.application = ApplicationLayer()
        
        # Client connection tracking
        self.client_socket = None
        self.running = False
        
    def start(self):
        """Start the server and listen for connections"""
        self.physical.initialize()
        self.running = True
        
        print("Server started. Waiting for connections...")
        
        while self.running:
            # Accept client connection
            self.client_socket = self.physical.accept()
            if not self.client_socket:
                continue
                
            # Handle client communication
            self.handle_client()
                
    def handle_client(self):
        """Handle communication with a connected client"""
        try:
            print(f"Handling client communication")
            
            while self.running and self.client_socket:
                try:
                    # Receive message through all OSI layers
                    # Layer 1: Physical (receive bits)
                    physical_data = self.physical.send_up(None, socket_to_read=self.client_socket)
                    if not physical_data:
                        break
                    
                    # Layer 2: Data Link (process frame)
                    datalink_data = self.datalink.send_up(physical_data)
                    if not datalink_data:
                        break
                    
                    # Layer 3: Network (process packet)
                    network_data = self.network.send_up(datalink_data)
                    if not network_data:
                        break
                    
                    # Layer 4: Transport (process segments)
                    transport_data = self.transport.send_up(network_data)
                    if not transport_data:
                        break
                    
                    # Layer 5: Session (process session)
                    session_data = self.session.send_up(transport_data)
                    if not session_data:
                        break
                    
                    # Layer 6: Presentation (process encoding/compression)
                    presentation_data = self.presentation.send_up(session_data)
                    if not presentation_data:
                        break
                    
                    # Layer 7: Application (process HTTP-like message)
                    application_data = self.application.send_up(presentation_data)
                    
                    print(f"Received message: {application_data}")
                    
                    # Process the request and generate a response
                    response = self.process_request(application_data)
                    
                    # Send response back through all layers
                    # Layer 7: Application
                    app_data = self.application.send_down(response, method='RESPONSE', path='/')
                    
                    # Layer 6: Presentation
                    pres_data = self.presentation.send_down(app_data)
                    
                    # Layer 5: Session
                    # Get session ID from received message
                    session_id = application_data.get('request_id')
                    sess_data = self.session.send_down(pres_data, session_id=session_id, command='DATA')
                    
                    # Layer 4: Transport
                    trans_data = self.transport.send_down(sess_data)
                    
                    # Layer 3: Network
                    # Use the source IP as the destination for the response
                    net_data = self.network.send_down(trans_data)
                    
                    # Layer 2: Data Link
                    dl_data = self.datalink.send_down(net_data)
                    
                    # Layer 1: Physical
                    self.physical.send_down(dl_data, socket=self.client_socket)
                    
                except Exception as e:
                    print(f"Error processing message: {e}")
                    break
                
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            if self.client_socket:
                try:
                    self.client_socket.close()
                except:
                    pass
                self.client_socket = None
            
    def process_request(self, request_data):
        """Process client request and generate response"""
        try:
            # Extract request info
            body = request_data.get('body', '')
            method = request_data.get('method', 'GET')
            path = request_data.get('path', '/')
            
            # Simple echo server functionality
            response = {
                "status": "OK",
                "message": f"Received {method} request for {path}",
                "echo": body
            }
            
            return response
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Error processing request: {str(e)}"
            }
        
    def stop(self):
        """Stop the server"""
        self.running = False
        if self.physical.socket:
            self.physical.socket.close()
            self.physical.socket = None

if __name__ == "__main__":
    server = OSIServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop()