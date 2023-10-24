from socket import socket, AF_INET, SOCK_STREAM
import struct
from sys import argv

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345
directionsString = ['U', 'D', 'L', 'R', 'Q', 'G']
directionsBytes = ['0010', '0011', '0100', '0110', '1000', '1111']
directionHeaderSize = 4

if len(argv) != 2:
    print(argv[0] + ' <message>')
    exit()


def main():
    with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
        sock.connect((HOST, PORT)) # Initiates 3-way handshake
        print('Client:', sock.getsockname()) # Client IP and port
        player_id_binary = sock.recv(2)
        player_id_hex = struct.unpack('!H', player_id_binary)
        print(player_id_hex)
        # sock.sendall(data) # Server IP and port implicit due to connect call
        reply = sock.recv(BUF_SIZE) # recvfrom not needed since address known
        print('Reply:', reply)

        while True:
            try:
                directionInput = input("please enter a direction")
                if directionInput not in directionsString:
                    raise Exception("Incorrect command entered, please try again")
            except Exception as details:
                print(str(details))
        # this is all the input info where we repeatedly as for input and then send that as bytes but will need to change it from the letter you get to hex asci to binray or something




main()