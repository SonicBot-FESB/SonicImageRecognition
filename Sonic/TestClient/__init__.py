import asyncio
from os import environ
from base64 import b64decode
from dotenv import load_dotenv

load_dotenv(override=True)

SERVER_HOST = environ["SERVER_HOST"]
SERVER_PORT = environ["SERVER_PORT"]


def save_b64_image(image_b64: str):
    image_jpg = b64decode(image_b64)
    with open("assets/test.jpg", "wb+") as file:
        file.write(image_jpg)


async def tcp_client(message: str):
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter

    reader, writer = await asyncio.open_connection(
        SERVER_HOST,
        SERVER_PORT,
    )

    writer.write((message).encode())
    await writer.drain()

    data = await reader.read(100000)
    print(f"Received: {data.decode()}")

    command, *response = data.decode().split(" ")
    if command == "IMG":
        save_b64_image(response[0])

    writer.close()
    await writer.wait_closed()


def run():
    while msg := input("Command: "):
        if not msg or msg == "Q":
            break
        asyncio.run(tcp_client(msg))
