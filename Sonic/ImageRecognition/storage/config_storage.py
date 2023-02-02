from ..exceptions import InvalidVideoResolution, InvalidRange, OCRInProgress


VIDEO_RESOLUTIONS = {
    "1080p": (1920, 1080),
    "720p": (1280, 720),
    "480p": (854, 480),
    "360p": (640, 360),
    "240p": (426, 240),
}

class ImageRecognitionConfig:
    _run_ocr = True
    _grayscale_range = [182, 255]
    _resolution = VIDEO_RESOLUTIONS["720p"]

    _vertical_crop_range = [0, 0]
    _horizontal_crop_range = [0, 0]

    @classmethod
    def stop(cls):
        cls._run_ocr = False

    @classmethod
    def start(cls):
        cls._run_ocr = True
    
    @classmethod
    def is_running(cls):
        return cls._run_ocr

    @classmethod
    def set_resolution(cls, resolution_name):
        if cls._run_ocr:
            raise OCRInProgress("Can't change resolution while ocr is running")
        if resolution_name not in VIDEO_RESOLUTIONS:
            raise InvalidVideoResolution(f"Invalid video resolution: {resolution_name}")

        cls._resolution = VIDEO_RESOLUTIONS[resolution_name]

    @classmethod
    def get_resolution(cls):
        return cls._resolution

    @classmethod
    def set_vertical_crop(cls, top_offset, bottom_offset):
        max = cls._resolution[0]
        if top_offset > max or bottom_offset > max or top_offset < 0 or bottom_offset < 0:
            InvalidRange(f"Invalid crop range: [{top_offset}, {bottom_offset}]")
        cls._vertical_crop_range = [top_offset, bottom_offset]

    @classmethod
    def get_vertical_crop_range(cls):
        return cls._vertical_crop_range

    @classmethod
    def set_horizontal_crop(cls, left_offset, right_offset):
        max = cls._resolution[1]
        if left_offset > max or right_offset > max or left_offset < 0 or right_offset < 0:
            InvalidRange(f"Invalid crop range: [{left_offset}, {right_offset}]")
        cls._horizontal_crop_range = [left_offset, right_offset]

    @classmethod
    def get_horizontal_crop_range(cls):
        return cls._horizontal_crop_range

    @classmethod
    def set_grayscale_range(cls, lower_limit, upper_limit):
        is_bottom_valid = (0 <= lower_limit <= 255)
        is_top_valid = (0 <= upper_limit <= 255)

        if not (is_top_valid and is_bottom_valid):
            raise InvalidRange(f"Invalid grayscale range: [{lower_limit}, {upper_limit}]")

        cls._grayscale_range[0] = lower_limit
        cls._grayscale_range[1] = upper_limit

    @classmethod
    def get_grayscale_range(cls):
        return cls._grayscale_range
