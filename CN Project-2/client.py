import socket
import threading
from network import *
from interface import *
import cv2

def handle_video(video_client, id):
    cap = cv2.VideoCapture(0)
    data = b""
    while True:
        ret, frame = cap.read()
        payload = Payload(frame, gui.return_id)
        send_video(video_client, payload)

        frame, data = recv_video(video_client, data)
        frame = pickle.loads(frame)
        frame = cv2.resize(frame, (800, 600))
        gui.update(frame)

def handle_chat(chat_client, id):
    while True:
        message = chat_client.recv(4096).decode()
        gui.chat_box.insert(END, message + "\n")

def handle_file(ft_client, id):
    data = b""
    while True:
        file, data = recv_video(ft_client, data)
        file = pickle.loads(file)
        file_data = file.frame
        from_id, file_name = file.id.split(" ")
        gui.file_box.insert(END, f"[Received] {file_name} From Client{from_id}\n")
        with open(f"Client{from_id}_{file_name}", "wb") as fp:
            fp.write(file_data)

gui = Gui()

video_client = socket.socket()
video_client.connect(("192.168.29.234", 7777))
gui.id, gui.max_clients = list(map(int, video_client.recv(size).decode().split("^")))
gui.return_id = gui.id
video_thread = threading.Thread(target=handle_video, args=(video_client, gui.id))
video_thread.start()

chat_client = socket.socket()
gui.chat_client = chat_client
chat_client.connect(("192.168.29.234", 7778))
chat_thread = threading.Thread(target=handle_chat, args=(chat_client, gui.id))
chat_thread.start()

ft_client = socket.socket()
gui.ft_client = ft_client
ft_client.connect(("192.168.29.234", 7779))
ft_thread = threading.Thread(target=handle_file, args=(ft_client, gui.id))
ft_thread.start()

gui.start()