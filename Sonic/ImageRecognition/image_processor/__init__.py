import asyncio
from typing import Callable
import cv2
from ..storage.config_storage import ImageRecognitionConfig
from ..storage.image_storage import ImageStorage
from os import environ

import numpy as np
from keras.models import Sequential

from Sonic.OcrModel import models
from Sonic.OcrModel.models import convolutional_nn



def _filter_with_opening(grayscale_frame):
    grayscale_range = ImageRecognitionConfig.get_grayscale_range()

    se = cv2.getStructuringElement(cv2.MORPH_RECT, (6,6))
    morphed = cv2.morphologyEx(grayscale_frame, cv2.MORPH_CLOSE, se)
    
    mask = cv2.inRange(
        morphed, np.array([grayscale_range[0]]),
        np.array([grayscale_range[1]]),
    )
    mask = cv2.bitwise_not(mask)

    return mask

def _crop_image(frame):
    top_crop, bottom_crop = ImageRecognitionConfig.get_vertical_crop_range()
    left_crop, right_crop = ImageRecognitionConfig.get_horizontal_crop_range()
    
    max_y = len(frame)
    max_x = len(frame[0])
    mask_croped = frame[
        top_crop::, left_crop::
    ][
        0:(max_y - bottom_crop), 0:(max_x - right_crop)
    ]

    return mask_croped


async def process_image(model: Sequential, format_input: Callable):
    SHOW_IMAGE = environ["SHOW_IMAGE"]

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        ImageRecognitionConfig.stop()

    print("Reading camera")
    while True:
        if not ImageRecognitionConfig.is_running():
            await asyncio.sleep(0.001)
        
        ret, frame = cap.read()

        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cropped_frame = _crop_image(grayscale)
        mask = _filter_with_opening(cropped_frame)

        ImageStorage.set_image(mask)
        
        mask_resized, predictions = models.predict_from_grayscale(
            model,
            format_input,
            mask,
            verbose=False,
        )
        predictions_uhs = [
            predictions[0][7], # H
            predictions[0][18], # S
            predictions[0][20], # U
        ]
        uhs = "HSU"
        max_index = np.argmax(predictions_uhs)
        print(f"{uhs[max_index]} - {round(predictions_uhs[max_index] * 100, 2)}%")

        if SHOW_IMAGE:
            cv2.waitKey(1)
            cv2.imshow("Preview", mask)
            cv2.imshow("Preview resized", mask_resized.reshape(28, 28, 1))

        await asyncio.sleep(0.001) 
