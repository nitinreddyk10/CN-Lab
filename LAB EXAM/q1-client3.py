import socket

SERVER_ADDRESS = ('localhost', 1234)
FORMAT='utf-8'

client_name = input("Enter server name (S0, S1, S2, S3, or S4): ")

if client_name in ['S0', 'S1', 'S2', 'S3', 'S4']:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    client_socket.send(client_name.encode())

    response = client_socket.recv(1024).decode()
    print(response)

    client_socket.close()
else:
    print("Invalid server name. Please enter S0, S1, S2, S3, or S4.")