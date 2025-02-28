from osi_model.layers.layer1_physical import PhysicalLayer
from osi_model.layers.layer2_datalink import DataLinkLayer
from osi_model.layers.layer3_network import NetworkLayer
from osi_model.layers.layer4_transport import TransportLayer
from osi_model.layers.layer5_session import SessionLayer
from osi_model.layers.layer6_presentation import PresentationLayer
from osi_model.layers.layer7_application import ApplicationLayer
import socket

class OSIClient:
    """Client implementation using the OSI model"""
    
    def __init__(self, server_host='127.0.0.1', server_port=8000):
        # Initialize all layers
        self.physical = PhysicalLayer(server_host, server_port, is_server=False)
        self.datalink = DataLinkLayer()
        self.network = NetworkLayer()
        self.transport = TransportLayer()
        self.session = SessionLayer()
        self.presentation = PresentationLayer()
        self.application = ApplicationLayer()
        
        # Session tracking
        self.current_session_id = None
        
    def connect(self):
        """Initialize and connect to the server"""
        self.physical.initialize()
        return self.physical.connect()
        
    def send_message(self, message, method='GET', path='/'):
        """Send a message through all OSI layers"""
        if not self.physical.socket:
            print("Not connected to server")
            return False
        
        try:
            # Generate new session if needed
            if not self.current_session_id:
                self.current_session_id = None  # Will be auto-generated
                command = 'OPEN'
            else:
                command = 'DATA'
                
            # Layer 7: Application
            app_data = self.application.send_down(message, method=method, path=path)
            
            # Layer 6: Presentation
            pres_data = self.presentation.send_down(app_data)
            
            # Layer 5: Session
            sess_data = self.session.send_down(pres_data, session_id=self.current_session_id, command=command)
            
            # Layer 4: Transport
            trans_data = self.transport.send_down(sess_data)
            
            # Layer 3: Network
            net_data = self.network.send_down(trans_data, destination_ip='192.168.1.1')
            
            # Layer 2: Data Link
            dl_data = self.datalink.send_down(net_data)
            
            # Layer 1: Physical
            result = self.physical.send_down(dl_data)
            
            return result
            
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
            
    def receive_message(self, timeout=30):
        """Receive and process a message through all OSI layers"""
        try:
            # Set socket timeout
            self.physical.socket.settimeout(timeout)
            
            # Layer 1: Physical (receive bits)
            physical_data = self.physical.send_up(None, socket_to_read=self.physical.socket)
            if not physical_data:
                print("No data received from server")
                return None
                
            # Reset socket timeout
            self.physical.socket.settimeout(None)
            
            # Layer 2: Data Link (process frame)
            datalink_data = self.datalink.send_up(physical_data)
            if not datalink_data:
                return None
                
            # Layer 3: Network (process packet)
            network_data = self.network.send_up(datalink_data)
            if not network_data:
                return None
                
            # Layer 4: Transport (process segments)
            transport_data = self.transport.send_up(network_data)
            if not transport_data:
                return None
                
            # Layer 5: Session (process session)
            session_data = self.session.send_up(transport_data)
            if not session_data:
                return None
                
            # Layer 6: Presentation (process encoding/compression)
            presentation_data = self.presentation.send_up(session_data)
            if not presentation_data:
                return None
                
            # Layer 7: Application (process HTTP-like message)
            application_data = self.application.send_up(presentation_data)
            
            return application_data
            
        except socket.timeout:
            print("Timeout waiting for server response")
            return None
        except Exception as e:
            print(f"Error receiving message: {e}")
            return None
        finally:
            # Reset socket timeout
            self.physical.socket.settimeout(None)
            
    def close(self):
        """Close the connection properly"""
        try:
            if self.current_session_id:
                # Send proper session closure
                app_data = self.application.send_down("Closing connection")
                pres_data = self.presentation.send_down(app_data)
                sess_data = self.session.send_down(pres_data, session_id=self.current_session_id, command='CLOSE')
                trans_data = self.transport.send_down(sess_data)
                net_data = self.network.send_down(trans_data)
                dl_data = self.datalink.send_down(net_data)
                self.physical.send_down(dl_data)
                
            # Close socket
            if self.physical.socket:
                self.physical.socket.close()
                self.physical.socket = None
                
        except Exception as e:
            print(f"Error closing connection: {e}")
        finally:
            self.current_session_id = None

if __name__ == "__main__":
    client = OSIClient()
    try:
        print("Connecting to server...")
        if client.connect():
            message = {
                "body": "Hello OSI World!",
                "type": "test_message"
            }
            print(f"Sending message: {message}")
            if client.send_message(message):
                response = client.receive_message()
                print(f"Received response: {response}")
    except KeyboardInterrupt:
        print("\nClosing client...")
    finally:
        client.close()
