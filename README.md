# 🐼 Panda Chat

A TCP-based chat server that supports multiple clients, broadcasts messages correctly, and implements special commands while ensuring robust error handling. Built with Python socket programming and multithreading, this chat server adds a fun twist with panda-themed features.

The project supports:
- Multi-Client Communication: Handles multiple clients and broadcasts messages correctly.
- Special Commands: Implements commands like @bamboo, @grove, and @leaves.
- Graceful Error Handling: Manages invalid inputs, unexpected disconnections, empty messages, and server shutdowns.
- PModular Code Structure: Designed with clean, maintainable, and well-commented code.
- Panda-Themed Extras: Adds fun elements like ASCII panda art, panda-related messages, and a GUI.

## 📌 Table of Contents
- Prerequisites
- Running the Chat Server
- Connecting Clients
- Demonstrating Functionality
- Challenges Faced
- Assumptions and Limitations
v
## 🔧 Prerequisites
Before running the project, make sure you have Python 3 installed. You can check by running:

```bash
python --version
```

Ensure you have the Python source files (server3.py and client3.py) downloaded.

## 🎯 Running the Chat Server

To run the server, use the command:

```bash
python3 server3.py
```

This proxy server listens on 127.0.0.1 at port 12345 (or another configured port).

## 🌐 Connecting Clients
- Open multiple terminal instances.
- Run:

```bash
python3 client3.py
```

- A user-friendly GUI will open for each client that connects.
- Each client will be prompted to enter a name for their panda (e.g., "FluffyPaws" or "BambooBuddy").
- Once connected, pandas can chat with each other through the GUI, sending and receiving messages in a fun, interactive way.

## 🧪 Demonstrating Functionality
- Multi-Client Broadcast:
    - Connect at least three clients.
    - Send messages from one client and show that all connected clients receive them.

- Special Commands:
    - Type @bamboo to see a random panda-related fact to the user who triggered the command.
    - Use @grove to see a list of all currently connected users’ names.
    - Use @leaves to exit the chat gracefully.

- Graceful Error Handling:
    - Enter an invalid command (e.g., @ww) to see how the server responds.
    - Simulate a lost connection (close a client unexpectedly) to see how the server handles it.
    - Try sending empty messages from a client and verify that the server handles it correctly without broadcasting nothingness.
    - Graceful server shutdown: Press Ctrl+C to stop the server. It should catch the signal and cleanly close all connections instead of   crashing with an error.

## 🔧 Challenges Faced
- Handling Multiple Clients Efficiently: Initially, some client messages weren’t broadcasting correctly due to issues in the threading implementation. It was resolved by refining the message-handling logic and ensuring that each client thread processes messages asynchronously.
- Graceful Disconnection & Error Handling: When a client unexpectedly closed, the server would sometimes crash due to unhandled exceptions. This was fixed by implementing robust error handling and logging to manage unexpected disconnects smoothly.
- Creating the GUI: Initially, the chat client was purely terminal-based, later, it was decided to add a basic GUI using Tkinter to make it more interactive. This required additional effort in handling event loops and threading, but it was a fun challenge and made the chat experience more user-friendly.

## ✨ Assumptions and Limitations
- The server handles only plain text chat; no file transfers or encryption.
- Clients must be properly configured to connect to the correct server address.
- The project ensures stability by handling client disconnections and invalid inputs gracefully.