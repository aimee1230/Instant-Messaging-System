import socket
import select
import sys
from _thread import *

#One thread to continuously receive messages from the server while allowing the main thread to handle 
#user input and other tasks.
# Function to handle incoming connections
def clientthread(conn, addr):
    # sends a message to the client whose user object is conn
    conn.send("Welcome to this chatroom!".encode())

    while True:
        try:
            message = conn.recv(2048)
            if message:
                # prints the message and address of the user who just sent the message on the server terminal
                print("<" + addr[0] + "> " + message.decode())

                # Calls broadcast function to send message to all
                message_to_send = "<" + addr[0] + "> " + message.decode()
                broadcast(message_to_send, conn)

            else:
                # message may have no content if the connection is broken, in this case we remove the connection
                remove(conn)

        except:
            continue

# Function to broadcast message to all clients except the sender
def broadcast(message, connection):
    for client_socket in list_of_clients:
        if client_socket != connection:
            try:
                client_socket.send(message.encode())
            except:
                # If the link is broken, we remove the client
                client_socket.close()
                remove(client_socket)

# Function to remove client from list_of_clients
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

# Main function to handle server setup and connections
def main():

    # Take IP address and port number from command line arguments
    IP_address = "127.0.0.1"  # Change this to the server's IP address
    Port = 12345      # Change this to the server's port number

    # Create server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the server to the specified IP address and port number
    server.bind((IP_address, Port))

    # Listen for incoming connections
    server.listen(100)

    # List to keep track of connected clients
    global list_of_clients
    list_of_clients = []

    print("Server started on {}:{}".format(IP_address, Port))

    while True:
        # Accept incoming connection
        conn, addr = server.accept()

        # Add the new client to the list of clients
        list_of_clients.append(conn)

        # Print the address of the client that just connected
        print(addr[0] + " connected")

        # Create a new thread to handle the client
        start_new_thread(clientthread, (conn, addr))

    conn.close()
    server.close()

# Call the main function
if __name__ == "__main__":
    main()
