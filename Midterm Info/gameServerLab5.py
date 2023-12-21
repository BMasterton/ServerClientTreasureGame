import struct

from View import display
from Board import Board
from threading import Semaphore, Thread
import random
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

playerDirections = ['U', 'D', 'L', 'R', 'Q', 'G'] # string version of all directions that can be picked
playerDirectionDecimals = [2, 3, 4, 6, 8, 15] # the decimal value of all of the directions changes from binary
BUF_SIZE = 1024
lock = Semaphore() #  lock is used on any shared variables that threaded connections may use, so like the newBoard or playerScores or Tile stuff etc.
playerCounter = 0 # keeps track of the connections

# General concept here, if we want to send something over to the client, we need to send it packed, if its not a string, and encoded in utf-8 if it is a string. This can then be decoded or unpacked on the other side so that we can grab the data, as the data needs to be transmitted in the form of binary.

# for example a string would be something like this: 'Hello World'.encode() or b'Hello World'
# if x ins  abinary string representing Hello World we can view its binary for using list(x)
# while an int or something else would be like this: score2_bin = struct.pack('!H', int(newBoard.printPlayerScore('2')))

#packs up all the points and headers for the points to send over to the client
def pointPack(newBoard): # This is a function that takes in the board, as we need the board to get the scores were gong to pack
    score1_bin = struct.pack('!H', int(newBoard.printPlayerScore('1'))) #because we want to send this data over we need it packed, and what this is saying is that we create a packed struct, the first param is the type it will sent as so an unsigned int here, and the second is the int its going to pack as an unsigned int.
    score2_bin = struct.pack('!H', int(newBoard.printPlayerScore('2')))
    scores_len = 4 #, we know that each score is two bytes, as that’s what an unsigned short is, so we can just double it we then get the packed version of it
    scores_header = struct.pack('!H', scores_len) # headers are something that we added in the lab, lets say you only want to receive a certain amount of data each time, well to do that we can send over a bunch of data and grab parts of it at a time. So we send over data saying this is the length of the coming data, and then heres the data. So we make the length an unsigned short pack here too.
    return scores_header + score1_bin + score2_bin #Luckily we can just add all the packed data to each other and send it all as one so were just adding the heeader first, and then the other two unsigned ints. This is a bit unique as were sending two separate length items in the same package, so the length is for both of them together, and in the client we can take it apart

#takes in a newboard and returns the packed version of the board with the header length prepended
def boardPack(newBoard):
    payload = newBoard.boardString().encode('utf-8') #  as this is just a string we can take the string and .encode() it, packing it and encoding it make it binary so we can add them
    payload_len = len(payload) # and we always want the length of the packed info.
    payload_header = struct.pack('!H', payload_len) # packed version of the length
    return payload_header + payload # returning the packed version of the length concatted with the packed version of the data we encoded

#takes in the byte string representing the player and returns the header length and player byte string
def playerPack(data):
# data here is in a bytestring, so the form it needs to be to be transmitted, so we don’t need to encode or pack it
    data_length = struct.pack('!H', len(data)) #length does need to be packed thought and we make it an unsigned short
    data_to_send = data_length + data
    return data_to_send


def playerMoveData(newBoard, playerInputDirection, playerId):
    if playerInputDirection not in playerDirections:
        raise Exception('Must give a valid direction or quit')
    newBoard.move_player(str(playerId), playerInputDirection)
    display(newBoard)

# Main thread function that deals with all logic for the boards and players
def playerControl(sc, newBoard, playerNames):
    global playerCounter
    playerId=0 #unique connection variable if we create this outside the Socket (sc) then for each unique connection we can assign it
    with sc: # this is important, with sc is with sock, each sc is its own multithread connection, so everyting under this with sc, will happen for each connection uniquely
# all of this is the initial step where we send over the player id,
        if playerCounter < 4: # setting player with playerCounter
            playerCounter += 1
        if playerCounter == 1:
            #trying to somehow get each connections value
            playerId = 1
            data = b'\x01' # data representing player 1, transformed in the client to be an int this is done in binary string hex form
            sc.sendall(playerPack(data)) #sending player data to the client
        elif playerCounter == 2:
            playerId = 2
            data = b'\x02'
            sc.sendall(playerPack(data))
        elif playerCounter == 3: # this player will still get sent through and cause the client to close
            playerId = 3
            data = b'\x03'
            sc.sendall(playerPack(data))
            quit(1)

        while True: # keep getting data from client, wait for data
            print('Client:', sc.getpeername())  # Client IP and port
            data = sc.recv(BUF_SIZE) # Receives info from the client as directions this is where we are always getting data from in the server side, surely this could be done differently or getting different data depending on the length and type or something
            print('data from recv', data)
            data2 = list(data) #  ok so technically we could also just unpack the data here as an unsigned short I believe as we are trying to get the int value of the hex passed through opposote to the way we did it with the player number. But we can also do it this way
            my_byte = data2[0] # We take the list of data we receive and we grab the first byte , depeding on the length of the data we get here and what we want from it we need to mask it, so if the number was 0010 we mask it by 1's in all spots or 15, if its 00100100 and we want the first 4 digits, we mask by 240 or 11110000 if we want the middle two we need to do it by 00001100 or 12 and so on. Once we have that num we then need to bit shift it, so for the 00100100 example we would need to shift it >> 4 or if it’s the middle shift it by 2. Example first_four_full = my_byte&240; first_four_only = first_four_full >>4
            print('my_byte', my_byte)
            first_four_full = my_byte & 15
            print('firstFourFull',first_four_full)
            if first_four_full == playerDirectionDecimals[0]:  # direction Up
                playerInputDirection = playerDirections[0]
                playerMoveData(newBoard, playerInputDirection, playerId)
                sc.sendall(pointPack(newBoard)) # send the returned value gotten from pointPack
            elif first_four_full == playerDirectionDecimals[1]:  # direction Down
                playerInputDirection = playerDirections[1]
                playerMoveData(newBoard, playerInputDirection, playerId)
                sc.sendall(pointPack(newBoard))
            elif first_four_full == playerDirectionDecimals[2]:  # direction Left
                playerInputDirection = playerDirections[2]
                playerMoveData(newBoard, playerInputDirection, playerId)
                sc.sendall(pointPack(newBoard))
            elif first_four_full == playerDirectionDecimals[3]:  # direction Right
                playerInputDirection = playerDirections[3]
                playerMoveData(newBoard, playerInputDirection, playerId)
                sc.sendall(pointPack(newBoard))
            elif first_four_full == playerDirectionDecimals[
                4]:  # when Q is received run send the scores of 1 and then 2 as shorts, send gameboard then itll run the quit command
                playerInputDirection = playerDirections[4]
                sc.sendall(pointPack(newBoard)) #i send these seperately so you need to do the header recv and then data recv twice
                sc.sendall(boardPack(newBoard))
                playerMoveData(newBoard, playerInputDirection, playerId)
                break
            elif first_four_full == playerDirectionDecimals[
                5]:  # when G is hit, print the scores, print the board, and then transmit the board
                playerInputDirection = playerDirections[5]
                playerMoveData(newBoard, playerInputDirection, playerId)
                with lock:
                    newBoard.printScore() # anything that is accessing newBoard and doing something on newboard we need to lock it so that its consistent
                display(newBoard)
                sc.sendall(pointPack(newBoard))
                sc.sendall(boardPack(newBoard))

class Game:
    def __init__(self):
        pass

    def start(self):
        newBoard = Board(5, 10, 5, 10, 2)  # creating the new boar
        playerNames = ["1", "2"]  # list of players that will be added
        HOST = ''
        PORT = 12345
        thread_list = [] # this is gong to be the list of threads that we have, in our case client connections

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
                    sock.bind((HOST, PORT))  # Claim messages sent to port "PORT" have to pass in a single argument that is a tuple containing host and port
                    sock.listen(1)  # Server only supports a single 3-way handshake at a time
                    print('Server:', sock.getsockname())  # Server IP and port
                    while True: # keep doing this as we have many connections to make and will keep allowing more connections and therefore threads to be created
                        sc, _ = sock.accept()  # Wait until a connection is established
                        # Creating the threads for sc, so we need to
                        thread_list.append(Thread(target=playerControl, args=(sc, newBoard, playerNames, )).start()) # Here we are creating the threads, and you can see that we append them to a list, and the call Thread(where the target is the function you want the threads to run, the parent running function for the treads action, and the args is what you pass to that function.
# Something to note here, is that in our function since we can just add clients when we want, we can start it immediately, so the unique threads are created for each client connection, in some other cases you don’t want to do this as you want them to all start at the same time. Like a thread that just counts to a million. If you had 5 threads you might want them to start at the same time. So once they are all made, you can start them with thread_list[-1].start()
                for t in thread_list:
                    t.join()  # kill command need the children to be killed before main ends, should be called automatically once the functions job is completed. .join() is the reap command.
            except Exception as details:
                print(str(details))
