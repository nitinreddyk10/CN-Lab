import socket
import threading

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_port = 12345
server_socket.bind(("localhost", server_port))
server_socket.listen(5)
print(f"Server is listening on port {server_port}")

# List to store client connections and game data
clients = []
size =int(input('enter size: '))
grid = [[' ' for _ in range(size)] for _ in range(size)]
scores = {'S': 0, 'O': 0}
current_player = 'S'

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


# Function to handle client connections and game moves
# Function to handle client connections and game moves
def handle_client(client_socket):
    global current_player
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            if data == "QUIT":
                break
            if data == current_player:
                print(f"PLAYER {current_player}")
                client_socket.send("Your turn. Enter row, column and letter (e.g., 1,2,s-1 o-2): ".encode())
                move = client_socket.recv(1024).decode()
                row, col, lett = map(int, move.split(','))
                if 0 <= row < 4 and 0 <= col < 4 and grid[row][col] == ' ':
                    if lett == 1:
                        grid[row][col] = 'S'
                    if lett == 2:
                        grid[row][col] = 'O'
                    client_socket.send("\nMove accepted".encode())
                    send_game_state()
                    score = check_sos(grid, row, col,lett)
                    
                    if score > 0:
                        client_socket.send("\nYou scored one point".encode())
                        scores[current_player] += score
                        for client in clients:
                            client.send(f"\nSCORES: {scores}".encode())
                    else:
                        client_socket.send("\nNo SOS found".encode())
                    
                    if(is_grid_full(grid)):
                        for client in clients:
                            client.send(f"\nSCORES: {scores}".encode())
                            #client.close()  # Close the client socket
                        break;
                    current_player = 'S' if current_player == 'O' else 'O'
                    #client_socket.send("Enter name: ".encode())
                else:
                    client_socket.send("Invalid move. Try again.".encode())
            else:
                client_socket.send("Not your turn. Wait for your opponent.".encode())
        except:
            continue
    for client in clients:
        if(scores['S']>scores['O']):
            client.send("\nWinner is PLAYER S".encode())
        elif(scores['O']>scores['S']):
            client.send("\nWinner is PLAYER O".encode())
        else:
            client.send(f"\nIts a Tie".encode())
        client.send(f"\nGame OVER".encode())




# Accept client connections and start a thread for each client
while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)
    if len(clients)==1:
        client_socket.send("Your name is S . Enter S to make move.".encode())
        print(f"Client 1 connected on {addr}")
    else:
        client_socket.send("Your name is O . Enter O to make move.\n".encode())
        print(f"Client 2 connected on {addr}")
        print("2 CLIENTS CONNECTED SUCCSSFULLY")
        send_game_state()
        for client in clients:
            client.send("_______".encode())
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()