from . import commands as cmd
from .server import ClServer
from .. import config

cl_server = ClServer(config.SERVER_HOST, config.SERVER_PORT)

cl_server.regsiter_command_handler("RES", cmd.handle_set_resolution)
cl_server.regsiter_command_handler("IMG", cmd.handle_get_image)
cl_server.regsiter_command_handler("SVC", cmd.handle_set_vertical_crop)
cl_server.regsiter_command_handler("SHC", cmd.handle_set_horizontal_crop)
cl_server.regsiter_command_handler("ONN", cmd.handle_turn_on)
cl_server.regsiter_command_handler("OFF", cmd.handle_turn_off)
cl_server.regsiter_command_handler("STT", cmd.handle_get_status)
cl_server.regsiter_command_handler("PNG", cmd.handle_ping)
cl_server.regsiter_command_handler("GSF", cmd.handle_set_grayscale_filter)
