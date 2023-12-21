#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import struct

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


# takes in a port sets up tcp on local host reads in a packed unsigned short called size, reads in size packed unsigned short inegers intoa list called numbers reads in another packed
# unsigned short integer n sends to the connected cliennt all integers in numbers that are divisible by 7 closes connection
def question19(portnumber: int):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind(('local host', portnumber))
        sock.listen(1)
        while True:
            sc, _ = sock.accept()
            with sc:
                try:
                    data = sc.recv(2)
                    size = struct.unpack('!H', data)
                    numbers = []
                    for i in range(size):
                        data = sock.recv(2)
                        unpackData = struct.unpack('!H', data)
                        numbers.append(unpackData)
                    nValue = sock.recv(2)
                    unpackNum = struct.unpack('!H', nValue)

                    divisibleNums = []

                    for value in numbers:
                        if value % unpackNum == 0:
                           sc.sendall(struct.pack('!H', value))
                except Exception as details:
                    print(str(details))

# my example of question 20
def question20(portNum: int):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind(('local host', portNum)) # might be able to just have port be '' same as in the actual server we use
        sock.listen(1)
        while True:
            sc, _ = sock.accept()
            with sc:
                numbers = []
                try:
                    data = question20buffer(sock, 2) # grab the data using buffer helper function
                    unpackData = struct.unpack('!h', data) # unpack the data as its still in byteform and we want int
                    if unpackData == -1:
                        break
                    numbers.append(unpackData)

                    pos = len(numbers)
                    while pos > 0:
                        pos = pos-1
                        sc.send(struct.pack('!h', numbers[pos]))

                except Exception as details:
                    print(str(details))
                return numbers

# this is really similar if not the same as headercheck from the working client / server
def question20buffer(current_socket: socket, expected_size: int)-> bytes:
    current_size = 0
    buffer = b''
    while current_size < expected_size:
        data = current_socket.recv(expected_size-current_size)
        buffer = buffer + data
        current_size = current_size + len(data)


def question20ExampleBuffer(current_socket:socket, expected_size: int)-> bytes:
    current_size = 0
    buffer = b''
    while current_size < expected_size:
        data = current_socket.recv(expected_size - current_size)
        buffer = buffer + data
        current_size = current_size + len(data)

# takes in a port sets up tcp server accepting on local host connection arrivng at that port,  readin a seried of signed short integers into a list called numbers. stops reading in integers
# as soon as -1 is encountered (-1 not saved to numbers) then sends the list in reverse order back to the client, closes connection retunrs the list.
def question20ExampleServer(port: int) -> [int]:
    numbers = []

    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    with sock:
        try:
            sock.bind(('local host', port))
            sock.listen(1)
            sc, name = sock.accept()
            with sc:
                while True:
                    number = struct.unpack('!h',question20ExampleBuffer(sock, 2))[0]
                    if number == -1:
                        break
                    numbers.append(number)

                pos = len(numbers)
                while pos > 0:
                    pos = pos - 1
                    sc.sendall(struct.pack('!h', numbers[pos]))
        except Exception as e:
            print(e)

    return numbers

#takes in a list of numbers (assume less than 255) and a port number, it then listens to that port on all network interfaces and waits for a client to connect. Once connected the function
# first sends out the length of the warray followed byh each list element all as packed unsigned bytes, exceptions caught.
def question21Send_list(numbersList: [int], port: int):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind(('local host', port)) # might be able to just have port be '' same as in the actual server we use
        sock.listen(1)
        while True:
            sc, _ = sock.accept()
            with sc:
                try:
                    arraylen = len(numbersList)
                    headerPack = struct.pack('!B', arraylen)
                    sc.sendall(headerPack)
                    for element in numbersList:
                        sc.sendall(struct.pack('!B', numbersList[element]))
                except Exception as e:
                    print(e)

# write a function that takes in a host ip or url and a port and then connects to the host at a given port. The function then receives the length of the liust n adn read in n
# numbers via the netowrk controller, all sent as packed bytes. The list is then retunre dot the called. Asyme the length and each number in the list are less thena 255
def question22receiveList(ip, port):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind((ip, port))  # might be able to just have port be '' same as in the actual server we use
        sock.listen(1)
        while True:
            sc, _ = sock.accept()
            with sc:
                numbers = []
                try:
                    length = sc.recv(1)
                    unpackLength = struct.unpack('!B', length)

                    for i in range(unpackLength):
                        data = question20buffer(sc, 2)
                        dataUP = struct.unpack('!B', data)
                        numbers.append(dataUP)

                    for i in range(unpackLength):
                        data = struct.pack('!B',numbers[i])
                        sc.sendall(data)

                except Exception as e:
                    print(e)

