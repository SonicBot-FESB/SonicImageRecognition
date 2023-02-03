import asyncio
from typing import Callable
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

        capture_image(cap, model, format_input, bool(show_image))
        await asyncio.sleep(0.001)
