from os import environ
from string import ascii_uppercase

from keras.layers import Dense, Dropout
from keras.models import Sequential, load_model
from keras.utils import to_categorical
from numpy.typing import NDArray


def _build_model(num_classes):
    # Create a neural network with 3 dense layers
    model = Sequential()
    model.add(Dense(512, activation="relu", input_shape=(784,)))
    model.add(Dropout(0.2))
    model.add(Dense(512, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(num_classes, activation="softmax"))

    return model


def train(training_images: NDArray, training_labels: NDArray):
    model_save_path = environ["FULLY_CONNECTED_MODEL_PATH"]

    # Convert class vectors to binary class matrices (transform the problem to multi-class classification)
    num_classes = len(set(training_labels))
    training_labels = to_categorical(training_labels, num_classes)

    model = _build_model(num_classes)
    model.summary()
    model.compile(
        loss="categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"]
    )

    # Train the model
    model.fit(
        training_images,
        training_labels,
        batch_size=128,
        epochs=20,
        verbose=1,
        validation_data=(training_images, training_labels),
    )

    model.save(model_save_path)

def format_input(grayscale_image: NDArray):
    return grayscale_image.reshape(1, 784)
