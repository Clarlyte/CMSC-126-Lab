import base64

class PresentationLayer:
    def encode(self, data):
        """Encodes data in Base64 format."""
        encoded = base64.b64encode(data.encode()).decode()
        print(f"[Presentation Layer] Encoded Data: {encoded}")
        return encoded

    def decode(self, encoded_data):
        """Decodes Base64 data."""
        decoded = base64.b64decode(encoded_data.encode()).decode()
        print(f"[Presentation Layer] Decoded Data: {decoded}")
        return decoded
