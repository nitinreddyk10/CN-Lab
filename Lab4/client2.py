import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            break

def main():
    host = '192.168.201.71'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_id = client_socket.recv(1024).decode('utf-8')
    print(f"Your unique ID: {client_id}")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        try:
            receiver_id = input("Enter receiver's ID (or 'exit' to quit): ")
            if receiver_id.lower() == 'exit':
                client_socket.send("exit|".encode('utf-8'))
                break

            message = input("Enter your message: ")
            client_socket.send(f"{receiver_id}|{message}".encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

if __name__ == '__main__':
    main()