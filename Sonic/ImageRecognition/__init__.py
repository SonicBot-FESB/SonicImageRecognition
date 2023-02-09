import asyncio
from typing import Callable

from keras.models import Sequential
from Sonic.ImageRecognition.cl_server import cl_server
from Sonic.ImageRecognition import image_processor


async def run(model: Sequential, format_input: Callable):
    await asyncio.gather(cl_server.start(), image_processor.run(model, format_input))
