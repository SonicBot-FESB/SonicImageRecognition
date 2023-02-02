import numpy as np
import dotenv
from os import environ
from datetime import datetime
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout
from keras.utils import to_categorical
from PIL import Image
import os
import string
import time




def load_az_character(row):
    row = row.rstrip("\n")
    row_data = row.split(",")
    label = int(row_data[0])

    image = np.array(
        row_data[1:],
        dtype="uint8",
    )

    return label, image


BATCH_SIZE = 32
EPOCHS = 50

def load_az_dataset(dataset_path):
    data = []
    labels = []

    if os.path.exists("assets/labels.npy") and os.path.exists("assets/images.npy"):
        print("PICKLES EXIST, LOADING...")
        labels = np.load("assets/labels.npy")
        images = np.load("assets/images.npy")
        return images, labels


    print("LOADING DATASET")
    with open(dataset_path, "r") as dataset_fp:
        for row in dataset_fp:
            label, image = load_az_character(row)
            data.append(image)
            labels.append(label)

    data = np.array(data, dtype="float32")
    labels = np.array(labels, dtype="int")


    np.save("assets/labels.npy", labels)
    np.save("assets/images.npy", data)

    return data, labels

def train_model(training_data, training_labels):
    print(set(training_labels))
    print(len(set(training_labels)))
    print("START TRAINING")

    # Convert class vectors to binary class matrices (transform the problem to multi-class classification)
    num_classes = 26
    training_labels = to_categorical(training_labels, num_classes)

    # Create a neural network with 3 dense layers
    model = Sequential()
    model.add(Dense(512, activation="relu", input_shape=(784,)))
    model.add(Dropout(0.2))
    model.add(Dense(512, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(num_classes, activation="softmax"))
    model.summary()
    model.compile(loss="categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

    # Train the model
    model.fit(training_data, training_labels, batch_size=128, epochs=20, verbose=1,
              validation_data=(training_data, training_labels))

    # Save the model
    model.save("assets/model.h5")


def load_model_file() -> Sequential:
    return load_model("assets/model.h5")

def test_model(model):
    image = Image.open("assets/test.jpg")
    image = image.resize((28, 28))
    image.save("assets/pilled.jpg")
    np_image = np.asarray(image)
    np_image = np_image.reshape(1, 784)
    start = time.time()
    predicted = model.predict(np_image)
    end = time.time()
    print(f"DURATION: {end-start}")

    for index, prediction in enumerate(predicted[0]):
        print(f"{string.ascii_uppercase[index]} - {round(prediction * 100, 2)}%")


def test_model_with_cap(model, mask):
    np_image = mask.reshape(1, 784)
    predicted = model.predict(np_image)
    max_index = np.argmax(predicted[0])
    print(f"{string.ascii_uppercase[max_index]} - {predicted[0][max_index]}")


if __name__ == "__main__":
    AZ_DATASET_PATH = environ["AZ_DATASET_PATH"]
    print(AZ_DATASET_PATH)

    # az_dataset = load_az_dataset(AZ_DATASET_PATH)
    # train_model(az_dataset[0], az_dataset[1])

    model = load_model_file()
    test_model(model)
