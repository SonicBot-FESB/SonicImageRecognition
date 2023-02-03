from os import environ

import numpy as np

from Sonic.OcrModel.utils.progress_bar import print_progress


def download_dataset():
    print(
        """
        Download the kaggle az handwritten alphabets dataset from this url:
        https://www.kaggle.com/datasets/sachinpatel21/az-handwritten-alphabets-in-csv-format

        Once downloaded extract its contents into the assets folder.
        """
    )


def _load_az_row(row):
    row = row.rstrip("\n")
    row_cells = row.split(",")

    label = int(row_cells[0])

    # image is flattened into an array of 784 grayscale values
    image = np.array(
        row_cells[1:],
        dtype="uint8",
    )

    return image, label


def load_dataset():
    total_labels = 26  # Number of characters in the alphabet

    dataset_path = environ["AZ_DATASET_PATH"]

    images = []
    labels = []

    with open(dataset_path, "r") as dataset_fp:
        for row in dataset_fp:
            image, label = _load_az_row(row)
            images.append(image)
            labels.append(label)
            print_progress(
                iteration=(label + 1),
                total=total_labels,
            )

    images = np.array(images, dtype="float32")
    labels = np.array(labels, dtype="int")

    return (
        images,
        labels,
    )
