# This will be a client that 1. Gets the number of clients c and number of repititions r from the command line 2. starts c clients, each of which connects to a server listening on local
# host port 12345 and sends a message to the server r times. 3. messgaes should be sent in an interleaved fashion not in sequential order

# this version has it showing the numbers changing buyt the the messgaes are not interleaved
# the client is not taking advantage of asynchronous transmissions, it is still largely operating sequentially

# !/usr/bin/python3.11
from asyncio import open_connection, run, sleep, create_task
from sys import argv

HOST = 'localhost'
PORT = 12345


async def send_message(client_id: int, num_reps: int) -> None:
    for i in range(num_reps):
        reader, writer = await open_connection(HOST, PORT)
        writer.write(('This is ' + str(client_id) + '\n').encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        await sleep(0)


async def main(num_clients: int, num_reps: int) -> None:
    tasks = []
    for i in range(num_clients):
        tasks.append(create_task(send_message(i,num_reps)))

    for t in tasks:
        await t


if len(argv) != 3:
    print(argv[0], '<Number of clients> <Number of repetitions>')
    exit(-1)

try:
    run(main(int(argv[1]), int(argv[2])))
except Exception as e:
    print(e)

#server = await asyncio.start_server(echo, '127.0.0.1', 12345) starts echo as a task so that it becomes possible
# to switch between (interleave) different running instances of echo

# on the client side, we have to create these tasks explicity

# run like main says, we need to say how many clients, and how many reps each client will do
# python3 AsyncClientBasic2-2.py 2 2
# python3 AsyncClientBasic2-2.py 4 2