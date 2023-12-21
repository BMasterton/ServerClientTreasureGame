#!/usr/bin/python3.11
from asyncio import open_connection, run
from sys import argv

async def client(message: str) -> None:
    reader, writer = await open_connection('127.0.0.1', 12345)
    writer.write(message.encode() + b'\n')
    data = await reader.readline()
    print(f'Received: {data.decode("utf-8")}')
    writer.close() # reader has no close() function
    await writer.wait_closed() # wait until writer completes close()

if len(argv) != 2:
    print(f'{argv[0]} needs 1 argument to transmit')
    exit(-1)
run(client(argv[1]))

#basically what you send in as the argument is being sent to the server, and you run it like this:
#python3 AsyncClientBasic.py 'Hello'
#python3 AsyncClientBasic.py Hello
#python3 AsyncClientBasic.py 12345
#python3 AsyncClientBasic.py 0b00000001
#python3 AsyncClientBasic.py 0b00000001


# -------------CLINT INFO ---------------------
# asyncio.open_connection('127.0.0.1', 12345) can throw an exception (eg., ConnectionRefusedError)
#on succes, returns a tuple containing a reader for reading from the stream, and a writer for writing to the stream
#no drain is needed on the client end because it write only once, then waits until data comes back from the server (which means
# that all thee clients data has been written)

#calling recv(1) is actually quite inefficient, since it can involve a context switch
#asyncio provided convenitent functions
    #coroutine read(n=-1)
        # read up to n bytes, if n is not provided, or set to -1, read until EOF and retur all read bytes. IF EOF was received and the internal buffer is empty, return an empty bytes object
    #coroutine readline()
        # rad one line, wehre 'line' is a swquence of bytes ending with \n. If EOF is received and \n was not found, the method returns partially read data. if EOD is received and the internal buffer
        # is empty, return an empty bytes object
    #coroutine readexactly(n)
        # read exactly n bytes. Raise an IncompleteReadError if EPF is reached before n can be read. USe the IncompleteReadError.partial attribute to get partiallyReadData
    #coroutine readuntil(sepeartor=b'\n')
        #Read data from the stream until separator is found. On success, the data and separator will be removed from the internal buffer (consumed). Returned data will include
        # the separator at the end. If the amount of data read exceeds configured stream limit, a LimitOverrunError exception is raised, and the data is left in the internal buffer and can
        # be read again. If EOF is reached before the complete separator is found, an IncompleteReadError exception is raised, and the internal buffer is reset. The IncompleteReadError.partial attribute may contain a portionof the separator

