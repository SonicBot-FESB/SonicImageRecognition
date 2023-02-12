from . import commands as cmd
from .server import ClServer
from .. import config

cl_server = ClServer(config.SERVER_HOST, config.SERVER_PORT)

cl_server.register_command_handler("RES", cmd.handle_set_resolution) # SET RESOLUTION
cl_server.register_command_handler("IMG", cmd.handle_get_image) # GET IMAGE
cl_server.register_command_handler("SVC", cmd.handle_set_vertical_crop) # SET VERTICAL CROP
cl_server.register_command_handler("SHC", cmd.handle_set_horizontal_crop) # SET HORIZONTAL CROP
cl_server.register_command_handler("ONN", cmd.handle_turn_on) # START IMAGE PROCESSING LOOP
cl_server.register_command_handler("OFF", cmd.handle_turn_off) # STOP IMAGE PROCESSING LOOP
cl_server.register_command_handler("STT", cmd.handle_get_status) # GET STATUS
cl_server.register_command_handler("PNG", cmd.handle_ping) # PING
cl_server.register_command_handler("GSF", cmd.handle_set_grayscale_filter) # SET GRAYSCALE FILTER 
cl_server.register_command_handler("WTS", cmd.handle_set_white_treshold) # SET WHITE COLOR PERCENTAGE PREDICTION TRESHOLD
cl_server.register_command_handler("PRD", cmd.handle_predict_character) # GET PREDICTION FOR LAST CPATURED IMAGE
