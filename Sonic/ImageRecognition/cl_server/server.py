import asyncio
import traceback

from ..exceptions import CommandNotImplemented


class ClServer:
    _method_handlers = {
        "RES": None, # SET RESOLUTION
        "IMG": None, # GET IMAGE
        "SVC": None, # SET VERTICAL CROP
        "SHC": None, # SET HORIZONTAL CROP
        "ONN": None, # START IMAGE PROCESSING LOOP
        "OFF": None, # STOP IMAGE PROCESSING LOOP
        "STT": None, # GET RUNING STATUS
        "GSF": None, # SET GRAYSCALE FILTER
        "PNG": None, # PING
    }

    def __init__(self, host, port):
        self.host = host
        self.port = port


    async def start(self):
        self.server = await asyncio.start_server(
            self.on_connect, self.host, self.port
        )

        print("Started server")
        async with self.server:
            await self.server.serve_forever()

    def close(self):
        self.server.close()


    async def on_connect(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data = await reader.read(1000)
        message = data.decode()
        message = message.rstrip("\n")
        print(f"Received: {message}")
        
        command, *args = message.split(" ")
        handler = self._method_handlers.get(command) or self.method_not_implemented_handler
        try:
            response = command
            response_data = handler(command, *args)
            if response_data:
                response_data_str = " ".join(map(str, response_data))
                response = f"{command} {response_data_str}"
        except Exception as ex:
            print(traceback.format_exc())
            response = f"ERR {str(ex)}"

        writer.write(response.encode())
        await writer.drain()


    def method_not_implemented_handler(self, command, *_):
        raise CommandNotImplemented(f"Method {command} not implemented")


    def regsiter_command_handler(self, command, callback):
        if command not in self._method_handlers:
            raise KeyError(f"Command: {command} not recognized")
        self._method_handlers[command] = callback
