import asyncio
import time


async def download(name, seconds):
    print(f"{name} started")

    await asyncio.sleep(seconds)

    print(f"{name} finished")


async def main():
    start = time.time()

    await asyncio.gather(
        download("File A", 3),
        download("File B", 2),
        download("File C", 1)
    )

    print(f"Total time: {time.time() - start:.2f} seconds")


asyncio.run(main())
