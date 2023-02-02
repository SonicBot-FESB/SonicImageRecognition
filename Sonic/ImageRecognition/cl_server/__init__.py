from . import commands as cmd
from .server import ClServer
from .. import config

server = ClServer(
    config.SERVER_HOST,
    config.SERVER_PORT
)

server.regsiter_command_handler("RES", cmd.handle_set_resolution)
server.regsiter_command_handler("IMG", cmd.handle_get_image)
server.regsiter_command_handler("SVC", cmd.handle_set_vertical_crop)
server.regsiter_command_handler("SHC", cmd.handle_set_horizontal_crop)
server.regsiter_command_handler("ONN", cmd.handle_turn_on)
server.regsiter_command_handler("OFF", cmd.handle_turn_off)
server.regsiter_command_handler("STT", cmd.handle_get_status)
server.regsiter_command_handler("PNG", cmd.handle_ping)
server.regsiter_command_handler("GSF", cmd.handle_set_grayscale_filter)
