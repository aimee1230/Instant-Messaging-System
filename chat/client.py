import socket
import threading

#One thread per client to handle multiple client connections concurrently.
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(2048).decode()
            if message:
                print(message)
        except Exception as e:
            print("Error receiving message:", e)
            break

def main():
    # Specify the server's IP address and port number
    server_ip = "127.0.0.1"  # Change this to the server's IP address
    server_port = 12345      # Change this to the server's port number

    # Create a socket object for connecting to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print("Connected to server.")

        # Start a thread to receive messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        # Main loop to send messages to the server
        while True:
            try:
                message = input()  # Get input from the user
                client_socket.send(message.encode())  # Send the message to the server
            except KeyboardInterrupt:
                # Handle Ctrl+C to gracefully exit
                print("Exiting...")
                break

    except ConnectionRefusedError:
        print("Connection refused: The server is not available.")
    except Exception as e:
        print("Error:", e)
    finally:
        # Close the socket when done
        client_socket.close()

if __name__ == "__main__":
    main()
