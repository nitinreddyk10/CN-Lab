import pickle
import struct
import cv2


class Payload:
    def __init__(self, frame, id):
        self.frame = frame
        self.id = id


payload_size = struct.calcsize("Q")
size = 4096


def send_video(client, payload):
    data = pickle.dumps(payload)
    data = struct.pack("Q", len(data)) + data
    client.sendall(data)


def recv_video(client, data):
    while len(data) < payload_size:
        packet = client.recv(size)

        if not packet:
            break
        data += packet
    packed_msg = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg)[0]

    while len(data) < msg_size:
        data += client.recv(size)
    payload = data[:msg_size]
    data = data[msg_size:]
    return payload, data
