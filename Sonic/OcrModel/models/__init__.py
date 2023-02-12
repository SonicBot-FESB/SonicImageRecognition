from typing import Callable
from PIL import Image
from keras.models import Sequential, load_model
from string import ascii_uppercase
import numpy as np
from numpy.typing import NDArray
import cv2


def load_model_file(path) -> Sequential:
    return load_model(path)


def predict_image(
    model: Sequential,
    format_input: Callable,
    path: str,
    classes_map=ascii_uppercase,
    verbose=True,
):
    image = Image.open(path)
    image = image.resize((28, 28))
    np_image = np.asarray(image)

    np_image = format_input(np_image)

    predicted = model.predict(np_image)

    if not verbose:
        return predicted

    for index, prediction in enumerate(predicted[0]):
        print(f"{classes_map[index]} - {round(prediction * 100, 2)}%")

    return predicted


def predict_from_grayscale(
    model: Sequential,
    format_input: Callable,
    grayscale_image: NDArray,
    classes_map=ascii_uppercase,
    verbose=True,
):
    mask_resized = cv2.resize(
        grayscale_image,
        dsize=(28, 28),
        interpolation=cv2.INTER_NEAREST_EXACT,
    )
    mask_resized = format_input(mask_resized)
    predicted = model.predict(mask_resized, verbose=verbose)

    if not verbose:
        return mask_resized, predicted

    for index, prediction in enumerate(predicted[0]):
        print(f"{classes_map[index]} - {round(prediction * 100, 2)}%")

    return mask_resized, predicted
