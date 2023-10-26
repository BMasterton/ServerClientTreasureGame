from socket import socket, AF_INET, SOCK_STREAM
import struct
from sys import argv

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345
directionsString = ['U', 'D', 'L', 'R', 'Q', 'G']
directionsBytes = ['0010', '0011', '0100', '0110', '1000', '1111']
directionHeaderSize = 4
endBuffer = b'\x00';

if len(argv) != 2:
    print(argv[0] + ' <message>')
    exit()

#when the server sends over the client id, for the rest of the connection the clinet will send back
# every direction byte with the client number in bytes appended onto it. ie send should be like 00100100 still
def main():
    with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
        sock.connect((HOST, PORT)) # Initiates 3-way handshake
        print('Client:', sock.getsockname()) # Client IP and port
        player_id_binary = sock.recv(1) # getting info from the server for player id
        print(player_id_binary)
        play_id_int = int(player_id_binary)
        print(play_id_int)
        # sock.sendall(data) # Server IP and port implicit due to connect call
        print('clientNumber:', play_id_int)

        while True:
            directionInput = input("please enter a direction")
            if directionInput == directionsString[0]: #direction is U
                sendCommand = struct.pack("!H",directionsBytes[0]).join(play_id_int).join(endBuffer)
                sock.sendall(sendCommand)
                print(sendCommand)
            elif directionInput == directionsString[1]: #direction is D
                sendCommand = struct.pack("!H",directionsBytes[1]).join(play_id_int).join(endBuffer)
                sock.sendall(sendCommand)
                print(sendCommand)
            elif directionInput == directionsString[2]: #direction is L
                sendCommand = struct.pack("!H", directionsBytes[2]).join(play_id_int).join(endBuffer)
                sock.sendall(sendCommand)
                print(sendCommand)
            elif directionInput == directionsString[3]: # direction is R
                sendCommand = struct.pack("!H", directionsBytes[3]).join(play_id_int).join(endBuffer)
                sock.sendall(sendCommand)
                print(sendCommand)
            elif directionInput == directionsString[4]: # direction is Q
                sendCommand = struct.pack("!H", directionsBytes[4]).join(play_id_int).join(endBuffer)
                sock.sendall(sendCommand)
                print(sendCommand)
            elif directionInput == directionsString[5]: # direction is G
                sendCommand = struct.pack("!H", directionsBytes[5]).join(play_id_int).join(endBuffer)
                sock.sendall(sendCommand)
                print(sendCommand)


        # this is all the input info where we repeatedly as for input and then send that as bytes but will need to change it from the letter you get to hex asci to binray or something




main()