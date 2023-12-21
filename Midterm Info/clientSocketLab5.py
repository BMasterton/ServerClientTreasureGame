from socket import socket, AF_INET, SOCK_STREAM
from struct import unpack
import struct

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345
directionsString = ['U', 'D', 'L', 'R', 'Q', 'G'] #list of direction strings
playerDirectionString = ['2', '3', '4', '6', '8', 'F'] # hex values of all directions
directionsBytes = [b'\x02', b'\x03', b'\x04', b'\x06', b'\x08', b'\x0F'] # byte hex values of all directions
HEADER_LEN = 2 # header length will always be two as its just two bytes representing size


# prints the scores from the incoming recV() function from server
def printScores(data): #  we are passing in the packed data that we wanted sent over
    score1 = unpack('!H', data[0:2])[0] # We are going to unpack it, and since we sent them together and received them together with our length header of 4 we want to unpack them but the first should be data from 0-2 bytes and below is 2-4 bytes, so they get the correct values
    score2 = unpack('!H', data[2:4])[0] #
    print('Score1', score1)
    print('Score2', score2)
    return


#prints the board from the incoming recv() function from server
def printBoard(board): # passing in the encoded board
    board.decode('utf-8') # undecoding it to be a string
    print(board)
    return


# gets the header length and then gets the next bit of data based on the length the header gave
def headerCheck(sock: socket):  # passing in the entire socket so that we can recv info
    data = sock.recv(HEADER_LEN) # grabbing the header length
    if len(data) != 2:
        raise Exception('Could not recieve Length of header!')
    num_bytes = struct.unpack('!H', data)[0]  # unpack Data, and read the first (and only) unsigned int
    bytes_read = 0
    bytes_from_server = b''
    while bytes_read < num_bytes:
        next_bytes = sock.recv( num_bytes - bytes_read) # this is the actual data we wanted, that we use header to get the length for
        bytes_read += len(next_bytes)
        bytes_from_server += next_bytes
    return next_bytes # actual data we want but still packed mind you


# main function that gets the client number and connects to the server, will repeatedly ask for an input
#send it over to the server and print out any retured info sent back from the client so the user can see whats going on
def main():
    with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket #  if you want to pass a socket through to a function like in the headerCheck you must pass it as what you called it here, and you can type it :socket
        sock.connect((HOST, PORT)) # Initiates 3-way handsha
        #below function is receiving data from header and then rest of needed data in recv buffer
        data_length_bytes = sock.recv(HEADER_LEN) # grabs the length of the header being sent it
        if len(data_length_bytes) != 2: #this is just a check for the length header in our clients case that if it isnt 2 then somethings gone wrong as length is always 2 bytes
            raise Exception('Could not recieve Length of header!')
        num_bytes = struct.unpack('!H', data_length_bytes)[0]  # unpack Data, and read the first (and only) unsigned int. Unpack the unsigned int, this would be the integer value of how long the header is
        print('numBytes', num_bytes)
        bytes_read = 0
        bytes_from_server = b''
        while bytes_read < num_bytes:
            next_bytes = sock.recv(num_bytes - bytes_read) # get the next bit of data with header length, so wanted data minus header # this is the actual data we are receiving that we want, it’s making sure it will work correctly with all the bytes_read and such
            bytes_read += len(next_bytes)
            bytes_from_server += next_bytes
            playerID = int.from_bytes(bytes_from_server, byteorder='big')
            print('Intfromserver', playerID)
        print('bytes from server',bytes_from_server)

        #player totallity checker closes client if a third is added
        if playerID > 2:
            print("too many clients closing the connection")
            return

        while True:
            directionInput = input("please enter a direction: ")
            if directionInput == directionsString[0]: #direction is U
                sock.sendall(directionsBytes[0]) # sending the information back to the server as a hex byte string, so we don’t need to pack it or anything
                printScores(headerCheck(sock)) # print out the scores with the socket of the size returned from the header
            elif directionInput == directionsString[1]: #direction is D
                sock.sendall(directionsBytes[1]) # returning one byte that is the byte string that represents the hex value of Up which is 2
                printScores(headerCheck(sock))
            elif directionInput == directionsString[2]: #direction is L
                sock.sendall(directionsBytes[2])
                printScores(headerCheck(sock))
            elif directionInput == directionsString[3]: # direction is R
                sock.sendall(directionsBytes[3])
                printScores(headerCheck(sock))
            elif directionInput == directionsString[4]: # direction is Q
                # send info to server, print scores and board, quit
                sock.sendall(directionsBytes[4])
                printScores(headerCheck(sock)) # calling the check on both the scores and the board as we sent them seperately
                printBoard(headerCheck(sock))
                return
            elif directionInput == directionsString[5]: # direction is G
                # send info to sever, then print the returned scores and board
                sock.sendall(directionsBytes[5])
                printScores(headerCheck(sock))
                printBoard(headerCheck(sock))


main()
