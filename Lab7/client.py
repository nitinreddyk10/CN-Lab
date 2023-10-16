import socket
import threading
import queue

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "localhost"
server_port = 12345
client_socket.connect((server_ip, server_port))

# Create a queue for user input
user_input_queue = queue.Queue()

# Function to send user input to the server
def send_message():
    while True:
        message = user_input_queue.get()
        client_socket.send(message.encode())
        if message == "QUIT":
            break

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()
            print(message)
            if "OVER" in message:
                break
        except ConnectionResetError:
            print("Connection closed by the server.")
            break

# Start two threads for sending and receiving messages
send_thread = threading.Thread(target=send_message)
recv_thread = threading.Thread(target=receive_messages)

send_thread.start()
recv_thread.start()

# Main user input loop
while True:
    message = input()
    user_input_queue.put(message)

# Ensure that the send thread has finished before closing the socket
send_thread.join()
client_socket.close()