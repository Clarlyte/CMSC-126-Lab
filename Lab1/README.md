# OSI Model Implementation

This project implements a practical demonstration of the OSI (Open Systems Interconnection) model, showing how data travels through the seven layers of network communication.

## Setup Instructions

1. Make sure you have Python 3.7+ installed on your system
2. Clone this repository
3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install socket hashlib
   ```

## Running the Application

1. First, start the server:
   ```bash
   python -m osi_model.server
   ```
   The server will start listening on localhost (127.0.0.1) port 8000.
![image](https://github.com/user-attachments/assets/258ce9af-e660-4691-8cde-08906e65f8dc)

3. In a separate terminal, run the client:
   ```bash
   python -m osi_model.client
   ```
![image](https://github.com/user-attachments/assets/363b9f32-b4b8-432e-bcc5-7ee59e526487)

   The client will connect to the server and send a test message.

## Project Structure

## Overview of the OSI Model

The OSI Model is a conceptual framework that standardizes the functions of a telecommunication or computing system into seven abstraction layers:

### 1. Physical Layer
- Transmits raw bits over physical medium
- Examples: Ethernet cables, radio waves
- In this implementation: Uses TCP sockets to simulate physical transmission

### 2. Data Link Layer
- Handles node-to-node data delivery
- Examples: Ethernet, Wi-Fi
- In this implementation: Manages frames and MAC addressing

### 3. Network Layer
- Handles routing and forwarding
- Examples: IP, ICMP
- In this implementation: Simulates IP addressing and routing

### 4. Transport Layer
- Ensures reliable end-to-end data delivery
- Examples: TCP, UDP
- In this implementation: Handles packet sequencing and error checking

### 5. Session Layer
- Manages sessions between applications
- Examples: NetBIOS, RPC
- In this implementation: Tracks communication sessions with unique IDs

### 6. Presentation Layer
- Handles data formatting, encryption, and compression
- Examples: SSL/TLS, JPEG, ASCII
- In this implementation: Handles data compression and encoding

### 7. Application Layer
- Provides network services directly to end-users
- Examples: HTTP, FTP, SMTP, DNS
- In this implementation: Handles HTTP-like requests and responses











