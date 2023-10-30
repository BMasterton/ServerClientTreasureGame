import struct

from View import display
from Board import Board
from threading import Semaphore, Thread
import random
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

playerDirections = ['U', 'D', 'L', 'R', 'Q', 'G'] # string version of all directions that can be picked
playerDirectionDecimals = [2, 3, 4, 6, 8, 15] # the decimal value of all of the directions changes from binary
BUF_SIZE = 1024
lock = Semaphore()
playerCounter = 0 # keeps track of the connections

#packs up all the points and headers for the points to send over to the client
def pointPack(newBoard):
    score1_bin = struct.pack('!H', int(newBoard.printPlayerScore('1')))
    score2_bin = struct.pack('!H', int(newBoard.printPlayerScore('2')))
    scores_len = 4
    scores_header = struct.pack('!H', scores_len)
    return scores_header + score1_bin + score2_bin

#takes in a newboard and returns the packed version of the board with the header length prepended
def boardPack(newBoard):
    payload = newBoard.boardString().encode('utf-8')
    payload_len = len(payload)
    payload_header = struct.pack('!H', payload_len)
    return payload_header + payload

#takes in the byte string representing the player and returns the header length and player byte string
def playerPack(data):
    data_length = struct.pack('!H', len(data))
    data_to_send = data_length + data
    return data_to_send

# Main thread function that deals with all logic for the boards and players
def playerControl(sc, newBoard, playerNames):
    global playerCounter
    playerId=0 #unique connection variable
    with sc:
        if playerCounter < 4: # setting player with playerCounter
            playerCounter += 1
        if playerCounter == 1:
            #trying to somehow get each connections value
            playerId = 1
            data = b'\x04' # data representing player 1, transformed in the client to be an int
            sc.sendall(playerPack(data)) #sending player data to the client
        elif playerCounter == 2:
            playerId = 2
            data = b'\x08'
            sc.sendall(playerPack(data))
        elif playerCounter == 3: # this player will still get sent through and cause the client to close
            playerId = 3
            data = b'\x12'
            sc.sendall(playerPack(data))
            sc.close()

        while True:
            print('Client:', sc.getpeername())  # Client IP and port
            data = sc.recv(BUF_SIZE) # Receives info from the client as directions
            data2 = list(data)
            my_byte = data2[0]
            #this mask isnt working and its returning 0 instead of what it should
            first_four_full = my_byte & 15
            print('firstFourFull',first_four_full)
            if first_four_full == playerDirectionDecimals[0]:  # direction Up
                playerInputDirection = playerDirections[0]
                sc.sendall(pointPack(newBoard))
            elif first_four_full == playerDirectionDecimals[1]:  # direction Down
                playerInputDirection = playerDirections[1]
                sc.sendall(pointPack(newBoard))
            elif first_four_full == playerDirectionDecimals[2]:  # direction Left
                playerInputDirection = playerDirections[2]
                sc.sendall(pointPack(newBoard))
            elif first_four_full == playerDirectionDecimals[3]:  # direction Right
                playerInputDirection = playerDirections[3]
                sc.sendall(pointPack(newBoard))
            elif first_four_full == playerDirectionDecimals[
                4]:  # when Q is received run send the scores of 1 and then 2 as shorts, send gameboard then itll run the quit command
                playerInputDirection = playerDirections[4]
                sc.sendall(pointPack(newBoard))
                sc.sendall(boardPack(newBoard))
                break
            elif first_four_full == playerDirectionDecimals[
                5]:  # when G is hit, print the scores, print the board, and then transmit the board
                playerInputDirection = playerDirections[5]
                with lock:
                    newBoard.printScore() # anything that is accessing newBoard and doing something on newboard we need to lock it so that its consistent
                display(newBoard)
                sc.sendall(boardPack(newBoard))
            print('Data', data)  # printing the data we receive

            # making sure the directions and players are allowed choices or reject
            if playerInputDirection not in playerDirections:
                raise Exception('Must give a valid direction or quit')
            #playerInputPlayer needs to be the connection number which would be 1 or 2
            newBoard.move_player(playerId, playerInputDirection)
            display(newBoard)


class Game:
    def __init__(self):
        pass

    def start(self):
        newBoard = Board(5, 10, 5, 10, 2)  # creating the new boar
        playerNames = ["1", "2"]  # list of players that will be added
        HOST = ''
        PORT = 12345
        thread_list = []

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



        while True:
            try:
                display(newBoard) #displays the original board
                with socket(AF_INET, SOCK_STREAM) as sock:  # TCP socket
                    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Details later
                    sock.bind((HOST, PORT))  # Claim messages sent to port "PORT"
                    sock.listen(1)  # Server only supports a single 3-way handshake at a time
                    print('Server:', sock.getsockname())  # Server IP and port
                    while True:
                        sc, _ = sock.accept()  # Wait until a connection is established
                        # Creating the threads for sc
                        thread_list.append(Thread(target=playerControl, args=(sc, newBoard, playerNames, )).start())
                for t in thread_list:
                    t.join()  # kill command need the children to be killed before main ends
            except Exception as details:
                print(str(details))


