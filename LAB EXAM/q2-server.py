import socket

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')
        response = f"Server received: {message}"
        client_socket.send(response.encode('utf-8'))
    client_socket.close()

def main():
    host = '127.0.0.1'
    port_s = 12345
    port_sr = 12346
    max_clients = 2 #max clients

    # Server s
    server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_s.bind((host, port_s))
    server_s.listen(max_clients)
    print(f"Server s is listening on {host}:{port_s}")

    # Redundant Server sr
    server_sr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sr.bind((host, port_sr))
    server_sr.listen(1)
    print(f"Redundant Server sr is listening on {host}:{port_sr}")

    connected_clients = 0

    while True:
        if connected_clients < max_clients:
            # Accept a connection for server s
            client_socket, client_address = server_s.accept()
            connected_clients += 1
            print(f"Accepted connection for server s from {client_address}")
            handle_client(client_socket)
        else:
            # Transfer the connection to server sr
            client_socket, client_address = server_sr.accept()
            print(f"Transferred connection to server sr from {client_address}")
            handle_client(client_socket)

if __name__ == "__main__":
    main()