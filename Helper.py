"""
@version: python3.7
@author: ‘mengyuantan‘
@contact: tanmy1016@126.com
@time: 2019/12/31 17:04
"""

import json
import numpy as np

CONFIG_FILE = './config.json'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    config = json.load(f)
    TIME_ARRAY_LENGTH = config["TIME_ARRAY_LENGTH"]
    MAXIMUM_TIME = config["MAXIMUM_TIME"]
    REFLECT_TIMES = config["REFLECT_TIMES"]
    ROOM_SIZE = config["ROOM_SIZE"]
    RX_HEIGHT = config["RX_HEIGHT"]
    FOV = config["FOV"]
    WALL_NODE_NUM = config["WALL_NODE_NUM"]


try:
    room_size = list(map(int, ROOM_SIZE.split("*")))
except:
    raise ImportError("ROOM_SIZE can't resolve.")
try:
    wall_node_num = list(map(int, WALL_NODE_NUM.split("*")))
except:
    raise ImportError("WALL_NODE_NUM can't resolve.")


ROOM_X_LEN, ROOM_Y_LEN, ROOM_Z_LEN = room_size[0], room_size[1], room_size[2]
WALL_NODE_NUM_X, WALL_NODE_NUM_Y = wall_node_num[0], wall_node_num[1]
# todo
MARGIN_X, MARGIN_Y, MARGIN_Z = 0, 0, 0
DT = MAXIMUM_TIME / TIME_ARRAY_LENGTH

# Constant
C = 3e8

