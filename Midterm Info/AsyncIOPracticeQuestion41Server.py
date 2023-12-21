# !/usr/bin/python3.11
from random import randint
from asyncio import run, sleep, start_server, StreamReader, StreamWriter

HOST=''
PORT=12345

DIMENSIONS = 4
board = [['' for _ in range(DIMENSIONS)] for _ in range(DIMENSIONS)]
board[randint(0, DIMENSIONS-1)][randint(0,DIMENSIONS-1)] = '1'
print(board)


async def handleConnection(reader: StreamReader, writer: StreamWriter)-> None:
    while True:
        writer.write(b'GO\n')
        await writer.drain()

        reply = await reader.readline()

        try:
            reply = reply.decode()
            row = int(reply[0])
            col = int(reply[1])
            if(0<= row < DIMENSIONS) and (0 <=col < DIMENSIONS) and (board[row][col] == '1'):
                writer.write(b'OK\n')
                await writer.drain()
                break
            else:
                writer.write(b'NO\n')
                await writer.drain()


        except ValueError:
            writer.write(b'NO\n')
            await writer.drain()
    writer.close()
    await writer.wait_closed()



async def main():
    server = await start_server(handleConnection, HOST, PORT)
    await server.serve_forever()

run(main())

#Question
# Create a server that complies with all of the following specifications: Use asyncio.
# On startup, the server creates an empty 4x4 game board. It then randomly selects
# one of these 16 cells and marks it with a '1'. Be sure to print out the board on the
# screen! The server then waits for a client connection on localhost port 12345. The
# server prompts the client to make a guess by transmitting the string "GO\n". The
# server then expects a position from the client in the format "_ _\n", where the first
# blank represents the row and the second blank represents the column. Values must
# be in the range of 0 - 3, so the server validates the client input. Any invalid input
# means that the input is ignored. If the position matches that of the '1' on the board,
# the client is sent the message "OK\n". Otherwise, including in the case of invalid
# input, the client is sent the message "NO\n". On OK, the connection is then closed.
# On "NO\n", the cycle repeats from Step 4 by prompting the client for another guess.
# The server must not crash. You can test the server using the command nc
# 127.0.0.1 12345