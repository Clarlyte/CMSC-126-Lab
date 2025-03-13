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

# Start session
session.start_session()

# User message
message = "Hello, Server!"

# Pass through OSI layers (Encapsulation)
app_data = application.encapsulate(message)
presentation_data = presentation.encode(app_data)
session_data = session.encapsulate(presentation_data)
transport_data = transport.encapsulate(session_data)
network_data = network.encapsulate(transport_data)
datalink_data = datalink.encapsulate(payload=network_data)

# Send data via Physical Layer
physical.send(datalink_data)
print(f"[Client] Final Data Sent: {datalink_data}")