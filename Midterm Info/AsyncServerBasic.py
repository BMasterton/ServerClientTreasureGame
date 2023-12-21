#!/usr/bin/python3.11
from asyncio import run, start_server, StreamReader, StreamWriter
async def echo(reader: StreamReader, writer: StreamWriter) -> None:
    data = await reader.readline() # getting data from the client
    message = data.decode() # data in this case is a string so we decode it
    addr = writer.get_extra_info('peername')
    print(f"Received {message} from {addr}")
    writer.write(data) # starts to write the data to the stream
    await writer.drain() # waits until the data is written
    writer.close()
    await writer.wait_closed()

async def main() -> None:
    server = await start_server(echo, '127.0.0.1', 12345)
    await server.serve_forever() # without this, the program terminates

run(main())

# wait asyncio.start_Server(echo, '127.0.0.1', 12345) starts a new instance of a call to echo; this looks like multithreading but in reality
#there is a single thread jumpong between different instances of echo

# drain waits until it is safe to write to the stream again (or safe to close it ); implements flow control, to avoid buffer overflows
