import asyncio
from typing import Callable

from keras.models import Sequential 
from Sonic.ImageRecognition.cl_server import server
from Sonic.ImageRecognition.image_processor import process_image

async def run(model: Sequential, format_input: Callable):
    await asyncio.gather(
        server.start(),
        process_image(model, format_input),
    )
