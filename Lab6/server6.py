import socket
import threading
import time

IP = socket.gethostbyname(socket.gethostname()) 
PORT = 5657
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
DISCONNECT_MSG = "DISCONNECT!"

conn_clients = []

def send_file(conn, filename):
    try:
        with open(filename, "rb") as file:
            data = file.read(SIZE)
            while data:
                conn.send(data)
                data = file.read(SIZE)
        conn.send(b"EOF")
    except FileNotFoundError:
        print(f"[ERROR] File '{filename}' not found.")

def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} Connected!')

    for client in conn_clients:
        if client['addr'] != addr:
            conn.send(f"s:[EXISTING CONNECTION]... {client['addr'][0]} {client['addr'][1]} connected to the server".encode(FORMAT))

    for client in conn_clients:
        if client['addr'] != addr:
            client['conn'].send(f"s:\n[NEW CONNECTION]...{addr[0]} {addr[1]}".encode(FORMAT))

    connected = True

    while connected:
        msg = conn.recv(1024).decode(FORMAT)
        
        if msg == DISCONNECT_MSG:
            connected = False
            for client in conn_clients:
                if client['addr'] != addr:
                    client['conn'].send(f"s:\n[DISCONNECTED]...{addr[0]} {addr[1]} from the server".encode(FORMAT))
            for client in conn_clients:
                if client["addr"] == addr:
                    conn_clients.remove(client)
                    break
            else:
                print(f'[ERROR] Cannot Disconnect {addr}')
        else:
            # Split the received message into IP and port
            parts = msg.split(":")
            if len(parts) == 2:
                to_ip = parts[0]
                to_port = int(parts[1])

                # Receive the filename and create a new file to write data
                filename = conn.recv(1024).decode(FORMAT)

                for client in conn_clients:
                    if client["addr"] == (to_ip, to_port):
                        client["conn"].send(filename.encode())
                        break

                for client in conn_clients:
                    if client['addr'] == (to_ip, to_port):
                        send_conn = client['conn']
                        break

                # data = conn.recv(1024)
                time.sleep(0.1)
                while True:
                    data = conn.recv(1024)
                    if data == b"EOF":
                        break
                    send_conn.send(data)
                time.sleep(0.1)
                send_conn.send(b"EOF")
                    # data = conn.recv(1024)

    conn.close()

def main():
    print(f'[SERVER] Starting... ')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(ADDR)

    server.listen()
    print(f'[SERVER] Listening on port : {PORT} ...')

    while True:
        conn, addr = server.accept()
        conn_clients.append({"conn" : conn, "addr" : addr})

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

if __name__ == '__main__':
    main()