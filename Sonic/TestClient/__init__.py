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


async def tcp_client():
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter

    reader, writer = await asyncio.open_connection(
        SERVER_HOST,
        SERVER_PORT,
    )
    return reader, writer


async def send_msg(reader, writer, message:str):
    writer.write((message).encode())
    await writer.drain()

    data = await reader.read(100000)
    print(f"Received: {data.decode()}")

    command, *response = data.decode().split(" ")
    if command == "IMG":
        save_b64_image(response[0])


def run():
    loop = asyncio.get_event_loop()
    reader, writer = loop.run_until_complete(tcp_client())
    print(reader, writer)

    while msg := input("Command: "):
        if not msg or msg == "Q":
            break
        loop.run_until_complete(send_msg(reader, writer, msg))

    writer.close()
    loop.run_until_complete(writer.wait_closed())
