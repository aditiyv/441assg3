import socket
import threading
import random
import logging
import signal
import sys

# Configure logging
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Panda-themed constants
PANDA_EMOJIS = ["🐼", "🍃", "ʕ¯ᴥ¯ʔ.zZ", "ฅʕ•ᴥ•`ʔ", "ʕ •ᴥ•ʔ", "ʕ¯㉨¯ʔฅ", "ʕづ•ﻌ•ʔづ♡", "ʕ๑◕ᴥ◕ʔ"]
PANDA_FACTS = [
    "Baby pandas are born pink and weigh only about 100 grams!",
    "A group of pandas is called an embarrassment!",
    "Pandas can swim and are excellent tree climbers!",
    "There are only about 1800 giant pandas left in the wild!",
    "Pandas rock a chic black-and-white ensemble 24/7. Who needs a wardrobe when you're naturally fashion-forward?",
    "With up to 14 hours of sleep per day, pandas have perfected the art of napping!"
]

# List to keep track of connected clients and their names
clients = []  # Stores the connected client sockets
client_names = []  # Stores the names of connected clients

# Flag to control the server loop
server_running = True  # Indicates whether the server is running

# Function to broadcast messages to all clients
def broadcast(message, sender=None):
    for client in clients:  # Iterate through all connected clients
        if client != sender:  # Skip the sender if provided
            try:
                client.send(message.encode('utf-8'))  # Send the message to the client
            except:
                if client in clients:  # Handle client disconnection
                    index = clients.index(client)  # Get the index of the client
                    clients.remove(client)  # Remove the client from the list
                    client.close()  # Close the client socket
                    name = client_names[index]  # Get the name of the disconnected client
                    client_names.remove(name)  # Remove the name from the list
                    broadcast(f"🐼 {name} has left the chat.")  # Notify others about the disconnection
                    logging.info(f"{name} has left the chat (connection error).")  # Log the disconnection

# Function to handle client connections
def handle_client(client):
    while True:  # Keep listening for messages from the client
        try:
            message = client.recv(1024).decode('utf-8')  # Receive a message from the client
            if not message:  # If the message is empty break the loop
                break

            if message.startswith('@'):  # Check if the message is a command
                handle_command(client, message)  # Handle the command
            else:
                panda_flair = random.choice(PANDA_EMOJIS)  # Add a random panda emoji to the message
                broadcast(f"{panda_flair} {client_names[clients.index(client)]}: {message}")  # Broadcast the message
                logging.info(f"{client_names[clients.index(client)]} sent a message: {message}")  # Log the message
        except:
            break  # Exit the loop if an error occurs

    if client in clients:  # Handle client disconnection
        index = clients.index(client)  # Get the index of the client
        clients.remove(client)  # Remove the client from the list
        client.close()  # Close the client socket
        name = client_names[index]  # Get the name of the disconnected client
        client_names.remove(name)  # Remove the name from the list
        broadcast(f"🐼 {name} has left the chat.")  # Notify others about the disconnection
        logging.info(f"{name} has left the chat.")  # Log the disconnection

# Function to handle special commands
def handle_command(client, command):
    if command == '@bamboo':
        fact = random.choice(PANDA_FACTS)  # Select a random panda fact
        client.send(f"🐼 Panda Fact: {fact}".encode('utf-8'))  # Send the fact to the client
        logging.info(f"Sent a panda fact to {client_names[clients.index(client)]}.")  # Log the action
    elif command == '@grove':
        client.send(f"🐼 Connected Pandas: {', '.join(client_names)}".encode('utf-8'))  # Send the list of connected clients
        logging.info(f"Sent connected pandas list to {client_names[clients.index(client)]}.")  # Log the action
    elif command == '@leaves':
        if client in clients:  # Ensure the client is still connected
            index = clients.index(client)  # Get the index of the client
            clients.remove(client)  # Remove the client from the list
            client.close()  # Close the client socket
            name = client_names[index]  # Get the name of the client
            client_names.remove(name)  # Remove the name from the list
            broadcast(f"🐼 {name} has left the chat.")  # Notify others about the disconnection
            logging.info(f"{name} has left the chat (using @leaves command).")  # Log the disconnection
    else:
        client.send("🐼 Unknown command.".encode('utf-8'))  # Notify the client about the unknown command
        logging.warning(f"{client_names[clients.index(client)]} sent an unknown command: {command}")  # Log the warning

# Function to shut down the server
def shutdown_server(signal=None, frame=None):
    global server_running
    logging.info("Shutting down the server...")  # Log the shutdown
    print("Shutting down the server...")  # Print the shutdown message

    for client in clients:
        client.close()  # Close each client socket
    clients.clear()  # Clear the list of clients
    client_names.clear()  # Clear the list of client names

    server_running = False  # Set the server running flag to False
    sys.exit(0)  # Exit the program

# Main server function
def start_server():
    global server_running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object for the server
    server.bind(('127.0.0.1', 5555))  # Bind the server to localhost and port 5555
    server.listen()  # Start listening for incoming connections

    signal.signal(signal.SIGINT, shutdown_server)  # Register the signal handler for graceful shutdown

    logging.info("🐼 Panda Chat Server is running...")  # Log that the server is running
    print("🐼 Panda Chat Server is running...")  # Print that the server is running

    while server_running:  # Main server loop
        try:
            client, address = server.accept()  # Accept a new client connection
            logging.info(f"Connected with {str(address)}")  # Log the connected clients address
            print(f"🐼 Connected with {str(address)}")  # Print the connected clients address

            client.send("🐼 Enter your panda name: ".encode('utf-8'))  # Prompt the client to enter their panda name
            name = client.recv(1024).decode('utf-8')  # Receive the clients panda name
            client_names.append(name)  # Add the client's name to the list of client names
            clients.append(client)  # Add the client socket to the list of clients

            broadcast(f"🐼 {name} has joined the chat!")  # Notify all clients that a new client has joined
            client.send("🐼 Welcome to the Panda Chat Room!".encode('utf-8'))  # Send a welcome message to the new client
            logging.info(f"{name} has joined the chat.")  # Log that the client has joined the chat

            thread = threading.Thread(target=handle_client, args=(client,))  # Start a new thread to handle the client
            thread.start()  # Start the thread
        except:
            if server_running:  # Check if the server is still running
                logging.error("An error occurred while accepting a connection.")  # Log an error if something goes wrong

    server.close()  # Close the server socket when the server stops running
    logging.info("🐼 Server has been shut down.")  # Log that the server has been shut down
    print("🐼 Server has been shut down.")  # Print that the server has been shut down


if __name__ == "__main__":
    start_server()