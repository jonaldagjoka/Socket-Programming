# Socket Programming

A collection of three Python-based chat server implementations with progressive complexity, from basic client-server communication to broadcast messaging and private chat functionality.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Testing](#testing)
- [Project Structure](#project-structure)

## About

This project implements three distinct chat systems, each building upon the previous one:

1. **Basic Chat System** - Simple one-to-one client-server communication
2. **Broadcast Chat System** - Multi-client chat with message broadcasting
3. **Private Chat System** - Direct messaging between specific users

All systems implement Base64 encryption for message transmission and persistent logging of chat history.

## Features

### Common Features
- Base64 message encryption/decryption
- Timestamp-based message logging
- Multi-threaded server architecture
- Graceful connection handling

### System-Specific Features

**Basic Chat (`server.py` / `client.py`)**
- Single client-server communication
- Message acknowledgment system
- Simple chat logging

**Broadcast Chat (`broadcast_server.py` / `broadcast_client.py`)**
- Multiple simultaneous clients
- Real-time message broadcasting
- User join/leave notifications
- Active user count tracking

**Private Chat (`private_server.py`)**
- Direct messaging: `@username message`
- Broadcast to all: `@all message`
- Username uniqueness enforcement
- Online user list
- System notifications

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd chat-systems

# No additional installation required
```

## Usage

### Basic Chat System

**Terminal 1 - Start Server:**
```bash
python3 server.py
```

**Terminal 2 - Start Client:**
```bash
python3 client.py
```

### Broadcast Chat System

**Terminal 1 - Start Server:**
```bash
python3 broadcast_server.py
```

**Terminal 2, 3, 4... - Start Clients:**
```bash
python3 broadcast_client.py
```

### Private Chat System

**Terminal 1 - Start Server:**
```bash
python3 private_server.py
```

**Terminal 2+ - Start Clients:**
```bash
# Client will be prompted for username
# Send messages using:
@username Your private message here
@all Message to everyone
```

### Configuration

Default settings (modifiable in source files):
- **HOST**: `0.0.0.0` (server) / `localhost` (client)
- **PORT**: `5000`
- **Log Files**: 
  - `chat_log.txt` (basic)
  - `broadcast_chat_log.txt` (broadcast)
  - `private_chat_log.txt` (private)

## Architecture

### Server Architecture

All servers follow a similar pattern:

```
Server Socket (listening)
    │
    ├──> Client Connection 1 ──> Thread 1
    ├──> Client Connection 2 ──> Thread 2
    └──> Client Connection N ──> Thread N
```

### Message Flow

```
Client Input
    │
    ├──> Base64 Encode
    │
    ├──> Socket Send
    │
    └──> Server Receive
            │
            ├──> Base64 Decode
            │
            ├──> Process & Log
            │
            └──> Response/Broadcast
```

### Threading Model

- **Daemon Threads**: Client handlers run as daemon threads
- **Thread Safety**: Broadcast/Private servers use locks for shared data
- **Concurrent Access**: Multiple clients handled simultaneously

## Testing

A comprehensive test suite is included in `test_chat_systems.py`.

**Run all tests:**
```bash
python3 test_chat_systems.py
```

**Test Categories:**
- Unit Tests - Encryption/Decryption
- Integration Tests - Server functionality
- Performance Tests - Speed benchmarks
- Logging Tests - File operations

**Expected Output:**
```
======================================================================
DUKE EKZEKUTUAR TESTET PËR SISTEMET E CHAT-IT
======================================================================

test_encrypt_simple_message ... ok
test_decrypt_simple_message ... ok
...
----------------------------------------------------------------------
Ran XX tests in X.XXXs

OK
```

## Project Structure

```
.
├── server.py                  # Basic chat server
├── client.py                  # Basic chat client
├── broadcast_server.py        # Broadcast chat server
├── broadcast_client.py        # Broadcast chat client
├── private_server.py          # Private messaging server
├── test_chat_systems.py       # Comprehensive test suite
├── chat_log.txt              # Basic chat logs
├── broadcast_chat_log.txt    # Broadcast chat logs
├── private_chat_log.txt      # Private chat logs
└── README.md                 # This file
```

## Implementation Details

### Encryption

Messages are encrypted using Base64 encoding:
```python
def encrypt(msg):
    return base64.b64encode(msg.encode()).decode()

def decrypt(msg):
    return base64.b64decode(msg.encode()).decode()
```

### Logging Format

```
[YYYY-MM-DD HH:MM:SS] Username: Message
[2025-12-21 16:30:03] Jona: Hello World
```

### Private Message Format

```
@username Your message      # Send to specific user
@all Broadcast message      # Send to all users
```

## Notes

- Base64 is used for demonstration; not cryptographically secure
- All timestamps use server time
- Maximum message size: 1024 bytes
- Servers must be started before clients
- Use `exit` command to disconnect gracefully

## Author

Jonalda Gjoka
