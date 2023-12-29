import cv2
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from network import *
import platform


class Gui:
    def __init__(self):
        self.root = Tk()
        self.root.title("Video Conferencing App")
        self.id = 0
        self.return_id = 0
        self.max_clients = 0
        self.chat_client = None
        self.ft_client = None

        self.tab_control = ttk.Notebook(self.root)

        self.video_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.video_tab, text="Video Conferencing")
        self.chat_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.chat_tab, text="Chat")
        self.file_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.file_tab, text="File Transfer")

    def start(self):
        # Video Conferencng Tab Content
        self.video_label = Label(self.video_tab, text=f"Client {self.id} Video Room")
        self.canvas = Canvas(self.video_tab, width=800, height=600)
        self.next_button = Button(self.video_tab, text="NEXT", command=self.go_next)
        self.prev_button = Button(self.video_tab, text="PREV", command=self.go_prev)

        self.video_label.pack()
        self.canvas.pack()
        self.next_button.pack(side=RIGHT, padx=10)
        self.prev_button.pack(side=LEFT, padx=10)

        self.client_names = [f"Client {id}" for id in range(self.max_clients)]
        self.chat_client_var = StringVar()
        self.file_client_var = StringVar()

        # Chat Tab Content
        self.chat_label = Label(self.chat_tab, text=f"Client {self.id} Chat Room")
        self.chat_box = Text(self.chat_tab, height=20, width=50)
        self.message_entry = Entry(self.chat_tab, width=50)
        self.broadcast_button = Button(
            self.chat_tab, text="Broadcast", command=self.broadcast_message
        )
        self.unicast_button = Button(
            self.chat_tab, text="Unicast", command=self.unicast_message
        )
        self.chat_dropdown = ttk.Combobox(
            self.chat_tab, textvariable=self.chat_client_var, values=self.client_names
        )

        self.chat_dropdown.set("Select Client")
        self.chat_label.pack()
        self.chat_box.pack(pady=10)
        self.message_entry.pack(pady=10)
        self.broadcast_button.pack()
        self.unicast_button.pack()
        self.chat_dropdown.pack()

        # File Transfer Tab Content
        self.file_label = Label(
            self.file_tab, text=f"Client {self.id} File Transfer Room"
        )
        self.file_box = Text(self.file_tab, height=20, width=50)
        self.file_entry = Entry(self.file_tab, width=40)
        self.browse = Button(
            self.file_tab, text="Browse File", command=self.choose_file
        )
        self.unicast_file_button = Button(
            self.file_tab, text="Unicast File", command=self.unicast_file
        )
        self.broadcast_file_button = Button(
            self.file_tab, text="Broadcast File", command=self.broadcast_file
        )
        self.file_dropdown = ttk.Combobox(
            self.file_tab, textvariable=self.file_client_var, values=self.client_names
        )

        self.file_dropdown.set("Select Client")
        self.file_label.pack()
        self.file_box.pack(pady=10)
        self.file_entry.pack(pady=10)
        self.browse.pack()
        self.broadcast_file_button.pack()
        self.unicast_file_button.pack()
        self.file_dropdown.pack()

        self.tab_control.pack(expand=1, fill="both")
        self.root.mainloop()

    def update(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)  # Create a PIL image
        img = ImageTk.PhotoImage(image=img)  # Convert to Tkinter-compatible image
        self.canvas.create_image(0, 0, anchor=NW, image=img)
        self.canvas.img = img

    def go_next(self):
        self.return_id = (self.return_id + 1) % self.max_clients

    def go_prev(self):
        self.return_id = (self.return_id - 1) % self.max_clients

    def broadcast_message(self):
        message = self.message_entry.get()
        self.message_entry.delete(0, END)
        self.chat_client.send(message.encode())

    def unicast_message(self):
        message = self.message_entry.get()
        self.message_entry.delete(0, END)
        id = self.chat_client_var.get().split(" ")[1]
        message = f"/private {id} {message}"
        self.chat_client.send(message.encode())

    def choose_file(self):
        file_path = filedialog.askopenfilename()
        self.file_entry.delete(0, END)
        self.file_entry.insert(0, file_path)

    def broadcast_file(self):
        file_path = self.file_entry.get()
        file_name = file_path.split('\\')[-1]
        with open(file_path, "rb") as file:
            file_data = file.read()
        payload = Payload(file_data, file_name)
        send_video(self.ft_client, payload)

    def unicast_file(self):
        file_path = self.file_entry.get()
        file_name = file_path.split('\\')[-1]
        id = self.file_client_var.get().split(" ")[1]
        with open(file_path, "rb") as file:
            file_data = file.read()
        file_name = f"/private {id} {file_name}"
        payload = Payload(file_data, file_name)
        send_video(self.ft_client, payload)