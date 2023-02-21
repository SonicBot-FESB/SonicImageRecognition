import asyncio
from typing import Callable
from Sonic.ImageRecognition.storage.image_storage import ImageStorage

from numpy.typing import NDArray
from Sonic.ImageRecognition.cl_server import cl_server
from Sonic.ImageRecognition.cl_server.commands import get_character_detected_message
import cv2

from Sonic.ImageRecognition.image_processor.capture_image import capture_image
from ..storage.config_storage import ImageRecognitionConfig
from os import environ
import numpy as np


def calculat_white_percentage(mask: NDArray):
    total_pixels = mask.shape[0] * mask.shape[1]
    return (np.count_nonzero(mask) / total_pixels) * 100


async def run():
    show_image = int(environ["SHOW_IMAGE"])
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        ImageRecognitionConfig.stop()

    while True:
        if not ImageRecognitionConfig.is_running():
            await asyncio.sleep(0.001)
            continue

        mask = await capture_image(cap, bool(show_image))
        white_percentage = calculat_white_percentage(mask)

        if (
            not ImageRecognitionConfig.should_predict(white_percentage) or 
            ImageStorage.get_character_detected_freshness() < 0.3
        ):
            await asyncio.sleep(0.001)
            continue
            
        ImageStorage.character_detected()
        chr_message = get_character_detected_message() 
        await cl_server.broadcast_data(chr_message)

        await asyncio.sleep(0.001)
