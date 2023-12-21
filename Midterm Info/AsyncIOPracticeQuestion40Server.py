# !/usr/bin/python3.11
import random
from asyncio import run, sleep, start_server, StreamReader, StreamWriter

HOST=''
PORT=12345

guess = random.randint(0,9)
print(guess)

numClients =0
turn = 0 # whos turn it is
over = False # is the game over


async def game(reader:StreamReader, writer: StreamWriter)-> None:
    global numClients
    global turn
    global over

    my_number = numClients # whos currently up
    numClients +=1

    while not over: # while game is still going on
        if turn != my_number: # this is the wait condition, if its not your turn wait for it to be
            await sleep(0.5)
            continue # loop back up to while not over
        if over: # 'over' could have changed due to the sleep above
            break
        writer.write(b'GO!\n') # clients turn
        await writer.drain()

        reply = await reader.readline()
        try:
            if guess == int(reply.decode()): # if you guess the number end game and close everyuthing
                over = True
                writer.write(b'Win\n')
                await writer.drain()
                writer.close()
                await writer.wait_closed()
                return # leave this loop
            continue
        except Exception as e:
            print(e)
            continue
        finally:
            turn = (turn + 1)% numClients
    writer.write(b'NO.\n') # after someone has got the winning number we exit and close
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    turn = (turn + 1)% numClients
    return


async def main():
    server = await start_server(game, HOST, PORT)
    await server.serve_forever()

run(main())


#Question
# For this server, you must use Python's asyncio. The server starts out by picking a
# random number in the range from 0 to 9, inclusive. The server then waits for
# connections on localhost port 12345. The server enforces turns among its clients; it
# lets a client know its turn by transmitting the string "GO!\n". The server then expects
# a newline-terminated guess from that client. If the guess matches the random
# number, the client is informed of the win using the string "WIN\n" and the
# connection is closed. All other clients are informed of their loss using the string "NO.
# \n"and the connection is closed. Your server must not crash. You can test the server
# using the command nc 127.0.0.1 12345