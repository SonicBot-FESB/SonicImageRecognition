from typing import Callable
import cv2

from Sonic.ImageRecognition.image_processor.prepare_image import (
    crop_image,
    filter_with_opening,
)
from ..storage.image_storage import ImageStorage




async def capture_image(cap, show_image: bool):
    _, frame = cap.read()

    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cropped_frame = crop_image(grayscale)
    mask = filter_with_opening(cropped_frame)

    ImageStorage.set_image(mask)

    if show_image:
        cv2.waitKey(1)
        cv2.imshow("Preview", mask)
    return mask
