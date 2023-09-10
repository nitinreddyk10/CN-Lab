import socket
import threading
IP = socket.gethostbyname(socket .gethostname())
PORT = 1234
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def handle_client(conn, addr):
    print(f" [NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False
        else:
            print(f"[{addr}] {msg}")
            response = f"Msg received: {msg}"
            conn.send(response.encode(FORMAT))
    
    conn.close()


def main():
    print(" [STARTING] Server is starting.")
    server = socket. socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is Listening on {IP}: {PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading. Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
