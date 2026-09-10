import asyncio
import time


async def task(name):
    print(f"{name} started")
    await asyncio.sleep(2)
    print(f"{name} finished")


async def main():
    await asyncio.gather(
        task("Task 1"),
        task("Task 2"),
        task("Task 3")
    )


start = time.time()

asyncio.run(main())

end = time.time()

print(f"Total time: {end - start:.2f} seconds")
