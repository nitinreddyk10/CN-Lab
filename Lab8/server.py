import socket
import threading
import datetime
import queue
import time
from collections import deque

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_port = 12345
server_socket.bind(("localhost", server_port))
server_socket.listen(5)
print(f"Server is listening on port {server_port}")

# List to store client connections and game data
clients = []

# Create a queue to store user requests
user_request_queue = queue.Queue(maxsize=4)

# Dictionary to store user payment status (e.g., True for paid, False for unpaid)
user_payment_status = {}

size = int(input('Enter the size: '))
grid = [[' ' for _ in range(size)] for _ in range(size)]
scores = {'S': 0, 'O': 0}
current_player = 'S'

# Number of clients with user_payment_status set to True
paid_clients_count = 0

# Function to send the game grid to all clients
def send_game_state():
    game_state = '\n'.join([' | '.join(row) for row in grid])
    print(game_state)
    for client in clients:
        client.send(game_state.encode())
        

# Function to check for SOS sequences and calculate the score
def check_sos(grid, row, col, letter):
    sos_count = 0

    if letter == 1:  # Check for 'S'
        # Check horizontally (left and right)
        if col >= 2 and grid[row][col - 2] == 'S' and grid[row][col - 1] == 'O':
            sos_count += 1
        if col <= size - 3 and grid[row][col + 2] == 'S' and grid[row][col + 1] == 'O':
            sos_count += 1

        # Check vertically (up and down)
        if row >= 2 and grid[row - 2][col] == 'S' and grid[row - 1][col] == 'O':
            sos_count += 1
        if row <= size - 3 and grid[row + 2][col] == 'S' and grid[row + 1][col] == 'O':
            sos_count += 1
    elif letter == 2:  # Check for 'O'
        # Check horizontally (left and right)
        if col >= 1 and col <= size - 2 and grid[row][col - 1] == 'S' and grid[row][col + 1] == 'S':
            sos_count += 1

        # Check vertically (up and down)
        if row >= 1 and row <= size - 2 and grid[row - 1][col] == 'S' and grid[row + 1][col] == 'S':
            sos_count += 1

    return sos_count


def is_grid_full(grid):
    for row in grid:
        if ' ' in row:
            return False
    print("Grid is full.GAME OVER")
    return True

def set_grid():
    global grid
    grid = [[' ' for _ in range(size)] for _ in range(size)]

def set_scores():
    global scores
    scores = {'S': 0, 'O': 0}

def set_player():
    global current_player
    current_player = 'S'

time_duration =0

# Function to authenticate a user based on payment status
def authenticate_user(client_socket):
    # Check if there are less than two clients in the clients list
    if len(clients) < 2:
        client_socket.send("Enter the time you want to play (in minutes): ".encode())
        playtime = client_socket.recv(1024).decode()
        
        # Step 1: Check if the entered playtime is valid (you can add more validation)
        try:
            playtime = int(playtime)
            if playtime < 1:
                raise ValueError
            else:
                global time_duration
                time_duration = playtime*60
        except ValueError:
            client_socket.send("Invalid playtime. Please enter a valid positive integer.".encode())
            return False

        # Step 2: Calculate the cost for playing based on playtime (e.g., Rs. 10 per minute)
        cost = 10 * playtime  # Adjust the cost calculation as needed

        client_socket.send(f"Cost for {playtime} minutes of playtime is Rs. {cost}. Please pay this amount: ".encode())
        payment = client_socket.recv(1024).decode()

        if payment == str(cost) and len(clients)<2:
            # Step 3: Add the authenticated user to the clients list
            clients.append(client_socket)
            return True
        else:
            client_socket.send(f"Payment of Rs. {cost} not accepted. Please pay the required amount to play next time.".encode())
    else:
        client_socket.send("Game is full. Please wait for the next game.".encode())
        return False


# Function to start the SOS game with a timeout
# Function to start the SOS game with a timeout
def start_game(clients):
    global current_player
    global time_duration
    global grid
    if current_player == 'S':
        clients[0].send("Your name is S. Enter S to make a move.".encode())
        clients[1].send("Your name is O. Enter O to make a move.".encode())
    end_time = time.time() + time_duration
    print(end_time)
    while time.time() < end_time:
                if current_player == 'S':
                    i=0
                    clients[0].send(" Enter S to make a move.".encode())
                    print("Hello server")
                    data = clients[0].recv(1024).decode()
                    print(data)
                    if not data:
                        break
                    if data == "QUIT":
                        break
                    if data == current_player:
                        print(f"PLAYER {current_player}")
                        clients[0].send("Your turn. Enter row, column, and letter (e.g., 1,2,s-1 o-2): ".encode())
                        move = clients[0].recv(1024).decode()
                        row, col, lett = map(int, move.split(','))
                        if 0 <= row < 4 and 0 <= col < 4 and grid[row][col] == ' ':
                            if lett == 1:
                                grid[row][col] = 'S'
                            if lett == 2:
                                grid[row][col] = 'O'
                            clients[0].send("\nMove accepted".encode())
                        else:
                            clients[0].send("\nINVALID MOVE".encode())
                    else:
                        clients[0].send("Not your turn. Wait for your opponent.".encode())
                if current_player == 'O':
                    i=1
                    clients[1].send(" Enter O to make a move.".encode())
                    data = clients[1].recv(1024).decode()
                    if not data:
                        break
                    if data == "QUIT":
                        break
                    if data == current_player:
                        print(f"PLAYER {current_player}")
                        clients[1].send("Your turn. Enter row, column, and letter (e.g., 1,2,s-1 o-2): ".encode())
                        move = clients[1].recv(1024).decode()
                        row, col, lett = map(int, move.split(','))
                        if 0 <= row < 4 and 0 <= col < 4 and grid[row][col] == ' ':
                            if lett == 1:
                                grid[row][col] = 'S'
                            if lett == 2:
                                grid[row][col] = 'O'
                            clients[1].send("\nMove accepted".encode())
                    else:
                        clients[1].send("Not your turn. Wait for your opponent.".encode())
                send_game_state()
                score = check_sos(grid, row, col, lett)

                if score > 0:
                            clients[i].send("\nYou scored one point".encode())
                            scores[current_player] += score
                            for client in clients:
                                client.send(f"\nSCORES: {scores}".encode())
                else:
                            clients[i].send("\nNo SOS found".encode())

                if (is_grid_full(grid)):
                            for client in clients:
                                client.send(f"\nSCORES: {scores}".encode())
                            break
                current_player = 'S' if current_player == 'O' else 'O'
                time_remaining = int(end_time - time.time())
                if(time_remaining<0):
                    print("TIME OUT")
                    for client in clients:
                        client.send("\nTIMEOUT".encode())
                else:
                    print(f"Time remaining: {time_remaining // 60} minutes {time_remaining % 60} seconds")
                    for client in clients:
                        client.send(f"Time remaining: {time_remaining // 60} minutes {time_remaining % 60} seconds".encode())
                
            
    for client_socket in clients:
        if (scores['S'] > scores['O']):
            client_socket.send("\nWinner is PLAYER S".encode())
        elif (scores['O'] > scores['S']):
            client_socket.send("\nWinner is PLAYER O".encode())
        else:
            client_socket.send(f"\nIt's a Tie".encode())
        client_socket.send(f"\nGame OVER".encode())
    set_grid()
    set_scores()
    set_player()
    return True

def check_queue():
    global user_request_queue
    print("220")

    # Close all client sockets and remove clients
    for client in clients:
        print("222")
        client.close()
    clients.clear()

    if user_request_queue.qsize()==0:
        server_socket.close()
    else:
        print("228")
        # Ensure user_request_queue has at least two items before processing
        if user_request_queue.qsize() >= 2:
            authenticate_user(user_request_queue.get())
            authenticate_user(user_request_queue.get())

            # Remove the first two elements from user_request_queue
           # print(user_request_queue)

            if len(clients) == 2:
                end = start_game(clients)
                if end:
                    check_queue()
        else:
            print("Not enough requests in the queue to process.")


# Function to handle client connections and game moves
def handle_client(client_socket):
    global current_player, paid_clients_count

    # Authenticate the user based on payment
    # client_address = client_socket.getpeername()

    # Step 1: Ask the connected client for the time they want to play
    if len(clients) < 2:
        authenticate_user(client_socket)
    else:
        if user_request_queue.qsize() < 4:  # Check if the queue is not full
            user_request_queue.put(client_socket)
            client_socket.send("Game is full. Please wait for the next game.".encode())
        else:
            client_socket.send(
                "Game is full, and the queue is full. Please try again later.".encode())
            client_socket.close()

    if len(clients) == 2 and client_socket in clients:
        end=start_game(clients)
        print(f"end={end}")
        if end:
           check_queue()
        
         
        # Your code here to start the game for clients in clients list


# Accept client connections and start a thread for each client
while True:
    client_socket, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()