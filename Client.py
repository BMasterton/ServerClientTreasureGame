from socket import socket, AF_INET, SOCK_STREAM
from struct import unpack
import struct

from sys import argv

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345
directionsString = ['U', 'D', 'L', 'R', 'Q', 'G']
playerDirectionString = ['2', '3', '4', '6', '8', 'F']
directionsBytes = [b'\x0010', b'\x0011', b'\x0100', b'\x0110', b'\x1000', b'\x1111']
directionHeaderSize = 4
endBuffer = b'\x00'
HEADER_LEN = 2

# prints the scores from the incoming recV() function from server
def printScores(data):
    # scores = sock.recv(BUF_SIZE) sock.revc(BUF_SIZE)would be passed into the function
    score1 = unpack('!H', data[0:2])[0]
    score2 = unpack('!H', data[2:4])[0]
    print('Score1', score1)
    print('Score2', score2)
    return

#prints the board from the incoming recv() function from server
def printBoard(board):
    board.decode('utf-8')
    print(board)
    return

#does some math to get a correct player number
def playerInt(playerIntNumber):
    return playerIntNumber / 4

def get_buf(current_socket: socket, expected_size: int) -> bytes:
    current_size = 0
    buffer = b''
    while current_size < expected_size:
        data = current_socket.recv(expected_size - current_size)
        if data == b'':
            return buffer
        buffer = buffer + data
        current_size = current_size + len(data)

    return buffer

def get_data(client: socket) -> bytes:
    print('Client', client.getsockname(), 'waiting for data')
    header = get_buf(client, HEADER_LEN)
    print('Client', client.getsockname(), 'Header', header, header.hex())
    data_len = unpack('!H', header)[0]
    data = get_buf(client, data_len)
    print('Client', client.getsockname(), 'Data', data, data.hex())
    return data


#when the server sends over the client id, for the rest of the connection the clinet will send back
# every direction byte with the client number in bytes appended onto it. ie send should be like 00100100 still
def main():
    with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
        sock.connect((HOST, PORT)) # Initiates 3-way handshake

        print('Client:', sock.getsockname()) # Client IP and port
        get_data()
        player_id_binary = sock.recv(BUF_SIZE) # getting info from the server for player id
        print('BinaryID', player_id_binary)
        player_hex_id = player_id_binary.hex()
        print('HexID',player_hex_id)
        player_int_number = int.from_bytes(player_id_binary, byteorder='big')
        print(player_int_number)

        #player totallity checker
        if playerInt(player_int_number) > 2:
            print("too many clients closing the connection")
            return

        while True:
            directionInput = input("please enter a direction: ")
            if directionInput == directionsString[0]: #direction is U
                sock.sendall(bytes.fromhex(playerDirectionString[0] + str(player_int_number)))
                printScores(sock.recv(BUF_SIZE))
            elif directionInput == directionsString[1]: #direction is D
                sock.sendall(bytes.fromhex(playerDirectionString[1] + str(player_int_number)))
                printScores(sock.recv(BUF_SIZE))
            elif directionInput == directionsString[2]: #direction is L
                sock.sendall(bytes.fromhex(playerDirectionString[2] + str(player_int_number)))
                printScores(sock.recv(BUF_SIZE))
            elif directionInput == directionsString[3]: # direction is R
                sock.sendall(bytes.fromhex(playerDirectionString[3] + str(player_int_number)))
                printScores(sock.recv(BUF_SIZE))
            elif directionInput == directionsString[4]: # direction is Q
                # send info to server, print scores and board, quit
                sock.sendall(bytes.fromhex(playerDirectionString[4] + str(player_int_number)))
                printScores(sock.recv(BUF_SIZE))
                printBoard(sock.recv(BUF_SIZE))
                return
            elif directionInput == directionsString[5]: # direction is G
                # send info to sever, then print the returned scores and board
                sock.sendall(bytes.fromhex(playerDirectionString[5] + str(player_int_number)))
                printScores(sock.recv(BUF_SIZE))
                printBoard(sock.recv(BUF_SIZE))


main()
