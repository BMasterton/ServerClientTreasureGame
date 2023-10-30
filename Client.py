from socket import socket, AF_INET, SOCK_STREAM
from struct import unpack
import struct

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345
directionsString = ['U', 'D', 'L', 'R', 'Q', 'G']
playerDirectionString = ['2', '3', '4', '6', '8', 'F']
directionsBytes = [b'\x0010', b'\x0011', b'\x0100', b'\x0110', b'\x1000', b'\x1111']
HEADER_LEN = 2

# prints the scores from the incoming recV() function from server
def printScores(data):
    score1 = unpack('!H', data[0:2])[0] #2:4 or 4:6 if 4 bytes is the number
    score2 = unpack('!H', data[2:4])[0] #4:6 nut maune 6:8
    print('Score1', score1)
    print('Score2', score2)
    return

#prints the board from the incoming recv() function from server
def printBoard(board):
    board.decode('utf-8')
    print(board)
    return

def headerCheck( data):  # there will always be two initial bytes, which are the length header
    if len(data) != 2:
        raise Exception('Could not recieve Length of header!')
    num_bytes = struct.unpack('!H', data)[0]  # unpack Data, and read the first (and only) unsigned int
    print('numBytes', num_bytes)
    bytes_read = 0
    bytes_from_server = b''
    while bytes_read < num_bytes:
        next_bytes = data.recv( num_bytes - bytes_read)
        bytes_read += len(next_bytes)
        bytes_from_server += next_bytes
    print(bytes_from_server)
    return bytes_from_server

#does some math to get a correct player number
def playerInt(playerIntNumber):
    return playerIntNumber / 4


#when the server sends over the client id, for the rest of the connection the clinet will send back
# every direction byte with the client number in bytes appended onto it. ie send should be like 00100100 still
def main():
    with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
        sock.connect((HOST, PORT)) # Initiates 3-way handsha
        data_length_bytes = sock.recv(HEADER_LEN)
        if len(data_length_bytes) != 2:
            raise Exception('Could not recieve Length of header!')
        num_bytes = struct.unpack('!H', data_length_bytes)[0]  # unpack Data, and read the first (and only) unsigned int
        print('numBytes', num_bytes)
        bytes_read = 0
        bytes_from_server = b''
        while bytes_read < num_bytes:
            next_bytes = sock.recv(num_bytes - bytes_read)
            bytes_read += len(next_bytes)
            bytes_from_server += next_bytes
            int_from_server = int.from_bytes(bytes_from_server, byteorder='big')
            print('Intfromserver', int_from_server)
        print('bytes from server',bytes_from_server)

        print('Client:', sock.getsockname()) # Client IP and port
        print('BinaryID', bytes_from_server)
        player_hex_id = bytes_from_server.hex()
        player_int_number = int.from_bytes(bytes_from_server, byteorder='big')
        print('Player ID', player_int_number)

        #player totallity checker
        if playerInt(int_from_server) > 2:
            print("too many clients closing the connection")
            return

        while True:
            directionInput = input("please enter a direction: ")
            if directionInput == directionsString[0]: #direction is U
                sock.sendall(directionsBytes[0] ) # sending the information back to the server
                data_length_bytes = sock.recv(HEADER_LEN) # getting the length of the server sent over data
                if len(data_length_bytes) != 2:
                    raise Exception('Could not recieve Length of header!')
                num_bytes = struct.unpack('!H', data_length_bytes)[0]  # unpack Data, and read the first (and only) unsigned int
                bytes_read = 0
                bytes_from_server = b''
                while bytes_read < num_bytes:
                    next_bytes = sock.recv(num_bytes - bytes_read)
                    bytes_read += len(next_bytes)
                    bytes_from_server += next_bytes
                    int_from_server = int.from_bytes(bytes_from_server, byteorder='big')

                printScores(sock.recv( num_bytes)) # print out the scores with the socket of the size returned from the header
            elif directionInput == directionsString[1]: #direction is D
                sock.sendall(bytes.fromhex(playerDirectionString[1] + str(player_int_number)))
                data_length_bytes = sock.recv(HEADER_LEN)
                print('datalengthbytesDirU', data_length_bytes)
                if len(data_length_bytes) != 2:
                    raise Exception('Could not recieve Length of header!')
                num_bytes = struct.unpack('!H', data_length_bytes)[
                    0]  # unpack Data, and read the first (and only) unsigned int
                print('numBytesDirectionU', num_bytes)
                bytes_read = 0
                bytes_from_server = b''
                while bytes_read < num_bytes:
                    next_bytes = sock.recv(num_bytes - bytes_read)
                    bytes_read += len(next_bytes)
                    bytes_from_server += next_bytes
                    int_from_server = int.from_bytes(bytes_from_server, byteorder='big')
                    print('IntfromserverDirectionU', int_from_server)
                print('bytes from serverDirectionU', bytes_from_server)

                printScores(sock.recv(num_bytes))
            elif directionInput == directionsString[2]: #direction is L
                sock.sendall(bytes.fromhex(playerDirectionString[2] + str(player_int_number)))
                data_length_bytes = sock.recv(HEADER_LEN)
                print('datalengthbytesDirU', data_length_bytes)
                if len(data_length_bytes) != 2:
                    raise Exception('Could not recieve Length of header!')
                num_bytes = struct.unpack('!H', data_length_bytes)[
                    0]  # unpack Data, and read the first (and only) unsigned int
                print('numBytesDirectionU', num_bytes)
                bytes_read = 0
                bytes_from_server = b''
                while bytes_read < num_bytes:
                    next_bytes = sock.recv(num_bytes - bytes_read)
                    bytes_read += len(next_bytes)
                    bytes_from_server += next_bytes
                    int_from_server = int.from_bytes(bytes_from_server, byteorder='big')
                    print('IntfromserverDirectionU', int_from_server)
                print('bytes from serverDirectionU', bytes_from_server)

                printScores(sock.recv(num_bytes))
            elif directionInput == directionsString[3]: # direction is R
                sock.sendall(bytes.fromhex(playerDirectionString[3] + str(player_int_number)))
                data_length_bytes = sock.recv(HEADER_LEN)
                print('datalengthbytesDirU', data_length_bytes)
                if len(data_length_bytes) != 2:
                    raise Exception('Could not recieve Length of header!')
                num_bytes = struct.unpack('!H', data_length_bytes)[
                    0]  # unpack Data, and read the first (and only) unsigned int
                print('numBytesDirectionU', num_bytes)
                bytes_read = 0
                bytes_from_server = b''
                while bytes_read < num_bytes:
                    next_bytes = sock.recv(num_bytes - bytes_read)
                    bytes_read += len(next_bytes)
                    bytes_from_server += next_bytes
                    int_from_server = int.from_bytes(bytes_from_server, byteorder='big')
                    print('IntfromserverDirectionU', int_from_server)
                print('bytes from serverDirectionU', bytes_from_server)

                printScores(sock.recv(num_bytes))
            elif directionInput == directionsString[4]: # direction is Q
                # send info to server, print scores and board, quit
                sock.sendall(bytes.fromhex(playerDirectionString[4] + str(player_int_number)))
                data_length_bytes = sock.recv(HEADER_LEN)
                print('datalengthbytesDirU', data_length_bytes)
                if len(data_length_bytes) != 2:
                    raise Exception('Could not recieve Length of header!')
                num_bytes = struct.unpack('!H', data_length_bytes)[
                    0]  # unpack Data, and read the first (and only) unsigned int
                print('numBytesDirectionU', num_bytes)
                bytes_read = 0
                bytes_from_server = b''
                while bytes_read < num_bytes:
                    next_bytes = sock.recv(num_bytes - bytes_read)
                    bytes_read += len(next_bytes)
                    bytes_from_server += next_bytes
                    int_from_server = int.from_bytes(bytes_from_server, byteorder='big')
                    print('IntfromserverDirectionU', int_from_server)
                print('bytes from serverDirectionU', bytes_from_server)

                printScores(sock.recv(num_bytes))
                printBoard(sock.recv(BUF_SIZE))
                return
            elif directionInput == directionsString[5]: # direction is G
                # send info to sever, then print the returned scores and board
                sock.sendall(bytes.fromhex(playerDirectionString[5] + str(player_int_number)))
                printScores(sock.recv(BUF_SIZE))
                printBoard(sock.recv(BUF_SIZE))


main()
