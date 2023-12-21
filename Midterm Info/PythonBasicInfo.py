# python functions and how they are used


# These are all byte strings
bytesFromServer = b''  # this is an empty byte string
bytesFromServer = b'x02'  # this is in hex
bytesFromServer = b'x0F'  # this is in hex
bytesFromServer = b'x2F'  # this is in hex
bytesFromServer = b'xFF'  # this is in hex
int.from_bytes(bytesFromServer)  # this allows you to get the int version of bytes

bytesFromServer1 = b'this is also a byte string'
bytesFromServer1 = b'wow another one'

# aside
Str1 = "Hello, C"  # where C is an exotic character
len(Str1) == 8
Str2 = Str1.encode('utf-8')
len(Str2) == 9
# youcan always send strings as the exact same thing with a b infront of it ie b'hello, C'
# they may have different lengths

# Converters
# Hex --> decimal
int('0xFF', 16) == 255
int('FFFF', 16) == 65535

# hex
hex(255) == 0xff  # decimal
hex(0b111) == 0x7  # binary
hex(0o77) == 0x3f  # octal
hex(0xFF) == 0xff  # hexidecimal

# the base and value have to match, ie the 0x1A is hex so the base needs to be 16
int('0o12', 8) == 10
int('0b110', 2) == 6  # make an int from the binary base 2
int('110', 2) == 6  # dont need the 0b if you dont want
int('0x1A', 16) == 26

# number examples
A = 30
B = 0b000011110  # binary 30
C = 0X1E  # hex 30
y = b'\x1E\x1E'  # Bytestring
X = b'\x1E'  # Bytestring

X[0] = 30

y[0] == 30
y[1] == 30

H = int.from_bytes(b'\X1E', 'big')

# masking and shifting
A = 0b00001111
B = 0b11110000

C = A & B == 00000000
D = A | B == 11111111
E = A ^ B == 0b11111111

A = 0b10101010  # Want to read the first 4 bytes aka 1010
# Mask it
A = A & 240  # 240 is 11110000
# A now looks like this 0b10100000
# Shift it now, and as we want the first 4 we need to add 4 zeros to the left to get 0b00001010
A >> 4  # A now looks like this 0b00001010 == 10

# if we wanted the middle 2 so 5 and 6th

B = 0b10101010
# Mask it
B = B & 12  # 12 is 00001100
# now we just need to shift it to to the right to get the 2 values we wnat in the far right spots
B >> 2  # == 0b00000010

# Reverse

Cmd = 12  # (1100)……1100 is actualy 0b00001100

Cmd << 4  # ==3 11000000 {160)

Pid = 2  # == 10 or 0b00000010

Pid << 2  # == 1000 (8)

Cmd | Pid  # == 11001000 (168)

# functions that may or may not be usefull

HEADER_LEN = 2  # header length will always be two as its just two bytes representing size


# use this if a header is necessary
# gets the header length and then gets the next bit of data based on the length the header gave
def headerCheck(sock: socket):
    data = sock.recv(HEADER_LEN)
    if len(data) != 2:
        raise Exception('Could not recieve length of data')
    num_bytes = struct.unpack('!H', data)[0]  # unpack Data, and read the first (and only) unsigned int
    bytes_read = 0
    bytes_from_Server = b''
    while bytes_read < num_bytes:
        next_bytes = sock.recv(num_bytes - bytes_read)
        bytes_read += len(next_bytes)
        bytes_from_Server += next_bytes
    return next_bytes


# goes through byte by byte untila newline or empty byte and creates the data byte string
def get_line(
        current_socket: socket) -> bytes:  # basically just starts with an empty byte string called buffer and keeps grabbing one byte of data, if its ever notihg or an end line  it gets returned
    buffer = b''
    while True:
        data = current_socket.recv(1)  # grab one bytea at a time
        if data == b'' or data == b'\n':  # if its empty bytestring or newline bytesting we return as its the end of wanted data
            return buffer
        buffer += data


# basically the same as above just done slightly differently
def fetch_buffer(sock: socket):  # sock here is
    Buf = b''
    while True:
        data = sc.recv(
            1)  # If we are using a header this could be grabbing the header length of something, and then below using that to grab the next set of data
        if 0 == len(data):  # connection to close if true
            break  # out of the while loop not if block
        Buf += data
    return Buf


# unpacking data from the struct.pack.
# here we sent over both point values packed together and since we know they are length 2 we can use an array grab to take certain sections that relate to what was put in
score1 = unpack('!H', data[0:2])[0]
score2 = unpack('!H', data[2:4])[0]

# for sockets sending info
# we can only send info as bytes, so everything we send over will be encrypted either with struct.pack() or with .encode('UTF-8') if its a string we are sending.
sock.sendall(pointPack(newBoard))

# recv()
# how we recieve data with a socket, we are asking for 1024 bytes of data, you dont have to grab it all at once
sock.recv(1024)

# multigrab send + recv
# you can send over lets say 8 bytes
# info = 8 bytes
sock.sendall(struct.pack(info))

# for the recv we can receve it all at once, or we can grab it piece by piece, 1 byte at a time, or more.
# below grabs all the data from that sendall() just parts at a time but its all from the same
sock.recv(2)
sock.recv(1)
sock.recv(1)
sock.recv(4)


# threading and sockets
def playerControl(sc: socket, newBoard, playerNames):
    pass


def start(self):
    newBoard = Board(5, 10, 5, 10, 2)  # creating the new boar
    playerNames = ["1", "2"]  # list of players that will be added
    HOST = ''
    PORT = 12345
    thread_list = []  # this is gong to be the list of threads that we have, in our case client connections

    while True:
        try:
            display(newBoard)  # displays the original board
            with socket(AF_INET, SOCK_STREAM) as sock:  # TCP socket
                sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Details later
                sock.bind((HOST,
                           PORT))  # Claim messages sent to port "PORT" have to pass in a single argument that is a tuple containing host and port
                sock.listen(1)  # Server only supports a single 3-way handshake at a time
                print('Server:', sock.getsockname())  # Server IP and port
                while True:  # keep doing this as we have many connections to make and will keep allowing more connections and therefore threads to be created
                    sc, _ = sock.accept()  # Wait until a connection is established
                    # Creating the threads for sc, so we need to
                    thread_list.append(Thread(target=playerControl, args=(sc, newBoard,
                                                                          playerNames,)).start())  # Here we are creating the threads, and you can see that we append them to a list, and the call Thread(where the target is the function you want the threads to run, the parent running function for the treads action, and the args is what you pass to that function.
            # Something to note here, is that in our function since we can just add clients when we want, we can start it immediately, so the unique threads are created for each client connection, in some other cases you don’t want to do this as you want them to all start at the same time. Like a thread that just counts to a million. If you had 5 threads you might want them to start at the same time. So once they are all made, you can start them with thread_list[-1].start()
            for t in thread_list:
                t.join()  # kill command need the children to be killed before main ends, should be called automatically once the functions job is completed. .join() is the reap command.
        except Exception as details:
            print(str(details))


# or something like this if you only want a certain amount of clients to connect


sock = socket(AF_INET, SOCK_STREAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(NUM_CLIENTS)  # how many clients were allowed to have
num_players = 1  # keeping track of the players
thread_list = []  # list of all client connections
for i in range(NUM_CLIENTS):  # we want only 2 clients
    sc, _ = sock.accept()
    thread_list.append(Thread(target=contact_player, args=(sc, num_players)))  # appending our threads to a list
    if num_players == 2:  # only starting the threads once we have 2
        thread_list[-1].start()  # start the threads together
    num_players += 1


# async
# all in a class of course
def start(self):
    self.newBoard = Board(5, 10, 5, 10, 2)  # creating the new boar
    playerNames = ["1", "2"]  # list of players that will be added
    HOST = ''
    PORT = 12345


# the function that each connection to the async server is running, with simple send functiosn
# we still pack and use struct.pack and encode the same but we send it much easier
async def playerControl(reader: StreamReader, writer: StreamWriter) -> None:
    writer.write(playerPack(data))  # this is doing sendall, we are writing data to the client with packed data
    await writer.drain()  # this is used after all writes, and it makes it so the program waits until a successfull transfer is completed


# code to create the async server connections and keep them going
async def main() -> None:
    server = await asyncio.start_server(playerControl, HOST, PORT)
    await server.serve_forever()


run(main())
