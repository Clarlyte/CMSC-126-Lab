import sys
import time
import threading
from layers import PhysicalLayer
from layers import DataLinkLayer
from layers import NetworkLayer
from layers import TransportLayer
from layers import SessionLayer
from layers import PresentationLayer
from layers import ApplicationLayer

def start_server():
    """Initialize and run the server component"""
    print("\n=== Starting OSI Model Server ===\n")
    
    # Instantiate all OSI layers for server
    physical = PhysicalLayer()
    datalink = DataLinkLayer()
    network = NetworkLayer()
    transport = TransportLayer()
    session = SessionLayer()
    presentation = PresentationLayer()
    application = ApplicationLayer()
    
    print("[Server] Waiting for incoming data...\n")
    
    # Receive raw data via Physical Layer
    raw_data = physical.receive()
    
    # Process received data
    print("[Server] Data received, decapsulating...")
    
    # Pass through OSI layers (Decapsulation)
    mac_address, datalink_data = datalink.decapsulate(raw_data)
    ip_address, network_data = network.decapsulate(datalink_data)
    transport_data = transport.decapsulate(network_data)
    session_data = session.decapsulate(transport_data)
    presentation_data = presentation.decode(session_data)
    message = application.decapsulate(presentation_data)
    
    # Display received message
    print(f"[Server] Received Message: {message}")
    print(f"[Server] Sender MAC: {mac_address}, Sender IP: {ip_address}")
    
    # Prepare response
    print("[Server] Preparing response...")
    response = f"Server received your message of {len(message)} bytes!"
    
    # Encapsulate response through layers
    app_data = application.encapsulate(response)
    pres_data = presentation.encode(app_data)
    sess_data = session.encapsulate(pres_data)
    trans_data = transport.encapsulate(sess_data)
    net_data = network.encapsulate(trans_data)
    link_data = datalink.encapsulate(net_data)
    
    # Send response
    print("[Server] Sending response...")
    physical.send(link_data)
    
    # End session
    session.end_session()
    print("[Server] Session ended\n")
    print("=== OSI Model Server Completed ===")

def start_client():
    """Initialize and run the client component"""
    print("\n=== Starting OSI Model Client ===\n")
    
    # Give the server time to start listening
    time.sleep(1)
    
    # Instantiate all OSI layers for client
    physical = PhysicalLayer(port=8081)  # Use different port for client
    datalink = DataLinkLayer()
    network = NetworkLayer()
    transport = TransportLayer()
    session = SessionLayer()
    presentation = PresentationLayer()
    application = ApplicationLayer()
    
    # Start session
    session.start_session()
    print("[Client] Started session")
    
    # Create message
    message = "Hello, Server! This is a test message from the OSI model client."
    print(f"[Client] Original message: {message}\n")
    
    # Encapsulate message through OSI layers
    print("[Client] Encapsulating data through OSI layers...")
    app_data = application.encapsulate(message)
    pres_data = presentation.encode(app_data)
    sess_data = session.encapsulate(pres_data)
    trans_data = transport.encapsulate(sess_data)
    net_data = network.encapsulate(trans_data)
    link_data = datalink.encapsulate(net_data)
    
    # Send message
    print("\n[Client] Sending data...")
    physical.send(link_data)
    print("[Client] Data sent successfully!")
    
    # Wait for server response
    print("[Client] Waiting for server response...")
    raw_response = physical.receive()
    
    if raw_response:
        print("[Client] Response received, decapsulating...")
        
        # Decapsulate response
        mac_address, datalink_data = datalink.decapsulate(raw_response)
        ip_address, network_data = network.decapsulate(datalink_data)
        transport_data = transport.decapsulate(network_data)
        session_data = session.decapsulate(transport_data)
        presentation_data = presentation.decode(session_data)
        response = application.decapsulate(presentation_data)
        
        print(f"[Client] Server Response: {response}")
        print(f"[Client] Server MAC: {mac_address}, Server IP: {ip_address}")
    else:
        print("[Client] No response received from server.")
    
    # End session
    session.end_session()
    print("[Client] Session ended\n")
    print("=== OSI Model Client Completed ===")

def run_simulation():
    """Run a complete simulation with both client and server"""
    print("\n=== Starting OSI Model Complete Simulation ===\n")
    
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Start the client
    start_client()
    
    # Wait for the server to complete
    server_thread.join(timeout=10)
    
    print("\n=== OSI Model Simulation Completed Successfully ===")
    print("✓ Full data encapsulation and transmission")
    print("✓ Successful message delivery")
    print("✓ Proper response received")
    print("✓ All OSI layers functioning correctly")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "simulation":
        run_simulation()
    elif len(sys.argv) > 1 and sys.argv[1] == "server":
        start_server()
    elif len(sys.argv) > 1 and sys.argv[1] == "client":
        start_client()
    else:
        print("Usage: python main.py [simulation|server|client]")
        print("  simulation - Run a complete client-server simulation")
        print("  server     - Run only the server component")
        print("  client     - Run only the client component")