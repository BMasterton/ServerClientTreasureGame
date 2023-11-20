# #question28 Write a multithreaded python server that guesses a random number between 1 and 100 (random.randint(1,100) from the random library. listens on port 12345 accepts
# #an arbitrary number of clients lets then know their ID repetedly reads in the huesses from the clients who send the number as a newline-terminate string lets the clinets know wether
# # they are correct or not and if so if they were the first, the server shoudl not crash
# # for this you literally just need to use nc localhost 12345 and then it will keep going and keep asking the client
# transmits numbers 
# #!/usr/bin/python3.11
#
# from random import randint
# from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
# from threading import Semaphore, Thread
#
# HOST = ''
# PORT = 12345
# NUM_CLIENTS = 1
#
# MIN = 1
# MAX = 100
# r = randint(MIN, MAX)
# print(r)
#
# lock = Semaphore()
# winner = 0
#
# def get_line(current_socket: socket) -> bytes: # basically just starts with an empty byte string called buffer and keeps grabbing one byte of data, if its ever notihg or an end line  it gets returned
#     buffer= b''
#     while True:
#         data = current_socket.recv(1)
#         if data == b'' or data == b'\n':
#             return buffer
#         buffer += data
#
# # main function of the thread server, brings in a socket and a player id which it will be sending to the client.
# def contact_player(client: socket, player_id:int ):
#     global lock, r, winner
#
#     with client:
#         client.sendall(f'Hello Player {player_id}\n'.encode()) # as this is a string we need to encode it to send over
#         while True:
#             try:
#                 number = int(get_line(client)) # we are always getting an int in so we just make sure the byte string is an int
#                 found = False
#                 found_first = False
#                 with lock:
#                     if number == r: # guessed the correct num
#                         found = True
#                         if winner == 0:
#                             found_first = True
#                             winner = player_id # setting the winner
#
#                 # sending takes time so its done outside the lock
#                 # sending back byte strings of what happened
#                 if found_first:
#                     client.sendall(b'You Won!\n')
#                 elif found:
#                     client.sendall(b'You got it!\n')
#                 else:
#                     client.sendall(b'No\n')
#             except ValueError:
#                 continue
#
#
# sock = socket(AF_INET, SOCK_STREAM)
# sock.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
# sock.bind((HOST,PORT))
# sock.listen(NUM_CLIENTS)
# num_players = 1
# while True:
#     sc, _ = sock.accept()
#     Thread(target=contact_player, args=(sc, num_players)).start() # creating the thread and using numPlayers to keep count of them
#     num_players += 1
#
#
#
#
#
#
# #question 29
# #!/usr/bin/python3.11
#
# from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
# from threading import Semaphore, Thread
#
# HOST =''
# PORT = 12345
# NUM_CLIENTS=2
#
# locks =[Semaphore(), Semaphore()]
# locks[-1].acquire() # locks the second player
# msg=b'Please begin\n'
#
#
# def get_line(current_socket: socket) -> bytes:  # basically just starts with an empty byte string called buffer and keeps grabbing one byte of data, if its ever notihg or an end line  it gets returned
#     buffer = b''
#     while True:
#         data = current_socket.recv(1)
#         if data == b'' or data == b'\n':
#             return buffer
#         buffer += data
#
# def contact_client(client: socket, client_id:int):
#     global locks, msg
#
#     sc, _ = client.accept()
#     with sc:
#         while True:
#             # Acquires the Semaphore lock corresponding to the client's ID (0 or 1). This means that if the lock is already acquired by the other client, the thread will block until the lock becomes available.
#             locks[client_id].acquire() #is used to acquire (lock) the second Semaphore in the list. In this context, it means that the second player's thread is initially blocked from sending a message. The first player's thread (client 0) can send a message initially.
#             sc.sendall(msg)
#             msg = get_line(sc) + b'\n'
#             locks[(client_id +1) % NUM_CLIENTS].release()# Releases the Semaphore lock of the other client (next in line, wrapping around from 1 to 0).
#
#
# sock = socket(AF_INET, SOCK_STREAM)
# sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# sock.bind((HOST, PORT))
# sock.listen(NUM_CLIENTS)
# num_clients = 1
# while num_clients != NUM_CLIENTS:
#     Thread(target=contact_client, args=(sock, num_clients)).start()
#     num_clients = num_clients + 1
#
#
# #Question 30 Write a multithreaded server that monitors sensors. Specifically using a b'?' the server prompts the first sensor client whether or not an alert condition is present
# # the 1-bytes reply is sent to the server if an alert is present b'!' the alert counter is incremented and the counter value is printed on the server. The server using a b'?'
# # then prompts the second sensor client wheter or not an alert condition is present. the reply is sent to the server, If an alert is present b'!' the alert counter is incremented and a message
# # is printed on the server this repeats indefinitely.
#
#
# #question 30
# #!/usr/bin/python3.11
#
# from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
# from threading import Semaphore, Thread
#
# HOST =''
# PORT = 12345
# NUM_CLIENTS=2
# ALERT=b'!'
# locks = []
# for i in range(NUM_CLIENTS): # getting all the clients which here is 2
#     locks.append(Semaphore()) # adding more semaphores to the list
#     locks[-1].acquire() # lockingthe last one
#
# alertCount = 0 # how many times we have received an alert message
#
#
# def contactClient(client: socket, client_id:int): # main function that runs from the thread
#     global alertCount, locks # need to grab the globals we set earlier
#
#     sc, _ = client.accept() # accepting the new socket ie each new client is one of these
#     with sc: # with that client
#         while True: # loop
#             locks[client_id].acquire() # for either client 0 or 1
#             sc.sendall(b'?') # always sends from the serve to the client asking for a mesage back
#             if sc.recv(1) == ALERT:
#                 alertCount +=1
#                 print('Alert', alertCount)
#             locks[(client_id +1) % NUM_CLIENTS].release() # Releases the Semaphore lock of the other client (next in line, wrapping around from 1 to 0).
#
#
#
#
# sock = socket(AF_INET, SOCK_STREAM)
# sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# sock.bind((HOST, PORT))
# sock.listen(NUM_CLIENTS)
# num_clients = 0 # starting at 0
# while num_clients != NUM_CLIENTS: # while there are less than 3 clients
#     Thread(target=contactClient, args=(sock, num_clients)).start()
#     num_clients = num_clients + 1
# locks[0].release()
# #In summary, locks[0].release() is used to allow "client 0" to proceed and send a message to the server,
# # while the server will release the lock of "client 1" to let it proceed when it's its turn. This coordination ensures orderly
# # communication between the server and the two clients.
#
#
#
#
#
# #Question 31 Write a python serve that creates a new thread for every client that connects. Each thread waits for a newline terminatied message
# #from its client, then prints the message to the server screen, then waits for the next message from its client. Be sure to use locks so that a print command
# # is not interuppted by another threads print command.
# transmits string sentences
#
# #!/usr/bin/python3.11
#
# from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
# from threading import Semaphore, Thread
#
# HOST =''
# PORT = 12345
# NUM_CLIENTS=1
#
# lock = Semaphore()
#
# def get_line(current_socket: socket) -> bytes:  # basically just starts with an empty byte string called buffer and keeps grabbing one byte of data, if its ever notihg or an end line  it gets returned
#     buffer = b''
#     while True:
#         data = current_socket.recv(1)
#         if data == b'' or data == b'\n':
#             return buffer
#         buffer += data
#
# def contact_client(client_socket: socket):
#     try:
#         with client_socket:
#             while True:
#                 local_msg = get_line(client_socket)
#                 if local_msg == b'':
#                     break
#                 with lock:
#                     print(local_msg)
#     except Exception as details:
#         print(details)
#
#
# sock = socket(AF_INET, SOCK_STREAM)
# sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# sock.bind((HOST, PORT))
# sock.listen(NUM_CLIENTS) # how many clients were allowed to have so here we can have just 1
# i = 0 # should just be for monitoring how many connections we have
# while True:
#     sc, _ = sock.accept()
#     Thread(target=contact_client, args=(sc,)).start()
#     i += 1 # keeping a number of connected clients



#question 32 Write a python server that creates a new thread for every client that connects. Each thread waits for a newline-terminated string from its client. It then converst the
#string to an integer ( or 0 if that is not possible) and adds it to a global sum. it then returns the latest global sum to the client. Be sure to use locks so that a race consition is avoided
# numbers of more than 4 digits are ignored
#transmits numbers

#!/usr/bin/python3.11

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Semaphore, Thread

HOST =''
PORT = 12345
NUM_CLIENTS=1
MAX_DIGITS = 4

lock = Semaphore()
total = 0

def get_line(current_socket: socket) -> bytes:  # basically just starts with an empty byte string called buffer and keeps grabbing one byte of data, if its ever notihg or an end line  it gets returned
    current_size = 0
    buffer = b''
    while current_size < MAX_DIGITS: # instead of while true we loop until the input digits are too large
        data = current_socket.recv(1) # just like the buffer we are grabbing data one byte at a time until we get a blank or a new line
        if data == b'' or data == b'\n':
            return buffer
        buffer += data
        current_size = current_size + len(data)
        # if we are here, the number is too big. Worse, it could be that the rest of the number is still in the input
        # buffer, and the next time ew call get_line, the rest will be read inm as a new number. Best to raise an error here.
    raise ValueError('newline not found')

def contact_client(client_socket: socket):
    global total
    try:
        with client_socket:
            local_msg = get_line(client_socket)
            if local_msg == b'':
                return
            val = int(local_msg)
            with lock:
                new_val = total + val
                total = new_val
            client_socket.sendall(str(new_val).encode() + b'\n')
    except Exception as details:
        print(details)


sock = socket(AF_INET, SOCK_STREAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(NUM_CLIENTS) # how many clients were allowed to have so here we can have just 1
while True:
    sc, _ = sock.accept()
    Thread(target=contact_client, args=(sc,)).start()








