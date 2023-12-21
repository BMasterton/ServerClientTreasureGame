#!/usr/bin/python3.11
import struct
from random import randint
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Semaphore, Thread
import time

HOST = ''
PORT = 1111
NUM_CLIENTS =2
messageList = {}
clientList = []


lock = Semaphore()
winner = 0



# goes through byte by byte untila newline or empty byte and creates the data byte string
def headerCheck(sock: socket):  # passing in the entire socket so that we can recv info
    data = sock.recv(2) # grabbing the header length
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

# main function of the thread server, brings in a socket and a player id which it will be sending to the client.
def contact_player(sc: socket ):
    global lock, winner

    with sc:
        try:
            data = sc.recv(2) # get byte data
            databyte1 = list(data)[0] # get first byte
            databyte2 = list(data)[1] # get second byte
            clientID = (databyte1 & 254) >> 1 # from the first byte mask it 7 places and shfit it one
            urgecyFlag = (databyte1 & 1)
            clientAndUrgency = clientID | urgecyFlag

            data = sc.recv(databyte2) # get the length of the
            dataLength = int.from_bytes(data, byteorder='big') # sinc we are getting in bytes we need the int from it

            data = sc.recv(dataLength) # get message from length
            message = data.decode('utf-8') # decode the message
            messageList[clientAndUrgency] = message, 0 # add it to an array so we can print it out
            exit()
        except Exception as e:
            print(e)
        except ValueError:
            exit()



sock = socket(AF_INET, SOCK_STREAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(NUM_CLIENTS) # how many clients were allowed to have so here we can have just 1
thread_list = [] # list of all client connections
while True:
    sc, _ = sock.accept()
    thread_list.append(Thread(target=contact_player, args=(sc,)).start()) # appending our threads to a list
    time.sleep(10)
    print(messageList.sorted())# trying to sort every 10 seconds


#seems to be working with client 2 but not client one, client two will win the game if it is guessed correctly
# but player one will not