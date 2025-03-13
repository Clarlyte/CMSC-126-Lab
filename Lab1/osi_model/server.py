from layers import PhysicalLayer
from layers import DataLinkLayer
from layers import NetworkLayer
from layers import TransportLayer
from layers import SessionLayer
from layers import PresentationLayer
from layers import ApplicationLayer

# Instantiate all OSI layers
physical = PhysicalLayer()
datalink = DataLinkLayer()
network = NetworkLayer()
transport = TransportLayer()
session = SessionLayer()
presentation = PresentationLayer()
application = ApplicationLayer()

# Receive raw data via Physical Layer
raw_data = physical.receive()

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

# End session
session.end_session()