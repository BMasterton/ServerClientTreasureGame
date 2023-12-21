#!/usr/bin/python3.11

# Question 34


#!/usr/bin/env python3.11
from asyncio import run, start_server, StreamReader, StreamWriter
from random import randint
num = randint(1, 100)
async def get_guess(reader: StreamReader, writer: StreamWriter) -> None:
    global num
    try:
        while True:
            data = await reader.readline()
            decoded_data = int(data.decode().strip())
            if decoded_data > num:
                writer.write(b"Too High\n")
                await writer.drain()
            elif decoded_data < num:
                writer.write(b"Too Low\n")
                await writer.drain()
            else:
                writer.write(b"Correct\n")
                await writer.drain()
                break
    except Exception as e:
        print(e)
    writer.close()
    await writer.wait_closed()
async def main():
    server = await start_server(get_guess, '', 12345)
    await server.serve_forever()
run(main())
# run with echo '50' | nc localhost 12345



#Question
# .Using asyncio, write a Python server that sets a global num to a random value,
# accepts connections from local and external clients on port 12345, repeatedly reads
# in one line at a time from one or more clients, converts that line to an int, checks
# whether or not that int is lower, higher, or equal to num, depending on the
# comparison, sends the client the message "Too High", "Too Low", or "Correct",
# respectively. If correct, the client connection is closed. All exceptions must be
# caught.
