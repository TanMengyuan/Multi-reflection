"""
@version: python3.7
@author: ‘mengyuantan‘
@contact: tanmy1016@126.com
@time: 2019/12/31 16:51
"""

import numpy as np
from Helper import ROOM_X_LEN, ROOM_Y_LEN, ROOM_Z_LEN


class RefNode:
    def __init__(self, pos, cur_hn):
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.hn_array = cur_hn

    def get_distance_and_hn(self, b_node):
        distance = np.sqrt(np.square(self.x - b_node.x) + np.square(self.y - b_node.y) + np.square(self.z - b_node.z))
        # todo: finish the formula to calculate the hn by a_node and b_node
        hn = distance ** 0.1
        return distance, hn

    def is_in_same_wall(self, b_node):
        return (self.x == b_node.x and self.x in [0, ROOM_X_LEN]) or \
               (self.y == b_node.y and self.y in [0, ROOM_Y_LEN])
