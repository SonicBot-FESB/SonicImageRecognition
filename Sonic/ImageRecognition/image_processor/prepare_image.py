import cv2
import numpy as np

from Sonic.ImageRecognition.storage.config_storage import ImageRecognitionConfig


def filter_with_opening(grayscale_frame):
    grayscale_range = ImageRecognitionConfig.get_grayscale_range()

    se = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))
    morphed = cv2.morphologyEx(grayscale_frame, cv2.MORPH_CLOSE, se)

    mask = cv2.inRange(
        morphed,
        np.array([grayscale_range[0]]),
        np.array([grayscale_range[1]]),
    )
    mask = cv2.bitwise_not(mask)

    return mask


def crop_image(frame):
    top_crop, bottom_crop = ImageRecognitionConfig.get_vertical_crop_range()
    left_crop, right_crop = ImageRecognitionConfig.get_horizontal_crop_range()

    max_y = len(frame)
    max_x = len(frame[0])
    mask_croped = frame[top_crop::, left_crop::][
        0 : (max_y - bottom_crop), 0 : (max_x - right_crop)
    ]

    return mask_croped
