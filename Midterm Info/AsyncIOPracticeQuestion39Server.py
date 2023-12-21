# !/usr/bin/python3.11
from asyncio import run, start_server, StreamReader, StreamWriter
sum = 0
async def sumFunc(reader: StreamReader, writer: StreamWriter)-> None:
    global sum
    try:
        while True:
            data = await reader.readline()
            decoded_data = data.decode().strip()
            if data == b'':
                break
            if decoded_data == '*':
                writer.write(str(sum).encode())
                await writer.drain()
            else:
                sum += int(decoded_data)

    except Exception as e:
        print(e)
    writer.close()
    writer.wait_closed()



async def main():
    server = await start_server(sumFunc, '', 33333)
    await server.serve_forever()

run(main())