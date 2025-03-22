# OSI Model Implementation

This project demonstrates a practical implementation of the OSI (Open Systems Interconnection) model, showing how data travels through the seven layers of network communication.

## Overview

The OSI Model is a conceptual framework that standardizes network communication into seven distinct layers. This implementation demonstrates the encapsulation and decapsulation process as data flows through each layer, providing a visual and programmatic representation of how network communication works.

## Setup Instructions

1. Make sure you have Python 3.7+ installed on your system
2. Clone this repository
3. No external dependencies needed - the implementation uses Python's standard libraries

## Running the Application

You can run the application in several ways:

### Full Simulation (Client and Server)

```bash
python main.py simulation
```

This will start both the server and client components in a full simulation, showing the complete data flow through all OSI layers.

### Server Only

```bash
python main.py server
```

Starts just the server component, which will listen for incoming connections.

### Client Only

```bash
python main.py client
```

Starts just the client component, which will attempt to connect to a running server.

## Example Output

When running the full simulation, you'll see the data flowing through each layer:

1. Client encapsulates a message through all seven layers
2. Message is transmitted via the Physical Layer
3. Server receives and decapsulates the message through all layers
4. Server prepares a response and sends it back
5. Client receives and processes the response

The application will show detailed information about each step, including:
- MAC addresses of communicating devices
- IP addresses used for routing
- Session management
- Data encoding/decoding
- Message encapsulation/decapsulation

  ![image](https://github.com/user-attachments/assets/d296c57b-c01d-424d-82dd-994dee1ab6f4)

## Project Structure

The project is organized by OSI layers:

- `main.py`: Main application entry point
- `layers/`:
  - `__init__.py`: Layer imports
  - `layer1_physical.py`: Physical Layer implementation (raw data transmission)
  - `layer2_datalink.py`: Data Link Layer implementation (MAC addressing)
  - `layer3_network.py`: Network Layer implementation (IP addressing)
  - `layer4_transport.py`: Transport Layer implementation (reliable delivery)
  - `layer5_session.py`: Session Layer implementation (session management)
  - `layer6_presentation.py`: Presentation Layer implementation (data encoding)
  - `layer7_application.py`: Application Layer implementation (message formatting)

## OSI Layers Implementation Details

### 1. Physical Layer
- Handles the actual data transmission using TCP sockets
- Simulates the physical medium of network communication
- Manages the raw binary data transfer between devices

### 2. Data Link Layer
- Manages MAC addressing for device identification
- Handles frames that contain network layer data
- Provides node-to-node data transfer

### 3. Network Layer
- Implements IP addressing for logical addressing
- Manages routing of data packets between networks
- Handles fragmentation and reassembly of data

### 4. Transport Layer
- Ensures reliable data transmission using encoding
- Manages end-to-end communication
- Handles flow control and error recovery

### 5. Session Layer
- Establishes, maintains, and terminates sessions
- Manages communication session synchronization
- Controls dialogue between devices

### 6. Presentation Layer
- Transforms data into a format usable by the application layer
- Handles encoding and encryption of data
- Manages data compression and translation

### 7. Application Layer
- Provides network services to end-user applications
- Formats messages for human readability
- Represents the interface to the user

## Notes

- This implementation is designed for educational purposes
- The MAC address and IP address are dynamically determined from your machine
- All communication happens locally (localhost) with different ports for client and server
- Base64 encoding is used to simulate data transformation in transport and presentation layers
