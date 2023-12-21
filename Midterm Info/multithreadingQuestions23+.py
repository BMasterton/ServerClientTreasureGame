#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import struct
from math import ceil, floor, log2
from sys import argv


#question27() write a tcp server listening on port 12345 that expects an unsigned byte x, followed by a 1-byte operator + or * followed by another packed byte y. The server must then compute
#x+y or x*y depening on operator and return the result as an unsigned short followd by a newline
HOST = '127.0.0.1'
PORT = 12345

with socket(AF_INET, SOCK_STREAM) as sock:
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))  # might be able to just have port be '' same as in the actual server we use
    sock.listen(1)
    while True:
        sc, _ = sock.accept()
        with sc:
            xr = sc.recv(1)
            opr = sc.recv(1)
            yr = sc.recv(1)

            x = struct.unpack('!B', xr)
            op = opr.decode()
            y = struct.unpack('!B', yr)
            print(x, op, y)
            if op == '+':
                sc.sendall(struct.pack('!H', x+y))
            elif op == '*':
                sc.sendall(struct.pack('!H', x*y))
            sc.sendall(b'\n')




#1 expects a single positive int passes asa command line input, if no argyment more than 1 or non + int is passes print out error and termineate 2. program must only take a command line
# argument do not use input() do not read from file 3. other than error message the program must not print to screeen 4. the program must then determine the least number of bytes required
#to transmit the number revieced i step 1 5. the smallest supported number is 1 largest is 2^64-1 6. the program then transmits the number recieved in step 1 to the serverm poreface by thge
#nuymber of required bytes.
def question26():
    if len(argv) != 2:
        print(argv[0] + '<positive integer>')
        exit()

    num = 0
    try:
        num = int(argv[1])
    except ValueError:
        print(argv[0] + '<positive integer>')
        exit()

    if num <= 0:
        print(argv[0] + '<positive integer>')
        exit()

    if 2^64-1 < num:
        print('number too big')
        exit()
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        numBytes = ceil(floor(log2(num) + 1) /8)
        flag = '!'
        if numBytes ==1:
            flag += 'B'
            numBytes = 1
        elif numBytes <=2:
            flag += 'H'
            numBytes = 2
        elif numBytes <=4:
            flag += 'I'
            numBytes = 4
        elif numBytes <=9:
            flag += 'Q'
            numBytes = 8

        sock.sendall(struct.pack('!b', numBytes))
        sock.sendall(struct.pack(flag, num))


def question25Buf(current_socket: socket, expected_size: int):
    current_size = 0
    buffer = b''
    while current_size < expected_size:
        data = current_socket.recv(expected_size - current_size)
        if data == b'':
            break # or break in some cases like question 24 ans 23
        buffer = buffer + data
        current_size = current_size + len(data)


# python function called sum_bytes(socket). socket is a socket connetion which may or may not be valid. Using socket, the function must first receive an unsigned byte (call it offset)
# followed by an unsigned 4-byte number (called payload_size) followed by the number of bytes indicated in paylaod size (call it payload) the function must then add up every nth byte in the
#payload and return the result to the calling function. For all errors false is returned
def question25SumBytes(s: socket):
    try:
        offset = struct.unpack('!B', question25Buf(s, 1))[0]
        payload_size = struct.unpack('!I', question25Buf(s, 4))[0]
        if offset == 0 or offset > payload_size:
            return False

        payload = question25Buf(s, payload_size)
        if payload_size != len(payload):
            return False

        val = 0
        for i in range(0, payload_size, offset):
            val += payload[i]
        return val
    except Exception as e:
        print(e)


#using socket the function must first receive an unsigned 4 byte length field( payload size) fillowd by the num of bytes indicated in payload size (called payload) followed by another
# unsigned byte, (actual checksum). the function must then add all the bytes in the payload, mod 255 and compare the results to the atual checksum, if the checsums match true, else false
def question24check(s: socket):
        try:
            payload_size = struct.unpack('!I', get_buf(s, 4))[0]
            payload =  get_buf(s, payload_size)
            if payload_size != len(payload):
                return False
            actual_checksum = struct.unpack('!B', get_buf(s, 1))[0]
            total = 0
            for element in payload:
                total = total + element
            if total % 255 == actual_checksum:
                return True
            else:
                return False

        except Exception as e:
            print(e)


# using socket, the function must call first received a byte call it n, from the network, followed by another 4-byte number (payload size) followd by the number of bytes indicated by
#payload size. The function must then return to the caller not over the network the nth byte in the payload if this is not possible false is returned.
def question23Expedite(s: socket):
    try:
        n = struct.unpack('!B', get_buf(s , 1))[0] # so we are unpacking the returned value from the buffer in one step. the [0] is used to retrieve the unsigned nyte value that was
        # unpacked from the bytestring returned by get_buf
        payload_size = struct.unpack('!I', get_buf(s,4))[0]
        payload = get_buf(s, payload_size)
        if payload_size != len(payload):
            return False
        if n>= payload_size:
            return False
        return payload[n]
    except Exception as e:
        print(e)


def get_buf(current_socket: socket, expected_size: int) -> bytes:
    current_size = 0
    buffer = b''
    while current_size < expected_size:
        data = current_socket.recv(expected_size - current_size)
        if data == b'':
            return buffer # or break in some cases like question 24 ans 23
        buffer = buffer + data
        current_size = current_size + len(data)



HOST = '127.0.0.1'
PORT = 12345
NUM_CONNECTIONS = 1

with socket(AF_INET, SOCK_STREAM) as sock:
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))  # might be able to just have port be '' same as in the actual server we use
    sock.listen(1)
    while True:
        sc, _ = sock.accept()
        with sc:
             #result = question23Expedite(sc)
            result = question24check(sc)
            print(question25SumBytes(sc))
        if not result:
            print('False')
        else:
            print('Data', chr(result))


