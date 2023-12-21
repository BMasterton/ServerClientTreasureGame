# !/usr/bin/python3.11
from asyncio import run, start_server, StreamReader, StreamWriter

VOWELS = ['a','e','i','o','u'] # list of all values cause checking for lowercase with base python is hard
async def lowerCaseFinder(reader: StreamReader, writer: StreamWriter) -> None:
    try:
        # while True: # seemingly as were only going to ask this once we dont need a while True
        returnMessage = b'OK'
        data = await reader.readline()
        decoded_data = data.decode().strip()
        for ch in decoded_data:
            if ch not in VOWELS:
                returnMessage = b'NO'
                break
        writer.write(returnMessage + b'\n')
        await writer.drain()
    except Exception as e:
        print(e)
    writer.close()
    await writer.wait_closed()



async def main():
    server = await start_server(lowerCaseFinder, '', 11111)
    await server.serve_forever()

run(main())


#Question
# Using asyncio, write a server that listens on port 11111 and accepts a string of text,
# followed by a newline, then returns 'OK' to the client if the string contains only
# lower-case vowels, 'NO' otherwise. For example:
# echo "abcde" | nc localhost 11111
# NO
# echo "aeiou" | nc localhost 11111
# OK
# echo "Aeiou" | nc localhost 11111
# NO
# Use only asyncio; do not use any other libraries.