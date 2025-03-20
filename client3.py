import socket
import threading
import tkinter as tk
from tkinter import messagebox
import platform

# Client configuration
HOST = '127.0.0.1'
PORT = 5555

# Panda ASCII Art
PANDA_ART = """
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⢀⠀⣠⡀⢐⠀⡔⢨⠋⠀⠀⢸
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡀⠉⠁⠙⠁⠈⠀⠉⠈⠁⣀⣴⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⢶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠛⠻⠟⣟⣋⣡⣬⣉⣛⠉⠉⠉⢻⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⢠⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢄⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⣿⣿⣿⣿⣿
⣿⣿⡏⠁⠀⠈⢛⡋⣾⣿⣿⠟⠋⠉⠙⠻⣿⣿⣿⡟⠁⠀⠀⢻⣿⣿⣿⣿
⣿⣿⣧⠀⣴⣾⣿⠀⣿⣿⡇⠀⠀⠠⠄⠀⣸⣿⣿⣧⡀⠐⠂⠀⠹⣿⣿⣿
⣿⣿⡏⣼⣿⣿⣿⡄⣿⣿⣿⣄⣀⣀⣀⣴⣿⣿⣄⣤⣿⣶⣶⣾⠇⣿⣿⣿
⠋⠉⠃⢿⣿⣿⣿⠃⠀⠈⠉⠛⠛⠛⠛⢿⣿⣿⣿⣿⣿⣿⠿⠋⠘⢿⣿⣿
⣄⣀⣀⣈⣛⣛⣛⣀⣀⣀⣀⣀⣀⣀⡀⠸⣛⣛⣛⣋⣉⣀⣀⣀⣀⣾⣿⣿
"""

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')  # Receive a message from the server
            if message:
                chat_window.config(state=tk.NORMAL)  # Enable the chat window to insert the message
                chat_window.insert(tk.END, message + "\n")  # Insert the received message into the chat window
                chat_window.config(state=tk.DISABLED)  # Disable the chat window to make it read-only
                chat_window.yview(tk.END)  # Auto-scroll the chat window to the bottom
            else:
                break  # Break the loop if no message is received (connection might be closed)
        except ConnectionAbortedError:
            break  # Handle the case where the connection is aborted
        except:
            print("Error receiving messages.")  # Handle any other exceptions, close the client, and exit the loop
            client.close()
            break

# Function to send messages to the server
def send_message(event=None):
    message = entry_box.get()  # Get the message from the input box
    if message:  # Check if the message is not empty
        try:
            if message == '@leaves':  # Check if the user wants to leave the chat
                client.send(message.encode('utf-8'))  # Send the leave command to the server
                client.close()  # Close the client socket
                root.quit()  # Quit the GUI application
            else:
                client.send(message.encode('utf-8'))  # Send the message to the server
                entry_box.delete(0, tk.END)  # Clear the input box after sending the message
        except:
            messagebox.showerror("Connection Error", "Unable to send message. Server may be disconnected.")
            client.close()
            root.quit()
    else:
        messagebox.showwarning("Empty Message", "Empty messages are not allowed.")  # Notify the user that empty messages are not allowed

# Function to handle window closing
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to leave the chat?"):  # Confirm if the user wants to quit
        try:
            client.send('@leaves'.encode('utf-8'))  # Send the leave command to the server
        except:
            pass  # Ignore errors if the server is already disconnected
        client.close()  # Close the client socket
        root.destroy()  # Destroy the GUI window

# Function to show the panda-themed name input dialog
def get_panda_name():
    name_dialog = tk.Toplevel(root)  # Create a new top-level window for the name input dialog
    name_dialog.title("Panda Name")  # Set the title of the dialog
    name_dialog.geometry("400x300")  # Set the size of the dialog
    name_dialog.configure(bg="#2d2d2d")  # Set the background color to dark gray

    panda_label = tk.Label(name_dialog, text=PANDA_ART, font=("Courier", 8), fg="#ffffff", bg="#2d2d2d")  # Display the panda ASCII art
    panda_label.pack(pady=10)  # Add padding around the label

    name_label = tk.Label(name_dialog, text="Enter your panda name:", font=("Arial", 12), fg="#ffffff", bg="#2d2d2d")  # Label for the name entry
    name_label.pack(pady=10)  # Add padding around the label
    name_entry = tk.Entry(name_dialog, font=("Arial", 12), bg="#3d3d3d", fg="#ffffff")  # Entry box for the user to input their name
    name_entry.pack(pady=10)  # Add padding around the entry box

    name = None  # Initialize the name variable to None

    def submit_name(event=None):
        nonlocal name  # Access the outer scope variable name
        name = name_entry.get()  # Get the name entered by the user
        if name:  # Check if the name is not empty
            name_dialog.destroy()  # Close the dialog if a valid name is entered
        else:
            messagebox.showwarning("Invalid Name", "Please enter a valid panda name.")  # Show a warning if the name is invalid

    name_entry.bind("<Return>", submit_name)  # Allow the user to submit the name by pressing Enter

    submit_button = tk.Button(
        name_dialog, text="Submit", command=submit_name, font=("Arial", 12), bg="#333333")  # Button to submit the name
    submit_button.pack(pady=10)  # Add padding around the button

    name_entry.focus_set()  # Automatically focus on the entry box when the dialog opens

    name_dialog.wait_window()  # Pause execution until the dialog is closed

    return name  # Return the name entered by the user

# GUI setup
root = tk.Tk()
root.title("Panda Chat Room 🐼")  # Default title
root.geometry("600x500")
root.configure(bg="#2d2d2d")  # Dark gray background

# Frame to hold the text widget + scrollbar (replaces ScrolledText so we can style the scrollbar)
chat_frame = tk.Frame(root, bg="#2d2d2d")
chat_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Chat window 
chat_window = tk.Text(
    chat_frame, state='disabled', wrap=tk.WORD, font=("Arial", 12),
    bg="#3d3d3d", fg="#ffffff"
)
chat_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(
    chat_frame, command=chat_window.yview,
    bg="#333333", # Scrollbar background
    troughcolor="#2d2d2d",   # Trough color
    activebackground="#444444",  # When clicked/active
    highlightbackground="#333333"
)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_window.config(yscrollcommand=scrollbar.set)

# Bottom frame for input box and send button
bottom_frame = tk.Frame(root, bg="#2d2d2d")
bottom_frame.pack(padx=20, pady=10, fill=tk.X)

# Message entry box
entry_box = tk.Entry(bottom_frame, font=("Arial", 12), bg="#3d3d3d", fg="#ffffff")
entry_box.bind("<Return>", send_message)  # Send message on Enter key
entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True)

# button 
send_button = tk.Button(
    bottom_frame, text="Send", command=send_message, font=("Arial", 12), bg="#333333"
)
send_button.pack(side=tk.RIGHT, padx=(10, 0))

# Handle window closing
root.protocol("WM_DELETE_WINDOW", on_closing)

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except:
    messagebox.showerror("Connection Error", "Unable to connect to the server.")
    root.quit()

# Get the panda name from the user
name = get_panda_name()
if name:
    try:
        client.send(name.encode('utf-8'))
        root.title(f"{name}'s Chat Room 🐼")  # Update the title bar with the panda name
    except:
        messagebox.showerror("Connection Error", "Unable to send name to the server.")
        client.close()
        root.quit()
else:
    try:
        client.send("Anonymous Panda".encode('utf-8'))
        root.title("Anonymous Panda's Panda Chat Room 🐼")  # Default title for anonymous users
    except:
        messagebox.showerror("Connection Error", "Unable to send name to the server.")
        client.close()
        root.quit()

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

# Start the GUI event loop
root.mainloop()