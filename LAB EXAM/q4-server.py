import socket

MAX_CONNECTIONS = 5
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', PORT))
server_socket.listen(MAX_CONNECTIONS)

print("Server is listening for clients...")

clients = []

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    
    if len(clients) < MAX_CONNECTIONS:
        clients.append(client_socket)
        print(f"Client {len(clients)} connected to Server.")
    else:
        print(f"Transferring client {len(clients) + 1} to Sr. Server.")
        # Here you can transfer the client_socket to Sr. Server as needed.
        pass


import socket

MAX_CONNECTIONS = 1
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', PORT))
server_socket.listen(MAX_CONNECTIONS)

print("Server is listening for clients-")

servers = {
    'S0': [],
    'S1': [],
    'S2': [],
    'S3': [],
    'S4': []
}

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    
    server_name = client_socket.recv(1024).decode()
    
    if server_name in servers.keys():
        servers[server_name].append(client_socket)
        
        if server_name == 'S0':
            if len(servers[server_name]) > 1:
                old_client_socket = servers[server_name].pop(0)
                old_client_socket.send("You are disconnected.".encode())
                old_client_socket.close()
        elif server_name == 'S1':
            if len(servers[server_name]) > 1:
                disconnected_socket = servers[server_name].pop(0)
                disconnected_socket.send("You are disconnected.".encode())
                disconnected_socket.close()
        elif server_name == 'S2' or server_name == 'S3':
            if len(servers[server_name]) > 1:
                disconnected_socket = servers[server_name].pop(0)
                disconnected_socket.send("You are disconnected.".encode())
                disconnected_socket.close()
        elif server_name == 'S4':
            if len(servers[server_name]) > 1:
                disconnected_socket = servers[server_name].pop(0)
                disconnected_socket.send("You are disconnected.".encode())
                disconnected_socket.close()
                for server in ['S1', 'S2', 'S3']:
                    for client_socket in clients[server]:
                        client_socket.send("You are disconnected.".encode())
                        client_socket.close()
                    clients[server] = []
    else:
        client_socket.send("Invalid server name.".encode())
        client_socket.close()