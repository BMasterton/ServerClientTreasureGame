#!/usr/bin/python3.11
import struct
from asyncio import run, open_connection
import sys

HOST = '127.0.0.1'
PORT = 1111

URGENCYFLAGS = ['U', 'N']
idBits = 0b00000000
flagBits = 0b00000000
messageLength = 0
message = b''

async def client():
    global idBits
    global flagBits
    global messageLength
    global message

    try:
        reader, writer = await open_connection(HOST, PORT)
        while True:
            # get the id from the command line and bit shift and mask it to get first 7 bits
            argID = int(sys.argv[1])
            # if the ids too hight exit
            if argID > 127:
                break
            argIDEncoded = struct.pack('!H', argID) # troubels getting the bits
            idBits = (argIDEncoded & 254) >> 1

            # grabbing the flag input and setting bits accordingly
            argUrgencyFlag = sys.argv[2]
            # if the flag isnt one of the choices exit
            if argUrgencyFlag not in URGENCYFLAGS:
                break
            if argUrgencyFlag == 'U':
                flagBits = 0b00000001
            elif argUrgencyFlag == 'N':
                flagBits = 0b00000000

            argMessage = sys.argv[3]
            if len(argMessage) > 255:
                argMessage = argMessage[:255] # get all characters in the string array up to 255 and ignore the rest
            messageLength = len(argMessage)
            messageLength = struct.pack('!H', messageLength)
            message = argMessage.encode('utf-8')

            IdAndFlagBits = idBits | flagBits # if argIDEncoded was bits this would all work but i ran out f time

            #sending info in its packs
            writer.write(IdAndFlagBits)
            await writer.drain()
            # this should be sending a byte but i cant find a sendexactly(1) coroutine
            writer.write(messageLength)
            await writer.drain()
            # send encoded message
            writer.write(message)
            await writer.drain()
    except ValueError:
        writer.close() # close in case errors occur
        await writer.wait_closed()
    except Exception as e:
        print(e)
        writer.close()
        await writer.wait_closed()

    #final close could also be done in a finally block
    writer.close()
    await writer.wait_closed()




run(client())