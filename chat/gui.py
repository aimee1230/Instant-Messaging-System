import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

#Tkinter's event loop runs in its own thread, ensuring the responsiveness of the GUI. No additional 
#threads need to be managed explicitly for the GUI.

class ChatApp:
    def __init__(self, root):
        #Tkinter root window
        self.root = root
        self.root.title("Chat Application")

        #This creates a scrolled text widget 
        self.message_history = scrolledtext.ScrolledText(self.root, width=50, height=20)
        self.message_history.pack(pady=10)

        #This creates an entry widget
        self.message_entry = tk.Entry(self.root, width=50)
        #The pack method is used to add it to the GUI window with some padding (pady).
        self.message_entry.pack(pady=5)

        #This creates a button widget
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        #sets a protocol for handling the closing event of the root window.
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize client socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        #It uses a try block to attempt the connection, and if successful, it starts a separate thread 
        #to continuously receive messages from the server by calling the self.receive_messages method.
        # If an exception occurs during the connection attempt, an error message is inserted into the 
        #message history widget.

        self.server_ip = "127.0.0.1"  # Change this to the server's IP address
        self.server_port = 12345       # Change this to the server's port number
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.start()
        except Exception as e:
            self.message_history.insert(tk.END, "Error connecting to server: {}\n".format(e))

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(2048).decode()
                if message:
                    self.message_history.insert(tk.END, message + "\n")
                    self.message_history.see(tk.END)
            except Exception as e:
                print("Error receiving message:", e)
                break

    def send_message(self):
        message = self.message_entry.get()
        if message:
            try:
                self.client_socket.send(message.encode())
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                print("Error sending message:", e)

    def on_closing(self):
        self.client_socket.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    chat_app = ChatApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
