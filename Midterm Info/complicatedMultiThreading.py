#!/usr/bin/python3.11
from threading import Thread, Semaphore
num = 0

lock = Semaphore()
def called_by_thread():
    global num

    #lets guard our gloablnum from sahred access
    with lock:
        for _ in range(1000000):
            num += 1
thread_list = [] #holds thread objects
for i in range(10): # creatingt 10 diff threads
    thread_list.append(Thread(target=called_by_thread)) # no call to .start as were not stating immediately
    thread_list[-1].start() #adding them all to the thread list and then starting them there, all working at the same time and the pthon nterpreter is donig all the work
# Wait until all threads have completed

for t in thread_list:
    t.join() # "reap" threads etc, will auto end when the threads function ends, if its a client thing it seems like you have exit the client then it will join the thread
    print(num)


# extra info
bits=0b0110
hex=0xF0
bytestring=b'ABC\xFE' # can only have 2 bytes after the x or you need to do another \x as in b'ABC\xFE\xC0
#if you use quotes you're making a string