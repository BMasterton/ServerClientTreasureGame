import struct

from View import display
from Board import Board
from threading import Semaphore, Thread
import random
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

playerDirections = ['U', 'D', 'L', 'R', 'Q', 'G']
playerDirectionDecimals = [2, 3, 4, 6, 8, 15]
BUF_SIZE = 1024
lock =  Semaphore()
playerCounter = 0


def get_line(current_socket: socket) -> str:
    buffer = b''
    while True:
        data = current_socket.recv(BUF_SIZE)
        if data == b'' or data == b'\n':
            return buffer
        buffer = buffer + data

def playerControl(sc, newBoard, playerNames):
    global playerCounter
    with sc:
        if playerCounter < 3:
            playerCounter += 1
        else:
            print("Player limit reached")
        sc.sendall(struct.pack("!H", playerCounter)) # so add if playerCoutner is 1 or two send the literal byte string
        # sc.sendall(b'\x01')
        print('Client:', sc.getpeername())  # Client IP and port
        data = sc.recv(1)  # ust this to get info from client
        #data3 = get_line(sc) # this should be the data we get from the client
        data2 = list(data)
        my_byte = data2[0]
        first_four_full = my_byte & 240
        first_four_only = first_four_full >> 4
        middle_two_full = my_byte & 12
        middle_two_only = middle_two_full >> 2
        if first_four_only == playerDirectionDecimals[0]:  # direcion Up
            playerInputDirection = playerDirections[0]
            sc.sendall(
                struct.pack('!HH', newBoard.printPlayerScore('1'), newBoard.printPlayerScore('2')))
        elif first_four_only == playerDirectionDecimals[1]:  # direction Down
            playerInputDirection = playerDirections[1]
            sc.sendall(
                struct.pack('!HH', newBoard.printPlayerScore('1'), newBoard.printPlayerScore('2')))
        elif first_four_only == playerDirectionDecimals[2]:  # direction Left
            playerInputDirection = playerDirections[2]
            sc.sendall(
                struct.pack('!HH', newBoard.printPlayerScore('1'), newBoard.printPlayerScore('2')))
        elif first_four_only == playerDirectionDecimals[3]:  # direction Right
            playerInputDirection = playerDirections[3]
            sc.sendall(
                struct.pack('!HH', newBoard.printPlayerScore('1'), newBoard.printPlayerScore('2')))
        elif first_four_only == playerDirectionDecimals[
            4]:  # when Q is received run send the scores of 1 and then 2 as shorts, send gameboard then itll run the quit command
            playerInputDirection = playerDirections[4]
            sc.sendall(struct.pack('!HH', newBoard.printPlayerScore('1'), newBoard.printPlayerScore('2')))
            sc.sendall(newBoard.boardString().encode('utf-8'))
        elif first_four_only == playerDirectionDecimals[
            5]:  # when G is hit, print the scores, print the board, and then transmit the board
            with lock:
                newBoard.printScore() # anything that is accessing newBoard and doing something on newboard we need to lock it so that its consistent
            sc.sendall(struct.pack('!HH', newBoard.printPlayerScore('1'), newBoard.printPlayerScore('2')))
            display(newBoard)
            sc.sendall(newBoard.boardString().encode('utf-8'))
        playerInputPlayer = str(middle_two_only)
        print('Data', data)  # printing the data we receive

        # making sure the directions and players are allowed choices or reject
        if playerInputDirection not in playerDirections:
            raise Exception('Must give a valid direction or quit')
        if playerInputPlayer not in playerNames:
            raise Exception('value must be 1 or 2')
        if playerInputPlayer == '1':
            newBoard.move_player(playerNames[0], playerInputDirection)
        elif playerInputPlayer == '2':
            newBoard.move_player(playerNames[1], playerInputDirection)
        display(newBoard)

class Game:
    def __init__(self):
        pass

    def start(self):
        newBoard = Board(5, 10, 5, 10, 2)  # creating the new boar
        playerNames = ["1", "2"]  # list of players that will be added
        clientCounter = 0
        connections = {} # perhaps for clients, the name is just player one or two based on whos been connected, and the value is whatever is returned from socket(AF_Inet, SOCK_STREAM)
                        # sc.getpeername is the clinets ip and port tho
        HOST = ''
        PORT = 12345


        # goes over all the players in playerNames and looks at a random  x and y pos so it can add them, if that position is
        # not a "." then it will try again until it can, if the spot is taken it will let the player know
        for player in playerNames:
            randPlayerXPos = random.randrange(0, 10)
            randPlayerYPos = random.randrange(0, 10)
            # making sure that if the tile already has a player or a treaure, another player cant spawn on them
            while newBoard.board[randPlayerXPos][randPlayerYPos].get_treasure() is not None or newBoard.board[randPlayerXPos][randPlayerYPos].get_player_from_current_tile() is not None:
                randPlayerXPos = random.randrange(0, 10)
                randPlayerYPos = random.randrange(0, 10)
            newBoard.add_player(player, randPlayerXPos, randPlayerYPos)

        thread_list = []
        # for i in range(2):
        #     thread_list.append(Thread(target=playerControl, args=(i, )))
        #     thread_list[-1].start()
        #
        # for t in thread_list:
        #     t.join() #kill command need the children to be killed before main ends

        while True:
            try:
                display(newBoard) #displays the original board
                #The question is do i need to keep doing it this way or do i have to break it up and do it
                # similar to the wya the test_server is doing it with clients
                with socket(AF_INET, SOCK_STREAM) as sock:  # TCP socket
                    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Details later
                    sock.bind((HOST, PORT))  # Claim messages sent to port "PORT"
                    sock.listen(1)  # Server only supports a single 3-way handshake at a time
                    print('Server:', sock.getsockname())  # Server IP and port
                    while True:
                        # if clientCount < 3: run the thread command and sc stuff
                        sc, _ = sock.accept()  # Wait until a connection is established
                        thread_list.append(Thread(target=playerControl, args=(sc, newBoard, playerNames, )).start())
            except Exception as details:
                print(str(details))


