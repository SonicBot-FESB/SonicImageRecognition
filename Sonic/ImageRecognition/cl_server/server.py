import asyncio
import traceback

from ..exceptions import CommandNotImplemented


class ClServer:
    _method_handlers = {}

    _connections = {}

    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def start(self):
        self.server = await asyncio.start_server(self.on_connect, self.host, self.port)

        print("Started server")
        async with self.server:
            await self.server.serve_forever()

    def close(self):
        self.server.close()

    def remove_conn(self, writer: asyncio.StreamWriter):
        conn_data = writer.get_extra_info("peername")
        if conn_data in self._connections:
            print(f"Disconnecting client: {conn_data}")
            self._connections.pop(conn_data)

    async def on_connect(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        conn_data = writer.get_extra_info("peername")
        self._connections[conn_data] = (reader, writer)

        print(f"New client connected {conn_data}")

        while not writer.is_closing():
            await self.handle_incoming_data(reader, writer)

        self.remove_conn(writer)

    async def broadcast_data(self, message: str):
        writer: asyncio.StreamWriter
        connections_copy = [*self._connections.values()]
        for _, writer in connections_copy:
            try:
                writer.write(message.encode())
                await writer.drain()
            except Exception:
                self.remove_conn(writer)

    
    async def handle_incoming_data(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        try:
            data = await reader.read(1000)
        except Exception:
            self.remove_conn(writer)
            return
        message = data.decode()
        message = message.rstrip("\n")

        if not message:
            print("Client disconnected")
            writer.close()
            return

        print(f"Received: {message}")

        command, *args = message.split(" ")
        handler = (
            self._method_handlers.get(command) or self.method_not_implemented_handler
        )
        try:
            response = command
            response_data = handler(command, *args)
            if response_data:
                response_data_str = " ".join(map(str, response_data))
                response = f"{command} {response_data_str}"
        except Exception as ex:
            print(traceback.format_exc())
            response = f"ERR {str(ex)}"
            return

        try:
            writer.write(response.encode())
            await writer.drain()
        except Exception:
            print("Lost connection 2")
            await writer.wait_closed()

     

    def method_not_implemented_handler(self, command, *_):
        raise CommandNotImplemented(f"Method {command} not implemented")

    def register_command_handler(self, command, callback):
        self._method_handlers[command] = callback
