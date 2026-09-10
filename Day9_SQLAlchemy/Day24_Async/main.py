from fastapi import FastAPI
import time
import asyncio

app = FastAPI()


@app.get("/sync")
def sync_endpoint():
    print("Sync started")

    time.sleep(3)

    print("Sync finished")

    return {"message": "Sync done"}


@app.get("/async")
async def async_endpoint():
    print("Async started")

    await asyncio.sleep(3)

    print("Async finished")

    return {"message": "Async done"}