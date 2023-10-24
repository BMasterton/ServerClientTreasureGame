from socket import socket, AF_INET, SOCK_STREAM
from sys import argv

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345
DirectionsString = ['U', 'D', 'L', 'R', 'Q', 'G']
DirectionsBytes = ['0010', '0011', '0100', '0110', '1000', '1111']
DirectionHeaderSize = 4

if len(argv) != 2:
    print(argv[0] + ' <message>')
    exit()

with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
    sock.connect((HOST, PORT)) # Initiates 3-way handshake
    print('Client:', sock.getsockname()) # Client IP and port
    data = argv[1].encode('utf-8') # Convert command line arg to binary
    direction = input('PLease enter a direction')
    while direction not in DirectionsString:
        direction = input('Not a valid entry, please try again')
    sock.sendall(data) # Server IP and port implicit due to connect call
    reply = sock.recv(BUF_SIZE) # recvfrom not needed since address known
    print('Reply:', reply)