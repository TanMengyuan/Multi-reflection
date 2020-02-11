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
    try:
        REFLECT_TIMES = int(config["REFLECT_TIMES"])
    except:
        raise ImportError("REFLECT_TIMES can't resolve, it should be INT.")
    ROOM_SIZE = config["ROOM_SIZE"]
    RX_HEIGHT = config["RX_HEIGHT"]
    FOV = np.deg2rad(config["FOV"])
    WALL_NODE_NUM = config["WALL_NODE_NUM"]
    REFLECTANCE = config["REFLECTANCE"]

# Resolve data
try:
    room_size = list(map(int, ROOM_SIZE.split("*")))
    ROOM_X_LEN, ROOM_Y_LEN, ROOM_Z_LEN = room_size[0], room_size[1], room_size[2]
except:
    raise ImportError("ROOM_SIZE can't resolve, it should be like 5*5*3.")
try:
    wall_node_num = list(map(int, WALL_NODE_NUM.split(",")))
    WALL_NODE_NUM_X, WALL_NODE_NUM_Y, WALL_NODE_NUM_Z = \
        wall_node_num[0], wall_node_num[1], wall_node_num[2]
except:
    raise ImportError("WALL_NODE_NUM can't resolve, it should be like 10,10,10")

MARGIN_X, MARGIN_Y, MARGIN_Z = (ROOM_X_LEN / WALL_NODE_NUM_X) / 2, \
                               (ROOM_Y_LEN / WALL_NODE_NUM_Y) / 2, \
                               (ROOM_Z_LEN / WALL_NODE_NUM_Z) / 2
DT = MAXIMUM_TIME / TIME_ARRAY_LENGTH

D_WALL_X = (ROOM_X_LEN * ROOM_Z_LEN) / (WALL_NODE_NUM_X * WALL_NODE_NUM_Z)
D_WALL_Y = (ROOM_Y_LEN * ROOM_Z_LEN) / (WALL_NODE_NUM_Y * WALL_NODE_NUM_Z)

# Constant
C = 3e8
RHO = 1 - REFLECTANCE
I0 = 0.73
A_PD = 1e-4
TETHA_HALF = np.deg2rad(60)
MM = np.int(- np.log(2) / np.log(np.cos(TETHA_HALF)))
TETHA_INC = np.deg2rad(45)
NN = 1.5

