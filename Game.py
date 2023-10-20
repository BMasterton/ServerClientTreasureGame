import struct

from View import display
from Board import Board
from Tile import Tile
import random
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


class Game:
    def __init__(self):
        pass

    def start(self):
        newBoard = Board(3, 10, 5, 10, 2)  # creating the new boar
        randPlayerXPos = random.randrange(0, 10)  # creating initial random x and y coords
        randPlayerYPos = random.randrange(0, 10)
        playerNames = ["1", "2"]  # list of players that will be added
        playerDirections = ['U', 'D', 'L', 'R', 'Q', 'G']
        playerDirectionDecimals = [2, 3, 4, 6, 8, 15]

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
                            data2 = list(data)
                            my_byte = data2[0]
                            first_four_full = my_byte & 240
                            first_four_only = first_four_full >> 4
                            middle_two_full = my_byte & 12
                            middle_two_only = middle_two_full >> 2
                            if first_four_only == playerDirectionDecimals[0]:
                                playerInputDirection = playerDirections[0]
                            elif first_four_only == playerDirectionDecimals[1]:
                                playerInputDirection = playerDirections[1]
                            elif first_four_only == playerDirectionDecimals[2]:
                                playerInputDirection = playerDirections[2]
                            elif first_four_only == playerDirectionDecimals[3]:
                                playerInputDirection = playerDirections[3]
                            elif first_four_only == playerDirectionDecimals[
                                4]:  # when Q is received run send the scores of 1 and then 2 as shorts, send gameboard then itll run the quit command
                                playerInputDirection = playerDirections[4]
                                sc.sendall(struct.pack('!HH', newBoard.printPlayerScore('1'), newBoard.printPlayerScore('2')) )
                                sc.sendall(str(newBoard).encode())
                            elif first_four_only == playerDirectionDecimals[
                                5]:  # when G is hit, print the scores, print the board, and then transmit the board
                                newBoard.printScore()
                                sc.sendall(struct.pack('!HH', newBoard.printPlayerScore('1'), newBoard.printPlayerScore('2')) )
                                display(newBoard)
                                sc.sendall(str(newBoard).encode())
                            playerInputPlayer = str(middle_two_only)
                            # print('FFOnly', first_four_only)
                            # print('M2Only', middle_two_only)
                            print('Data', data)
                            sc.sendall(data)  # Client IP and port implicit due to accept call
                            # get value from user and make sure its an allowed input if not tell them and repeat until proper input
                            # this will all need to change to send and recieve bit info from the server that we send with echo, and that data we decrypt will be then used to check the playerinputdirectiopn adn
                            # playerinputname adn do all the checks and moves on etc
                            # playerInputDirection = input("(U)p (D)own (L)eft (R)ight (Q)uit \n")
                            # print("(U)p (D)own (L)eft (R)ight (Q)uit or (G)ameBoard \n") #feel like this should somehow go to the client but for now it can just be on the server
                            if playerInputDirection not in playerDirections:
                                raise Exception('Must give a valid direction or quit')
                            if playerInputPlayer not in playerNames:
                                raise Exception('value must be 1 or 2')
                            if playerInputPlayer == '1':
                                newBoard.move_player(playerNames[0], playerInputDirection)
                            elif playerInputPlayer == '2':
                                newBoard.move_player(playerNames[1], playerInputDirection)
                            display(newBoard)
            except Exception as details:
                print(str(details))


