#!/usr/bin/python3.11

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Semaphore, Thread

HOST =''
PORT = 12345
NUM_CLIENTS=1

lock = Semaphore()
thread_list = []


def get_line(current_socket: socket) -> bytes:  # basically just starts with an empty byte string called buffer and keeps grabbing one byte of data, if its ever notihg or an end line  it gets returned
    buffer = b''
    while True:
        data = current_socket.recv(1)
        if data == b'' or data == b'\n':
            return buffer
        buffer += data


def contact_client(client_socket: socket):
    global total
    try:
        with client_socket:
            local_msg = get_line(client_socket)
    except Exception as details:
        print(details)


sock = socket(AF_INET, SOCK_STREAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(NUM_CLIENTS) # how many clients were allowed to have so here we can have just 1
while True:
    sc, _ = sock.accept()
    thread_list.append(Thread(target=contact_client, args=(sc,)).start()
