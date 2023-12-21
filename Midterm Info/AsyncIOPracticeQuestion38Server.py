# !/usr/bin/python3.11
from asyncio import run, start_server, StreamReader, StreamWriter

PUNC = ['.', ',', '!', '?', ';', ':']
async def punctuationFinder(reader: StreamReader, writer: StreamWriter):
    try:
        data = await reader.readline()
        decoded_data = data.decode().strip()
        counter = 0
        for ch in decoded_data:
            if ch in PUNC:
                counter +=1
        writer.write(str(counter).encode('utf-8') + b'\n')
    except Exception as e:
        print(e)
    writer.close()
    await writer.wait_closed()




async def main():
    server = await start_server(punctuationFinder, '', 33333)
    await server.serve_forever()

run(main())


## Question
# 
# Using asyncio, write a server that listens on port 33333 and accepts a string of text,
# followed by a newline, then returns the number of punctuation symbols (specifically:
# .,:;? ) that were found, to the client. For example:
# echo "a. bc, defgh" | nc localhost 33333
# 2
# echo "...???" | nc localhost 33333
# 6
# echo "Aeiou" | nc localhost 33333
# 0
# Use only asyncio; do not use any other libraries.