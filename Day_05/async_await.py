import asyncio

async def task(name):
    print(f"{name} started")
    await asyncio.sleep(2)
    print(f"{name} finished")

async def main():
    t1 = asyncio.create_task(task("Task 1"))
    t2 = asyncio.create_task(task("Task 2"))

    await t1
    await t2

asyncio.run(main())

 # Output:-
 
# Task 1 started
# Task 2 started
# Task 1 finished
# Task 2 finished

#---- Both wait together → concurrency


# Example:-


import asyncio

async def fetch_data(index):
    print(f"Fetching data {index}...")
    await asyncio.sleep(2)   # Non-blocking wait.
    return f"Result {index}"

async def main():
    # Create tasks
    t1 = asyncio.create_task(fetch_data(1))
    t2 = asyncio.create_task(fetch_data(2))
    t3 = asyncio.create_task(fetch_data(3))

    # Wait for all tasks to complete
    results = await asyncio.gather(t1, t2, t3)

    print(results)

asyncio.run(main())



# Threadpool- Executor (managing Threads):-
from concurrent.futures import ThreadPoolExecutor
import time

def download(i):
    print(f"Download {i} started")
    time.sleep(2)
    return f"File {i}"

with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(download, [1,2,3])
    print(list(results))


# Multi-Processings:--

from multiprocessing import Process

def work(n):
    for _ in range(1_000_000):
        n*n

p1 = Process(target=work, args=(10,))
p2 = Process(target=work, args=(20,))

p1.start()
p2.start()

p1.join()
p2.join()


# ProcessPool- Executor:--
from concurrent.futures import ProcessPoolExecutor

def heavy(x):
    return x*x

with ProcessPoolExecutor() as executor:
    results = executor.map(heavy, range(10))

print(list(results))



