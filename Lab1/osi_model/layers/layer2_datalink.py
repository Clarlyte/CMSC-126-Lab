import uuid

class DataLinkLayer:
    def __init__(self):
        self.mac_address = self.get_mac_address()

   def get_mac_address(self):
        """Fetches the MAC address dynamically and reverses it."""
        # Generate the MAC address dynamically
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 48, 8)])
        
        # Reverse the MAC address string
        reversed_mac = ':'.join(mac.split(':')[::-1])  # Split by ':' and reverse the parts
        
        print(f"[Data Link Layer] Assigned MAC Address: {reversed_mac}")
        return reversed_mac

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
