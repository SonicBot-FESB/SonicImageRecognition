from typing import Callable
import cv2
from Sonic.ImageRecognition.image_processor.predict_character import predict_character

from Sonic.ImageRecognition.image_processor.prepare_image import (
    crop_image,
    filter_with_opening,
)
from ..storage.image_storage import ImageStorage

from keras.models import Sequential


def capture_image(cap, model: Sequential, format_input: Callable, show_image: bool):
    _, frame = cap.read()

    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cropped_frame = crop_image(grayscale)
    mask = filter_with_opening(cropped_frame)

    prediction_data = predict_character(
        mask,
        model,
        format_input,
    )

    ImageStorage.set_image(mask)

    if show_image:
        print(f"{prediction_data['character']} - {prediction_data['probability']}%")
        cv2.waitKey(1)
        cv2.imshow("Preview", mask)
        cv2.imshow(
            "Preview resized", prediction_data["formated_input"].reshape(28, 28, 1)
        )
