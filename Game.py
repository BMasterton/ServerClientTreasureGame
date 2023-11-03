import asyncio
import struct

from View import display
from Board import Board
from threading import Semaphore
import random
from asyncio import run, start_server, StreamReader, StreamWriter

playerDirections = ['U', 'D', 'L', 'R', 'Q', 'G'] # string version of all directions that can be picked
playerDirectionDecimals = [2, 3, 4, 6, 8, 15] # the decimal value of all of the directions changes from binary
BUF_SIZE = 1024
lock = Semaphore()
playerCounter = 0 # keeps track of the connections


#packs up all the points and headers for the points to send over to the client
def pointPack(newBoard):
    score1_bin = struct.pack('!H', int(newBoard.printPlayerScore('1'))) # packing the scores as unsigned ints
    score2_bin = struct.pack('!H', int(newBoard.printPlayerScore('2')))
    scores_len = 4
    scores_header = struct.pack('!H', scores_len) # packing the length as unsigned int
    return scores_header + score1_bin + score2_bin # returning the value of all packed, header and points


#takes in a newboard and returns the packed version of the board with the header length prepended
def boardPack(newBoard):
    payload = newBoard.boardString().encode('utf-8') #encoding the boardstring in utf-8, same as packing but with a string
    payload_len = len(payload) # get the length of the string to be sent
    payload_header = struct.pack('!H', payload_len) # pack the header
    return payload_header + payload # return appended values


#takes in the byte string representing the player and returns the header length and player byte string
def playerPack(data):
    data_length = struct.pack('!H', len(data)) # pack the length of the playerid data
    data_to_send = data_length + data # concat it to the sending data
    return data_to_send

# Check to make sure direction is correct then runs move player and displays board for player
def playerMoveData(newBoard, playerInputDirection, playerId):
    if playerInputDirection not in playerDirections:
        raise Exception('Must give a valid direction or quit')
    newBoard.move_player(str(playerId), playerInputDirection) # move player on the board
    display(newBoard) # displays the board


class Game:
    def __init__(self):
        pass

    def start(self):
        self.newBoard = Board(5, 10, 5, 10, 2)  # creating the new boar
        playerNames = ["1", "2"]  # list of players that will be added
        HOST = ''
        PORT = 12345

        async def playerControl(reader: StreamReader, writer: StreamWriter) -> None:
            global playerCounter
            playerId = 0  # unique connection variable

            if playerCounter < 4:  # setting player with playerCounter
                playerCounter += 1
                # this can also be more dry. they all do the same thing
            if playerCounter == 1:
                playerId = 1
                data = b'\x01'  # data representing player 1, transformed in the client to be an int
                writer.write(playerPack(data))
                await writer.drain()
            elif playerCounter == 2:
                playerId = 2
                data = b'\x02'
                writer.write(playerPack(data))
                await writer.drain()
            elif playerCounter == 3:  # this player will still get sent through and cause the client to close
                playerId = 3
                data = b'\x03'
                writer.write(playerPack(data))
                await writer.drain()
                quit(1)


            while True:
                addr = writer.get_extra_info('peername') # grabbing extra peername data from writer
                print('Address', addr)
                data = await reader.read(BUF_SIZE) # retrieving data from the reader
                print('data from recv', data)
                data2 = list(data)
                my_byte = data2[0]
                print('my_byte', my_byte)
                first_four_full = my_byte & 15 # bit masking the direction data which is always 4 bits
                print('firstFourFull', first_four_full)
                # since all the directions do the same thing theres a more dry way to do it
                if first_four_full == playerDirectionDecimals[0]:  # direction Up
                    playerInputDirection = playerDirections[0]
                    playerMoveData(self.newBoard, playerInputDirection, playerId) # Moving the player
                    writer.write(pointPack(self.newBoard)) # writing data to client, with packed data
                    await writer.drain() # wait until sucessfull transfer compelted
                elif first_four_full == playerDirectionDecimals[1]:  # direction Down
                    playerInputDirection = playerDirections[1]
                    playerMoveData(self.newBoard, playerInputDirection, playerId)
                    writer.write(pointPack(self.newBoard))
                    await writer.drain()
                elif first_four_full == playerDirectionDecimals[2]:  # direction Left
                    playerInputDirection = playerDirections[2]
                    playerMoveData(self.newBoard, playerInputDirection, playerId)
                    writer.write(pointPack(self.newBoard))
                    await writer.drain()
                elif first_four_full == playerDirectionDecimals[3]:  # direction Right
                    playerInputDirection = playerDirections[3]
                    playerMoveData(self.newBoard, playerInputDirection, playerId)
                    writer.write(pointPack(self.newBoard))
                    await writer.drain()
                elif first_four_full == playerDirectionDecimals[
                    4]:  # when Q is received run send the scores of 1 and then 2 as shorts, send gameboard then itll run the quit command
                    playerInputDirection = playerDirections[4]
                    writer.write(pointPack(self.newBoard)) # send the points
                    await writer.drain()
                    writer.write(boardPack(self.newBoard)) # send the board
                    await writer.drain()
                    playerMoveData(self.newBoard, playerInputDirection, playerId)
                    return
                elif first_four_full == playerDirectionDecimals[
                    5]:  # when G is hit, print the scores, print the board, and then transmit the board
                    playerInputDirection = playerDirections[5]
                    playerMoveData(self.newBoard, playerInputDirection, playerId)
                    with lock:
                        self.newBoard.printScore()  # anything that is accessing newBoard and doing something on newboard we need to lock it so that its consistent
                    display(self.newBoard)
                    writer.write(pointPack(self.newBoard)) # send the points
                    await writer.drain()
                    writer.write(boardPack(self.newBoard)) # send the board
                    await writer.drain()


        # goes over all the players in playerNames and looks at a random  x and y pos so it can add them, if that position is
        # not a "." then it will try again until it can, if the spot is taken it will let the player know
        for player in playerNames:
            randPlayerXPos = random.randrange(0, 10)
            randPlayerYPos = random.randrange(0, 10)
            # making sure that if the tile already has a player or a treaure, another player cant spawn on them
            while self.newBoard.board[randPlayerXPos][randPlayerYPos].get_treasure() is not None or self.newBoard.board[randPlayerXPos][randPlayerYPos].get_player_from_current_tile() is not None:
                randPlayerXPos = random.randrange(0, 10)
                randPlayerYPos = random.randrange(0, 10)
            self.newBoard.add_player(player, randPlayerXPos, randPlayerYPos)

        display(self.newBoard)

        # main function who will run the playerControl function, this will open up asyncio connection to client for however many clients
        async def main() -> None:
            server = await asyncio.start_server(playerControl, HOST, PORT)
            await server.serve_forever()


        run(main())