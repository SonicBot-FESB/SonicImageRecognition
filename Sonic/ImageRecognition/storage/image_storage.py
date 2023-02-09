from typing import Union
from datetime import datetime
from numpy import ndarray
from base64 import b64encode
import cv2


class ImageStorage:
    _image: Union[ndarray, None] = None
    _captured_at = None

    @classmethod
    def set_image(cls, img: ndarray):
        cls._image = img
        cls._captured_at = datetime.now().timestamp()

    @classmethod
    def get_image_base64(cls):
        if cls._image is None or cls._captured_at is None:
            raise PermissionError("Cannot access image, image processing not started")
        retval, buffer = cv2.imencode(".jpg", cls._image)
        base64_img = b64encode(buffer).decode()
        return base64_img, cls._captured_at
