# !/usr/bin/python3.11
from random import randint
from asyncio import run, sleep, start_server, StreamReader, StreamWriter

HOST=''
PORT=12345

DIMENSIONS = 4
board = [['' for _ in range(DIMENSIONS)] for _ in range(DIMENSIONS)]


def place(client):
    global board

    while True:
        row = randint(0, DIMENSIONS-1)
        col = randint(0, DIMENSIONS-1)
        if board[row][col] =='':
            board[row][col] = client
            return

place('1')
place('2')
print(board)

clientNum = 0


async def handleConnection(reader: StreamReader, writer: StreamWriter)-> None:
    global clientNum
    loop = True

    clientNum += 1
    if clientNum ==1:
        other_client = '2'
    elif clientNum == 2:
        other_client ='1'
    else:
        other_client = ''
        loop = False

    while loop:
        writer.write(b'GO\n')
        await writer.drain()

        reply = await reader.readline()

        try:
            reply = reply.decode()
            row = int(reply[0])
            col = int(reply[1])
            if(0<= row < DIMENSIONS) and (0 <=col < DIMENSIONS) and (board[row][col] == other_client):
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

# #Question
# 2.Modify your answer to the previous question so that the following conditions hold:
# Instead of 1 client, the server supports 2 clients. Specifically: At startup, a '2' is also
# placed randomly in a blank cell. Both clients can make a guess anytime they wish;
# turns are not enforced. A client must guess the other client's cell to get an OK back. So, client 1 will get only an OK if it guesses the location of the '2' and client 2 will
# only get an OK if is guesses the location of the '1'. (Client 1 is the first client to
# connect, client 2 is the second client to connect. Any other clients are
# disconnected.)
