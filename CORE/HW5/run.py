# run.py
import asyncio
import subprocess

async def run_server():
    process = await asyncio.create_subprocess_exec(
        "python", "server.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    while True:
        line = await process.stdout.readline()
        if not line:
            break
        print(line.decode().strip())

async def run_client():
    process = await asyncio.create_subprocess_exec(
        "python", "client.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    while True:
        line = await process.stdout.readline()
        if not line:
            break
        print(line.decode().strip())


    while True:
        line = await process.stdout.readline()
        if not line:
            break
        print(line.decode().strip())

async def main():
    server_task = asyncio.create_task(run_server())
    client_task = asyncio.create_task(run_client())

    try:
        await asyncio.gather(server_task, client_task)
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Cancelling tasks...")
        server_task.cancel()
        client_task.cancel()

        await asyncio.gather(server_task, client_task, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())
