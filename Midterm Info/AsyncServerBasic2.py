#!/usr/bin/python3.11
from asyncio import run, start_server, StreamReader, StreamWriter
cnx = 0
async def echo(reader: StreamReader, writer: StreamWriter) -> None:
    global cnx
    try:
        local_id = cnx
        cnx += 1
        while True:
            data = await reader.readline()
            if data == b'':
                break
            message = data.decode()
            print(f"{local_id} {data}")
            writer.write(data) # starts to write the data to the stream
            await writer.drain() # waits until the data is written
        writer.close()
        await writer.wait_closed()
    except Exception:
        pass


async def main() -> None:
    server = await start_server(echo, '127.0.0.1', 12345)
    await server.serve_forever() # without this, the program terminates


run(main())