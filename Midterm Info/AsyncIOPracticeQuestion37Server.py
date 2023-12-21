# !/usr/bin/python3.11
from asyncio import run, start_server, StreamReader, StreamWriter


NUMBERS = ['1','2','3','4','5','6','7','8','9','0']
async def digitCounter(reader: StreamReader, writer: StreamWriter) -> None:
    try:
        data = await reader.readline()
        decoded_data = data.decode().strip()
        counter = 0
        for ch in decoded_data:
            if ch in NUMBERS: # or better yet if ch.isdigit():
                counter +=1
        writer.write(str(counter).encode('utf-8') + b'\n')
        await writer.drain()
    except Exception as e:
        print(e)
    writer.close()
    await writer.wait_closed()





async def main():
    server = await start_server(digitCounter, '', 22222)
    await server.serve_forever()

run(main())


#Question
# Using asyncio, write a server that listens on port 22222 and accepts a string of text,
# followed by a newline, then returns the number of digits found in that string to the
# client. For example:
# echo "abcde" | nc localhost 22222
# 0
# echo "ics226" | nc localhost 22222
# 3
# Do not pack any numbers; use only strings. Use only asyncio; do not use any other
# libraries.