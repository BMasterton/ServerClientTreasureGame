#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
BUF_SIZE = 1024
HOST = ''
PORT = 65432
with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
    sock.listen(1) # Server only supports a single 3-way handshake at a time

    print('Server:', sock.getsockname()) # Server IP and port

    while True:
        #this runs once for every conenction...
        sc, _ = sock.accept() # Wait until a connection is established
        with sc: # with sc will take care of closing the socket, I don't have to
            print('Client:', sc.getpeername()) # Client IP and port
            data = sc.recv(BUF_SIZE) # recvfrom not needed since address known
            print(data)
            sc.sendall(data) # Client IP and port implicit due to accept call


#buffer for somethings
def question19Buf(current_socket: socket, expected_size: int):
    current_size = 0
    buffer = b''
    while current_size < expected_size:
        data = current_socket.recv(expected_size - current_size)
        if data == b'':
            return buffer
        buffer = buffer + data
        current_size = current_size + len(data)
    return buffer

#more buffers
def question20buffer(current_socket: socket, expected_size: int)-> bytes:
    current_size = 0
    buffer = b''
    while current_size < expected_size:
        data = current_socket.recv(expected_size-current_size)
        buffer = buffer + data
        current_size = current_size + len(data)

# more buffers
def question25Buf(current_socket: socket, expected_size: int):
    current_size = 0
    buffer = b''
    while current_size < expected_size:
        data = current_socket.recv(expected_size - current_size)
        if data == b'':
            break # or break in some cases like question 24 ans 23
        buffer = buffer + data
        current_size = current_size + len(data)


