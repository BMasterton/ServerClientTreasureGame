from View import display
from Board import Board
from Tile import Tile
import random
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

newBoard = Board(3, 10, 5, 10, 2) # creating the new boar
randPlayerXPos = random.randrange(0, 10) # creating initial random x and y coords
randPlayerYPos = random.randrange(0, 10)
playerNames = ["1", "2"] # list of players that will be added
playerDirections = ['U' , 'D' , 'L' , 'R' , 'Q']

BUF_SIZE = 1024
HOST = ''
PORT = 12345


# goes over all the players in playerNames and looks at a random  x and y pos so it can add them, if that position is
# not a "." then it will try again until it can, if the spot is taken it will let the player know
for player in playerNames:
    randPlayerXPos = random.randrange(0, 10)
    randPlayerYPos = random.randrange(0, 10)
    # making sure that if the tile already has a player or a treaure, another player cant spawn on them
    while newBoard.board[randPlayerXPos][randPlayerYPos].get_treasure() is not None:
        if newBoard.board[randPlayerXPos][randPlayerYPos].get_player_from_current_tile() is not None:
            randPlayerXPos = random.randrange(0, 10)
            randPlayerYPos = random.randrange(0, 10)
            raise ValueError("space already occupied")
    newBoard.add_player(player, randPlayerXPos, randPlayerYPos)

while True:
    try:
        display(newBoard)
        with socket(AF_INET, SOCK_STREAM) as sock:  # TCP socket
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Details later
            sock.bind((HOST, PORT))  # Claim messages sent to port "PORT"
            sock.listen(1)  # Server only supports a single 3-way handshake at a time
            print('Server:', sock.getsockname())  # Server IP and port
            while True:
                sc, _ = sock.accept()  # Wait until a connection is established
                with sc:
                    print('Client:', sc.getpeername())  # Client IP and port
                    data = sc.recv(BUF_SIZE)  # recvfrom not needed since address known
                    print(data)
                    sc.sendall(data)  # Client IP and port implicit due to accept call
    # get value from user and make sure its an allowed input if not tell them and repeat until proper input
                    playerInputDirection = input("(U)p (D)own (L)eft (R)ight (Q)uit \n")
                    if playerInputDirection.upper() not in playerDirections:
                        raise Exception('Must give a valid direction or quit')
                    # get player name input from user and depending on the player send that info to moveplayer
                    playerInputPlayer = str(input("Player 1 or 2 \n"))
                    if playerInputPlayer not in playerNames:
                        raise Exception('value must be 1 or 2')
                    if playerInputPlayer == '1':
                        newBoard.move_player(playerNames[0], playerInputDirection)
                    elif playerInputPlayer == '2':
                        newBoard.move_player(playerNames[1], playerInputDirection)
    except Exception as details:
        print(str(details))



