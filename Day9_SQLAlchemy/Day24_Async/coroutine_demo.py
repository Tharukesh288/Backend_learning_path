import asyncio


async def task():
    print("Task is running")
    await asyncio.sleep(2)
    print("Task is finished")


result = task()

print(result)
print(type(result))
