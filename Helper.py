"""
@version: python3.7
@author: ‘mengyuantan‘
@contact: tanmy1016@126.com
@time: 2019/12/31 17:04
"""

import json
import numpy as np
from RefNode import RefNode

CONFIG_FILE = './config.json'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    config = json.load(f)
    TIME_ARRAY_LENGTH = config["TIME_ARRAY_LENGTH"]
    MAXIMUM_TIME = config["MAXIMUM_TIME"]
    C = config["C"]
    REFLECT_TIMES = config["REFLECT_TIMES"]


DT = MAXIMUM_TIME / TIME_ARRAY_LENGTH

# todo: finish the all wall node by using looping
WALL_NODE = [RefNode([0.1, 0, 0.1], np.zeros(TIME_ARRAY_LENGTH)),
             RefNode([0, 1.5, 1], np.zeros(TIME_ARRAY_LENGTH)),
             RefNode([0.75, 5, 1.25], np.zeros(TIME_ARRAY_LENGTH)),
             RefNode([5, 0.8, 2.15], np.zeros(TIME_ARRAY_LENGTH))]
