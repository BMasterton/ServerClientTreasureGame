#!/usr/bin/python3.11

from random import randint
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Semaphore, Thread
import time

HOST = ''
PORT = 56765
NUM_CLIENTS =2

MIN = 1
MAX = 100
r = randint(MIN, MAX)


lock = Semaphore()
winner = 0

def mathAnswer():
    x = randint(1, 10)
    y = randint(1, 10)
    total = x * y
    print(x, '*', y)
    return total

# goes through byte by byte untila newline or empty byte and creates the data byte string
def get_line(current_socket: socket) -> bytes: # basically just starts with an empty byte string called buffer and keeps grabbing one byte of data, if its ever notihg or an end line  it gets returned
    buffer= b''
    while True:
        data = current_socket.recv(1) # grab one bytea at a time
        if data == b'' or data == b'\n': # if its empty bytestring or newline bytesting we return as its the end of wanted data
            return buffer
        buffer += data

# main function of the thread server, brings in a socket and a player id which it will be sending to the client.
def contact_player(client: socket, player_id:int ):
    global lock, winner

    with client:
        # while True:
        while 0 == winner:
        #     time.sleep(5)  # wait 5 seconds then try and do the rest
            try:
                total = mathAnswer() # get the total for what x and y are
                number = int(get_line(client)) # get the clients input using get_line func
                found_first = False
                if number == total: # if input number is correct then
                    if winner == 0: # if there isnt a winner yet
                        found_first = True
                        winner = player_id # winner is now the passed in id
                if found_first:
                    client.sendall(b'Winner') # send winner info back to client letting them know they won
                    print(player_id) # letting the server know who won
                    exit()
            except ValueError:
                continue


def timer():
    global lock, winner, total
    while 0 == winner:
        with lock:
            if 0 == winner: total = mathAnswer()

        time.sleep(5)

sock = socket(AF_INET, SOCK_STREAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(NUM_CLIENTS) # how many clients were allowed to have so here we can have just 1
num_players = 1 # keeping track of the players
thread_list = [] # list of all client connections
for i in range(NUM_CLIENTS): # we want only 2 clients
    sc, _ = sock.accept()
    thread_list.append(Thread(target=contact_player, args=(sc, num_players))) # appending our threads to a list
    thread_list[-1].start()
    if num_players ==2:
            Thread(target = timer).start()
    # if num_players == 2: # only starting the threads once we have 2
    #     thread_list[-1].start() # start the threads together

    num_players += 1
#seems to be working with client 2 but not client one, client two will win the game if it is guessed correctly
# but player one will not