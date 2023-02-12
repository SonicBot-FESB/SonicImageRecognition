from os import environ
from typing import Callable

from keras.models import Sequential

import numpy as np
from numpy.typing import NDArray

from Sonic.OcrModel import models


VERBOSE = environ.get("VERBOSE", "False") == "True"

def predict_character(
    grayscale_image: NDArray, model: Sequential, format_input: Callable
):
    mask_resized, predictions = models.predict_from_grayscale(
        model,
        format_input,
        grayscale_image,
        verbose=VERBOSE,
    )

    predictions_uhs = [
        predictions[0][7],  # H
        predictions[0][18],  # S
        predictions[0][20],  # U
    ]
    label_values = "HSU"
    max_label = np.argmax(predictions_uhs)

    return {
        "formated_input": mask_resized,
        "character": label_values[max_label],
        "probability": round(predictions[0][max_label] * 100, 2),
    }
