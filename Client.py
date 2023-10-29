from socket import socket, AF_INET, SOCK_STREAM
from struct import unpack
import struct

from sys import argv

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345
directionsString = ['U', 'D', 'L', 'R', 'Q', 'G']
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


# gets the buffer size of the data being sent through and returns it in bytes
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

#i think this just sends data and then also gets data at the same time
def put_data(data: str) -> bytes:
    client = connections[data[-1]]
    encoded_data = bytes.fromhex(data)
    print('Client', client.getsockname(), 'sending', data, '(', encoded_data.hex(), ')')
    client.sendall(encoded_data)
    response = get_data(client)
    return response

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
        # play_id_int = int(player_id_binary)
        # print(play_id_int)
        # # sock.sendall(data) # Server IP and port implicit due to connect call
        # print('clientNumber:', play_id_int)

        while True:
            directionInput = input("please enter a direction ")
            if directionInput == directionsString[0]: #direction is U
                # actually want to use put_data, to send all data to the server
                put_data('2' + player_hex_id)
                # byteString = directionsBytes[0] + player_id_binary + endBuffer # making a binary string of the command info
                # #sendCommand = struct.pack("!H",directionsBytes[0]).join(player_id_binary).join(endBuffer)
                # print('bytes', byteString)
                # sock.sendall(byteString)
            elif directionInput == directionsString[1]: #direction is D
                sendCommand = struct.pack("!H",directionsBytes[1]).join(player_id_binary).join(endBuffer)
                sock.sendall(sendCommand)
                print(sendCommand)
            elif directionInput == directionsString[2]: #direction is L
                sendCommand = struct.pack("!H", directionsBytes[2]).join(player_id_binary).join(endBuffer)
                sock.sendall(sendCommand)
                print(sendCommand)
            elif directionInput == directionsString[3]: # direction is R
                sendCommand = struct.pack("!H", directionsBytes[3]).join(player_id_binary).join(endBuffer)
                sock.sendall(sendCommand)
                print(sendCommand)
            elif directionInput == directionsString[4]: # direction is Q
                sendCommand = struct.pack("!H", directionsBytes[4]).join(player_id_binary).join(endBuffer)
                sock.sendall(sendCommand)
                print(sendCommand)
            elif directionInput == directionsString[5]: # direction is G
                sendCommand = struct.pack("!H", directionsBytes[5]).join(player_id_binary).join(endBuffer)
                sock.sendall(sendCommand)
                print(sendCommand)


        # this is all the input info where we repeatedly as for input and then send that as bytes but will need to change it from the letter you get to hex asci to binray or something




main()