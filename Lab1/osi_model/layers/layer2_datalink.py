import uuid

class DataLinkLayer:
    def __init__(self):
        self.mac_address = self.get_mac_address()

    def get_mac_address(self):
        """Fetches the MAC address dynamically."""
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xFF) for elements in range(0, 2 * 6, 8)])
        print(f"[Data Link Layer] Assigned MAC Address: {mac}")
        return mac

    def encapsulate(self, payload):
        """Adds MAC address to the data before sending."""
        framed_data = f"{self.mac_address}|{payload}"  # Correctly using the payload here
        print(f"[Data Link Layer] Encapsulated Frame: {framed_data}")
        return framed_data

    def decapsulate(self, framed_data):
        """Extracts MAC address from received data."""
        mac, data = framed_data.split("|", 1)
        print(f"[Data Link Layer] Decapsulated Data: {data} (Sender MAC: {mac})")
        return mac, data
