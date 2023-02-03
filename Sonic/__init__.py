from dotenv import load_dotenv

load_dotenv(override=True)

import asyncio
import typer

import Sonic.ImageRecognition as ImageRecognition
import Sonic.OcrModel as OcrModel
from Sonic.OcrModel.consts import NeuralNetworks
import Sonic.TestClient as TestClient


app = typer.Typer()


@app.command()
def image_recognition(network: NeuralNetworks):
    model_path = OcrModel.consts.neural_network_model_path_map[network]
    model = OcrModel.models.load_model_file(model_path)
    module_nn = OcrModel.consts.neural_network_module_map[network]
    asyncio.run(ImageRecognition.run(model, module_nn.format_input))


@app.command()
def test_client():
    TestClient.run()


@app.command()
def train(network: NeuralNetworks):
    module_nn = OcrModel.consts.neural_network_module_map[network]
    images, labels = OcrModel.datasets.az_dataset.load_dataset()

    module_nn.train(images, labels)


@app.command()
def predict(network: NeuralNetworks, image_path: str):
    module_nn = OcrModel.consts.neural_network_module_map[network]
    model_path = OcrModel.consts.neural_network_model_path_map[network]

    model = OcrModel.models.load_model_file(model_path)

    OcrModel.models.predict_image(model, module_nn.format_input, image_path)
