from socket import socket, AF_INET, SOCK_STREAM
from struct import unpack
import struct

from sys import argv

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345
directionsString = ['U', 'D', 'L', 'R', 'Q', 'G']
playerDirectionString = ['2', '3', '4', '6', '8', '15']
directionsBytes = [b'\x0010', b'\x0011', b'\x0100', b'\x0110', b'\x1000', b'\x1111']
directionHeaderSize = 4
endBuffer = b'\x00'

#added from the test_server
HEADER_LEN = 2

PLAYER1 = '4'
PLAYER1_STR = '1'
PLAYER2 = '8'
PLAYER2_STR = '2'

first_run = True
connections = {}


# constants added from the constants file
CMD_MASK = 0b11110000
UP = 0b00100000
LEFT = 0b01000000
RIGHT = 0b01100000
DOWN = 0b00110000
QUIT = 0b10000000
GET = 0b11110000

PLAYER_MASK = 0b00001100
CONST_PLAYER1 = 0b0100
CONST_PLAYER2 = 0b1000
PLAYER1_NAME = '1'
PLAYER2_NAME = '2'

ERROR = b'E'
OK = b'O'

def printScores(data):
    # scores = sock.recv(BUF_SIZE) sock.revc(BUF_SIZE)would be passed into the function
    score1 = unpack('!H', data[0:2])[0]
    score2 = unpack('!H', data[2:4])[0]
    print('Score1', score1)
    print('Score2', score2)


#when the server sends over the client id, for the rest of the connection the clinet will send back
# every direction byte with the client number in bytes appended onto it. ie send should be like 00100100 still
def main():
    with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
        sock.connect((HOST, PORT)) # Initiates 3-way handshake

        print('Client:', sock.getsockname()) # Client IP and port
        player_id_binary = sock.recv(BUF_SIZE) # getting info from the server for player id
        print('BinaryID', player_id_binary)
        player_hex_id = player_id_binary.hex()
        print('HexID',player_hex_id)
        player_int_number = int.from_bytes(player_id_binary, byteorder='big')
        print(player_int_number)
        # play_id_int = int(player_id_binary)
        # print(play_id_int)
        # # sock.sendall(data) # Server IP and port implicit due to connect call
        # print('clientNumber:', play_id_int)
        #player totallity checker
        if player_int_number/4 > 2:
            print("too many clients closing the connection")
            return

        while True:
            directionInput = input("please enter a direction: ")
            if directionInput == directionsString[0]: #direction is U
                # actually want to use put_data, to send all data to the server
                # put_data('2' + player_hex_id)
                # byteString = directionsBytes[0] + player_id_binary + endBuffer # making a binary string of the command info
                # #sendCommand = struct.pack("!H",directionsBytes[0]).join(player_id_binary).join(endBuffer)
                # print('bytes', byteString)
                # sock.sendall(bytes.fromhex('2' + player_hex_id))
                sock.sendall(bytes.fromhex(playerDirectionString[0] + str(player_int_number)))
                #not working
                scores = sock.recv(BUF_SIZE)
                # printScores(sock.recv(BUF_SIZE))

                score1 = unpack('!H', scores[0:2])[0]
                score2 = unpack('!H', scores[2:4])[0]
                print('Score1', score1)
                print('Score2', score2)

                board = sock.recv(BUF_SIZE)
                board.decode('utf-8')
                print(board)

            elif directionInput == directionsString[1]: #direction is D
                # sendCommand = struct.pack("!H",directionsBytes[1]).join(player_id_binary).join(endBuffer)
                # sock.sendall(sendCommand)
                # print(sendCommand)
                sock.sendall(bytes.fromhex(playerDirectionString[1] + str(player_int_number)))
            elif directionInput == directionsString[2]: #direction is L
                # sendCommand = struct.pack("!H", directionsBytes[2]).join(player_id_binary).join(endBuffer)
                # sock.sendall(sendCommand)
                # print(sendCommand)
                sock.sendall(bytes.fromhex(playerDirectionString[2] + str(player_int_number)))
            elif directionInput == directionsString[3]: # direction is R
                # sendCommand = struct.pack("!H", directionsBytes[3]).join(player_id_binary).join(endBuffer)
                # sock.sendall(sendCommand)
                # print(sendCommand)
                sock.sendall(bytes.fromhex(playerDirectionString[3] + str(player_int_number)))
            elif directionInput == directionsString[4]: # direction is Q
                # sendCommand = struct.pack("!H", directionsBytes[4]).join(player_id_binary).join(endBuffer)
                # sock.sendall(sendCommand)
                # print(sendCommand)
                sock.sendall(bytes.fromhex(playerDirectionString[4] + str(player_int_number)))
                scores = sock.recv(BUF_SIZE)
                score1 = unpack('!H', scores[0:2])[0]
                score2 = unpack('!H', scores[2:4])[0]
                print('Score1', score1)
                print('Score2', score2)
                board = sock.recv(BUF_SIZE)
                board.decode('utf-8')
                print(board)
                return
                #gonna need to recieve the scores and board and print them. them return so the connection dies
            elif directionInput == directionsString[5]: # direction is G
                # sendCommand = struct.pack("!H", directionsBytes[5]).join(player_id_binary).join(endBuffer)
                # sock.sendall(sendCommand)
                # print(sendCommand)
                sock.sendall(bytes.fromhex(playerDirectionString[5] + str(player_int_number)))




        # this is all the input info where we repeatedly as for input and then send that as bytes but will need to change it from the letter you get to hex asci to binray or something




main()