from enum import Enum
from os import environ

from Sonic.OcrModel.models import convolutional_nn, fully_connected_nn


class NeuralNetworks(str, Enum):
    fully_connected = "fully_connected"
    convolutional = "convolutional"


neural_network_model_path_map = {
    "fully_connected": environ["FULLY_CONNECTED_MODEL_PATH"],
    "convolutional": environ["CONVOLUTIONAL_MODEL_PATH"],
}

neural_network_module_map = {
    "fully_connected": fully_connected_nn,
    "convolutional": convolutional_nn,
}
