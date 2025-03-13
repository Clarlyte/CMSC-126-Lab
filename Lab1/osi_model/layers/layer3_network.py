import socket

class NetworkLayer:
    def __init__(self):
        self.ip_address = self.get_ip_address()
        print(f"[Network Layer] Assigned IP Address: {self.ip_address}")

    def get_ip_address(self):
        """Gets the local machine's IP address dynamically."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def encapsulate(self, payload):
        """Adds IP header."""
        packet = f"{self.ip_address}|{payload}"
        print(f"[Network Layer] Encapsulated Packet: {packet}")
        return packet

    def decapsulate(self, packet):
        """Extracts IP header."""
        ip, payload = packet.split("|", 1)
        print(f"[Network Layer] Decapsulated - Source IP: {ip}, Data: {payload}")
        return ip, payload
