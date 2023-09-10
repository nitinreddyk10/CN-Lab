import socket
import threading
import random
import string

clients = {}
lock = threading.Lock()



def generate_unique_id():
    return ''.join(random.choice(string.hexdigits) for _ in range(6))


def handle_client(client_socket, client_address):
    unique_id = generate_unique_id()

    with lock:
        clients[unique_id] = client_socket
        client_socket.send(f"Your unique ID is: {unique_id}".encode('utf-8'))
        update_client_list()

    print(f"New connection from {client_address} - ID: {unique_id}")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            receiver_id, msg = message.split('|')
            with lock:
                receiver_socket = clients.get(receiver_id)
                if receiver_socket:
                    receiver_socket.send(f"Message from {unique_id}: {msg}".encode('utf-8'))
                else:
                    client_socket.send(f"Error: Client {receiver_id} not found.".encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
            break

    with lock:
        del clients[unique_id]
        print(f"Connection closed with {client_address} - ID: {unique_id}")
        update_client_list()

    client_socket.close()


def update_client_list():
    online_clients = "Online Clients: " + ', '.join(clients.keys())
    for client_socket in clients.values():
        try:
            client_socket.send(online_clients.encode('utf-8'))
        except:
            pass


def main():
    host = '192.168.201.71'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == '__main__':
    main()
