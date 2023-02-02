from os import environ

from keras.layers import Dense, Dropout, Flatten, Convolution2D, MaxPooling2D
from keras.models import Sequential
from keras.utils import to_categorical
from numpy.typing import NDArray


def _build_model(num_classes):
    # Create a neural network with 2 convolutional layers and 2 dense layers
    model = Sequential()
    model.add(Convolution2D(32, 3, 3, activation="relu", input_shape=(28, 28, 1)))
    model.add(Convolution2D(32, 3, 3, activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation="softmax"))

    return model


def train(training_images: NDArray, training_labels: NDArray):
    model_save_path = environ["CONVOLUTIONAL_MODEL_PATH"]
    training_images = training_images.reshape(
        training_images.shape[0],
        28,
        28,
        1,
    )
    num_classes = len(set(training_labels))

    training_labels = to_categorical(training_labels, num_classes)
    model = _build_model(num_classes)

    model.summary()
    model.compile(
        loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
    )

    # Train the model
    model.fit(
        training_images,
        training_labels,
        batch_size=32,
        epochs=10,
        verbose=1,
        validation_data=(training_images, training_labels),
    )

    # Save the model
    model.save(model_save_path)

def format_input(grayscale_image: NDArray):
    return grayscale_image.reshape(1, 28, 28, 1)
