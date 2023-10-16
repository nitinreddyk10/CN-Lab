import socket
import threading
import os
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 5657
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT!"

def receive_file(client, filename):
    try:
        with open(filename, "wb") as file:
            data = client.recv(SIZE)
            while data != b"EOF":
                file.write(data)
                data = client.recv(SIZE)
            file.write(b"EOF")
        print(f"[RECEIVED] File '{filename}' received successfully.")
    except:
        print(f"[ERROR] Failed to receive file '{filename}'.")

def recv_msg(client):
    connected = True

    # print("client while loop")
    while connected:
        # print("client while loop inside")
        msg = client.recv(SIZE).decode(FORMAT)
        print("msg received")

        if not msg:
            print("Disconnected from server.")
            break

        parts = msg.split(":")
        if len(parts) == 2:
            type = parts[0]
            content = parts[1]

            if type == "s":
                print(f"[SERVER] {content}")
                continue
            if type == "a":
                print('sf')
                continue
                
            with open(content, "wb") as file:
                time.sleep(0.1)
                data = client.recv(SIZE)
                while data != b"EOF":
                    file.write(data)
                    data = client.recv(SIZE)
                # time.sleep(0.1)

    print("Closing connection...")  
    client.close()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    print(f'[CONNECTED] Connected to server on {IP}:{PORT}')

    thread = threading.Thread(target=recv_msg, args=(client,))
    thread.start()

    connected = True

    while connected:
        msg = input('> Enter IP: ')
        port = input('> Enter Port: ')

        if msg == DISCONNECT_MESSAGE:
            print(f"[DISCONNECTED] Disconnected from {IP}:{PORT}")
            client.send(msg.encode())
            break
        else:
            # Send IP and port as separate strings
            client.send(f"{msg}:{port}".encode(FORMAT))

        filename = input('> Enter File Name ')
        client.send(f"sf:{filename}".encode(FORMAT))

        with open(filename, "rb") as f:
            time.sleep(0.1)
            data = f.read(SIZE)
            while data:
                client.send(data)
                data = f.read(SIZE)
            time.sleep(0.1)
            client.send(b"EOF")

    client.close()

if __name__ == '__main__':
    main()