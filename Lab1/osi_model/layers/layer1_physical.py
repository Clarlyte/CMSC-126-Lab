import socket

class PhysicalLayer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 👈 Fix for Windows socket reuse
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f"[Physical Layer] Server listening on {self.host}:{self.port}")

    def send(self, data):
        """Sends data over a TCP socket"""
        print(f"[Physical Layer] Sending data to {self.host}:{self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(data.encode())

    def receive(self):
        """Receives data over a TCP socket"""
        try:
            conn, addr = self.socket.accept()
            with conn:
                data = conn.recv(1024).decode()
                print(f"[Physical Layer] Received raw data: {data}")
                return data
        except socket.error as e:
            print(f"[Physical Layer] Socket Error: {e}")
            return None
