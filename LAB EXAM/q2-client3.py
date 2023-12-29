import socket

def main():
    host = '127.0.0.1'
    port = 12346

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        message = input("Enter a message to send to the server (or) type 'exit' : ")
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")

    client_socket.close()

if __name__ == "__main__":
    main()