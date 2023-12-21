#!/usr/bin/python3.11
import struct
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
BUF_SIZE = 1024
HOST = ''
PORT = 24680
with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
    sock.listen(1) # Server only supports a single 3-way handshake at a time

    print('Server:', sock.getsockname()) # Server IP and port

    #write a function that takes a valid socet connection, reads in the size of the message as a packed insigned long long from teh socket conection then reads in the message form the
    # same socket connection and finally returns the read in message in decoded form.
    def question18buf(current_socket:socket, expected_size: int):
        current_size = 0
        buffer = b''
        while current_size < expected_size:
            data = current_socket.recv(expected_size- current_size)
            buffer = buffer + data
            current_size = current_size + len(data)

    def question18(socket: socket):
        data = socket.recv(8)
        length = struct.unpack('!Q', data)
        bytes_read = 0
        bytes_from_server = b''
        while bytes_read < length:
            next_bytes = sock.recv(length - bytes_read)
            bytes_read += len(next_bytes)
            bytes_from_server += next_bytes
        return next_bytes.decode()



    #Write a function that takes in 4 params, a valid socket s, a byte string t, a number n, and a stop byte c. Sends n as a packed unsigned byte  via s , sends t vis s in chunks
    #seperated by c, or until reached the end of t.
    def question17(s: socket, t:bytes, n:int, c:bytes)-> None:
        s.sendall(struct.pack('!B', n))
        limit = len(t)
        last = 0
        for i in range(limit):
            if t[i] == c[0] or i == limit -1:
                s.sendall(t[last:i + 1])
                print(t[i], c[0], t[last:i+1])
                last = i + 1

    #write a function (1) takes two params, namely a valid socket connection and a stop character (2) reads a packed unsigned byte n from socket (3) reads in bytes from s until n copie
    # of stop char have been received, and (4) returns all bytes read from current socket including the last last found stop char
    def question16(current_socket: socket, stopcharacter):
        nValue = current_socket.recv(1) # recieve 1 unsigned byte to get the n value currently packed
        intNValue = struct.unpack('!B', nValue) # unpack that length data basically this is the header
        buffer = b''
        counter = 0
        while counter < intNValue:
            data = current_socket(1)
            if data == stopcharacter:
                counter += 1
            buffer = buffer + data
        return buffer




    # write a python function that takes in a socket and a number n. the function must then use your function in the previous question to read in n number of lines and return teh longest
    def get_longest_line(current_socket: socket, n: int):
        longestLength = 0;
        longestByteString = b''

        for i in range(n):
            current_line = get_lineQuestion15(current_socket)
            current_len = len(current_line)
            if(current_len > longestLength):
                longestByteString = current_line
                longestLength = current_len
        return longestByteString

    #used to complete get_longest_line function,
    def get_lineQuestion15(current_socket: socket):
        buffer = b''  # empty buffer
        while True:  # keep repeating until something below tells you not too ie return
            data = current_socket.recv(
                1)  # data will be coming through as a bytestring so b'a' or b'1' or b'\n' or something like that
            if data == b'\n':
                return buffer
            buffer = buffer + data


    # write a python function that takes in a socket and a delimiter string in byte format, and reads in bytes from the socket connection until one of the delimiters is encountered
    # the bytes read so far are then returned
    def get_lineQuestion14(current_socket: socket, delimiter: bytes) -> bytes:
        buffer = b''
        while True:
            data = current_socket.recv(1)
            if data in delimiter:
                return buffer
            buffer = buffer + data


    # write a python function that takes in a socket and a bytestring then reads in bytes from the socket connetion until a newline is encountered. All bytes read so far that are in the byte
    #string are then returned.
    def get_lineQuestion13(current_socket: socket, bytestring: bytes) -> bytes: # bring in a bytestring and a socket
        buffer = b'' # empty buffer
        while True: # keep repeating until something below tells you not too ie return
            data = current_socket.recv(1) # data will be coming through as a bytestring so b'a' or b'1' or b'\n' or something like that
            if data == b'\n':
                return buffer
            if data in bytestring: # if byte in bytestring so like var1 = b'a' bytestring = b'abcdef' it would return true, you can iterate through like that dont need a for loop
                buffer = buffer + data

    #write a function that takes in a socket, and reads in bytes from the socket connection until a newline is encountered. All bytes red so far that are even are then returned
    def get_lineQuestion12(current_socket: socket) -> bytes:
        buffer = b'' # empty buffer to fill with data
        while True: # while there is data
            data = current_socket.recv(1) #only grab one byte at a time and since theyre ints or unsigned ints , the
            if data ==b'\n': # if the byte is a endline then return what you have so far
                return buffer
            if int.from_bytes(data, byteorder='big') & 0b1 == 0: # 0b1 == 0 is saying if the least significant bit or the futhert right bit is 0 then the number is even, and if its 1 the number is odd. So the & 0b1 ==0 is an even odd checker
                buffer = buffer + data


    #question 11
    while True:
        #this runs once for every conenction...
        sc, _ = sock.accept() # Wait until a connection is established
        with sc: # with sc will take care of closing the socket, I don't have to
            print('Client:', sc.getpeername()) # Client IP and port
            data = sc.recv(BUF_SIZE) # recvfrom not needed since address known
            data2 = data.decode()
            data3 = data2.split(' ')
            counter = 0
            for data in data3:
                if int(data):
                    counter = counter + data
                elif int(data) != int:
                    errorMessage = 'Error\n'
                    errorMessage.encode()
                    sc.sendall(errorMessage)
            sendMessage = counter + '\n'
            sc.sendall(sendMessage.encode())


#Write a python program that recieves a string of numbers (seperated by spaces), over a network via port 24680, adds the nums together then returns the results plus a newline to the sender
# if an error occurs due to an invalid number, the string "Error\n" must be returned to the sender instead. Commands will be echo "10 20 30 40" | nc localhost 24680 returns a string
# '100\n' and the command echo "10 20 30 40 abc" | nc localhost 24680 returns a string 'Error\n'.

#hints if string is '1 2 3 4', the string.split(' ') returns the list ['1','2','3','4']
# if d contains data that was reveived via the network d.decode() to convert it to the regular string
# to transmit a regular string r via the network, use r.encode()

