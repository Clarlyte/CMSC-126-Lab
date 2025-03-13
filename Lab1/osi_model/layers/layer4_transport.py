import base64

class TransportLayer:
    def encapsulate(self, payload):
        """Encodes the message in base64 to simulate transport encryption."""
        encoded_payload = base64.b64encode(payload.encode()).decode()
        print(f"[Transport Layer] Encapsulated Transport Data: {encoded_payload}")
        return encoded_payload

    def decapsulate(self, payload):
        """Decodes the message from base64."""
        decoded_payload = base64.b64decode(payload.encode()).decode()
        print(f"[Transport Layer] Decapsulated Data: {decoded_payload}")
        return decoded_payload
