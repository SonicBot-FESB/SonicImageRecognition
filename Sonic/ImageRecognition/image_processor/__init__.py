import asyncio
from typing import Callable
from Sonic.ImageRecognition.cl_server import cl_server
from Sonic.ImageRecognition.cl_server.commands import get_prediction_response
import cv2

from Sonic.ImageRecognition.image_processor.capture_image import capture_image
from ..storage.config_storage import ImageRecognitionConfig
from os import environ

from keras.models import Sequential


async def run(model: Sequential, format_input: Callable):
    show_image = int(environ["SHOW_IMAGE"])
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        ImageRecognitionConfig.stop()

    while True:
        if not ImageRecognitionConfig.is_running():
            await asyncio.sleep(0.001)

        prediction_data = await capture_image(cap, model, format_input, bool(show_image))
        prediction_response = get_prediction_response(prediction_data)
        if prediction_response:
            await cl_server.broadcast_data(prediction_response)

        await asyncio.sleep(0.001)
