import asyncio
from typing import Callable

from keras.models import Sequential
from Sonic.ImageRecognition.cl_server import cl_server
from Sonic.ImageRecognition import image_processor
from Sonic.ImageRecognition.storage.config_storage import ImageRecognitionConfig


async def run(model: Sequential, format_input: Callable):
    ImageRecognitionConfig.configure_prediction_model(model, format_input)
    await asyncio.gather(cl_server.start(), image_processor.run())
