#!/usr/bin/python3.11

from asyncio import run, open_connection
HIGH = 100
LOW = 1

async def client():
    low = LOW
    high = HIGH
    writer = None
    try:
        reader, writer = await open_connection('127.0.0.1', 12345)
        while True:
            mid = (low + high) // 2 # integer division
            print(f'Guessing {mid}')
            writer.write(str(mid).encode() + b'\n')
            # await writer.drain() # seemingly you can have this here or not
            data = await reader.readline()
            decoded_data = data.decode().strip()
            print(decoded_data)
            if decoded_data =='Too High':
                high = mid
            elif decoded_data == 'Too Low':
                low = mid
            else:
                break
    except Exception as details:
        print(details)
    if writer is not None:
        writer.close()
        await writer.wait_closed()




run(client())


# Question

# .Using asyncio, write a Python client that connects to the server in the previous
# question; sends the server a UTF-8 encoded number that is midpoint between
# HIGH and LOW (both constants are based on the range you used in the previous
# question); and waits for a server to reply with a line of encoded text. If the server
# says "Too High", the client sets the new high point to the current mid point, if the
# server says "Too Low", the client sets the new low point to the current mid point,
# and if the server says "Correct", closes the connection. If the reply was not correct,
# the client calculates a new mid point and sends that to the server, until the correct
# number is guessed. All exceptions must be caught.

# For example, assuming the server's number is 12, and HIGH = 100 and LOW = 0,
# the client would first send 50. Getting back the reply "Too high", it will then send
# 25. Getting back the reply "Too high", it will then send 12, upon which "Correct" is
# returned and the client quits.