import socket
import cv2
from network import *
import numpy as np
import threading

max_clients = 4
size = 4096

video_server = socket.socket()
video_server.bind(("192.168.29.234", 7777))
video_server.listen(max_clients)
temp_image = cv2.imread("black.jpg")
frames = [temp_image] * max_clients

chat_server = socket.socket()
chat_server.bind(("192.168.29.234", 7778))
chat_server.listen(max_clients)
chat_clients = [0] * max_clients

ft_server = socket.socket()
ft_server.bind(("192.168.29.234", 7779))
ft_server.listen(max_clients)
ft_clients = [0] * max_clients

def handle_video(video_client, id):
    data = b""
    while True:
        payload, data = recv_video(video_client, data)
        payload = pickle.loads(payload)
        frames[id] = payload.frame

        send_video(video_client, frames[payload.id])

def handle_chat(chat_client, id):
    while True:
        message = chat_client.recv(size).decode()

        if message.startswith("/private"):
            _, to_id, message = message.split(" ", 2)
            chat_clients[int(to_id)].send(f"[PRIVATE] Client{id} : {message}".encode())
        else:
            message = f"Client{id} : {message}"
            for client in chat_clients:
                if client != 0:
                    client.send(message.encode())

def handle_file(ft_client, id):
    data = b""
    while True:
        payload, data = recv_video(ft_client, data)
        payload = pickle.loads(payload)
        file_data = payload.frame
        file_name = payload.id

        if file_name.startswith("/private"):
            _, to_id, file_name = file_name.split(" ", 2)
            payload.id = f"{id} {file_name}"
            send_video(ft_clients[int(to_id)], payload)
        else:
            payload.id = f"{id} {file_name}"
            for client in ft_clients:
                if client != 0:
                    send_video(client, payload)

id = 0
while True:
    video_client, addr = video_server.accept()
    video_client.sendall(f"{id}^{max_clients}".encode())
    video_thread = threading.Thread(target=handle_video, args=(video_client, id))
    video_thread.start()

    chat_client, addr = chat_server.accept()
    chat_clients[id] = chat_client
    chat_thread = threading.Thread(target=handle_chat, args=(chat_client, id))
    chat_thread.start()

    ft_client, addr = ft_server.accept()
    ft_clients[id] = ft_client
    ft_thread = threading.Thread(target=handle_file, args=(ft_client, id))
    ft_thread.start()

    id += 1