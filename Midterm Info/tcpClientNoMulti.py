#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM
import struct
BUF_SIZE = 1024
HOST = '127.0.0.1' #server MUST be listening on this ip - this is where we connect TO
PORT = 65432


def get_buf(current_socket: socket, expected_size: int):
    current_size = 0
    buffer = b''
    while current_size < expected_size:
        data = current_socket.recv(expected_size - current_size)
        if data == b'':
            break # or break in some cases like question 24 ans 23
        buffer = buffer + data
        current_size = current_size + len(data)

with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
    sock.connect((HOST, PORT)) # Initiates 3-way handshake
    #connect accepts a single argument that is a tuple
    payload_size = struct.unpack(get_buf(sock, 1)) # if we need a header we would use this header to get the length of what the payload should be
    payload = get_buf(sock, payload_size) # this doesn't need to be unpacked as its fine to use in bytestring i guess

    sock.sendall("<data>") # Server IP and port implicit due to connect call, should be packed or encoded to send, or send as bytestring

