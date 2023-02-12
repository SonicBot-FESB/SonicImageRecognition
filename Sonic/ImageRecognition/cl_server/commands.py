from os import environ

from Sonic.ImageRecognition.predict_character import predict_character
from ..storage.config_storage import ImageRecognitionConfig
from ..storage.image_storage import ImageStorage


def handle_set_resolution(_, resolution_name: str):
    ImageRecognitionConfig.set_resolution(resolution_name)


def handle_get_image(_):
    image_base64, captured_at = ImageStorage.get_image_base64()
    return image_base64, captured_at


def handle_set_vertical_crop(_, *args: str):
    try:
        top_offset = int(args[0])
        bottom_offset = int(args[1])
    except:
        raise ValueError(f"Invalid arguments: {args}")
    ImageRecognitionConfig.set_vertical_crop(top_offset, bottom_offset)


def handle_set_horizontal_crop(_, *args: str):
    try:
        left_offset = int(args[0])
        right_offset = int(args[1])
    except:
        raise ValueError(f"Invalid arguments: {args}")
    ImageRecognitionConfig.set_horizontal_crop(left_offset, right_offset)


def handle_turn_on(_):
    ImageRecognitionConfig.start()


def handle_turn_off(_):
    ImageRecognitionConfig.stop()


def handle_get_status(_):
    return [int(ImageRecognitionConfig.is_running())]


def handle_set_grayscale_filter(_, *args: str):
    try:
        lower_limit = int(args[0])
        upper_limit = int(args[1])
    except Exception:
        raise ValueError(f"Invalid arguments: {args}")

    ImageRecognitionConfig.set_grayscale_range(lower_limit, upper_limit)


def handle_set_white_treshold(_, *args: str):
    try:
        white_treshold = int(args[0])
    except Exception:
        raise ValueError(f"Invalid arguments: {args}")

    ImageRecognitionConfig.set_white_percentage_prediction_treshold(white_treshold)


def handle_ping(_):
    return ["PONG"]


def handle_predict_character(_, *args):
    mask = ImageStorage.get_image() 
    model, format_input = ImageRecognitionConfig.get_model_config()

    if not all((mask is not None, model, format_input)):
        return ["A", "0"]

    prediction_data = predict_character(
        mask,
        model,
        format_input,
    )

    return [
        prediction_data["character"],
        prediction_data["probability"],
    ]


def get_character_detected_message():
    return "CHR"
