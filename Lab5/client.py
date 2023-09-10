# Import the necessary modules
import socket        # Module for socket communication
import threading    # Module for multi-threading
import time         # Module for handling time

# Get the local IP address and define a port to use
ip = socket.gethostbyname(socket.gethostname())
port = 205
addr = (ip, port)

# Define constants for data transmission
size = 1024          # Maximum data size
format = 'utf-8'     # Data encoding format
disconnect_msg = "Disconn"  # Disconnect message

# Define a function for receiving data from the server
def receiving_data(conn, addr):
    flag = True
    while flag:
        msg = conn.recv(size).decode(format)  # Receive and decode data
        if msg == 'Disconn':
            print("Disconnected From the Server")
            break
        msg = msg.split(':')  # Split received message

        if msg[0] == "[ACKNOW]":
            print(f"\033[1K\r[SERVER] {msg[1]}\n")  # Print server acknowledgment message

        elif msg[0] == '[FILE]':
            conn.send("[ACKNOW]:File name Received".encode(format))  # Send acknowledgment to server
            f = open(msg[1], 'w')  # Open a file with the received filename
            ed_data = conn.recv(size).decode(format)
            print(ed_data)
            data = ed_data.split(":")
            if data[0] == '[DATA]':
                f.write(data[1])  # Write received data to the file
                conn.send("[ACKNOW]:Data Received".encode(format))  # Send acknowledgment to server
                print(f"\033[1K\rFile {msg[1]} Received from [SERVER]")
                print('Enter choice 1 to send file else 0: ')
                f.close()  # Close the file
            else:
                print("Error in receiving file\n")  # Handle error in receiving file
    conn.close()  # Close the connection

# Define the main function
def main():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    c.connect(addr)  # Connect to the server
    recv_thread = threading.Thread(target=receiving_data, args=(c, addr))  # Create a thread for receiving data
    recv_thread.start()  # Start the receiving data thread
    print(f"Connected to Server on {addr}")
    while True:
        k = int(input('Enter choice 1 to send file 2 to Disconnect else 0: '))  # Get user input
        if k == 1:
            file_name = input("Enter the file name: ")  # Prompt for the file name
            try:
                f = open(file_name, 'r')  # Open the file for reading
                ed_file_name = '[FILE]:' + file_name
                c.send(ed_file_name.encode(format))  # Send the file name to the server
                data = f.read()  # Read the file contents
                data = '[DATA]:' + data
                c.send(data.encode(format))  # Send the file data to the server
                f.close()  # Close the file
            except FileNotFoundError:
                print("File Not Found\n")  # Handle file not found error
        elif k == 2:
            c.send("Disconn".encode(format))  # Send a disconnect message to the server
            break  # Exit the loop and close the program

# Check if the script is run as the main program
if __name__ == '__main__':
    main()  # Call the main function