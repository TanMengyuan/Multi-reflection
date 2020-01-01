"""
@version: python3.7
@author: ‘mengyuantan‘
@contact: tanmy1016@126.com
@time: 2019/12/31 16:51
"""

import numpy as np
from Helper import ROOM_X_LEN, ROOM_Y_LEN, ROOM_Z_LEN, FOV, C


class RefNode:
    def __init__(self, pos, cur_hn):
        self.x, self.y, self.z = pos[0], pos[1], pos[2]
        self.hn_array = cur_hn

    def get_delay_and_hn(self, b_node):
        distance = np.sqrt(np.square(self.x - b_node.x) +
                           np.square(self.y - b_node.y) +
                           np.square(self.z - b_node.z))
        # todo: finish the formula to calculate the hn by a_node and b_node
        # <-- This is just a sample -->
        hn = 1 / np.square(distance)
        delay = distance / C
        return delay, hn

    def is_in_same_wall(self, b_node):
        return (self.x == b_node.x and self.x in [0, ROOM_X_LEN]) or \
               (self.y == b_node.y and self.y in [0, ROOM_Y_LEN])

    def is_in_FOV(self, b_node):
        # todo: finish the calculate the FOV
        return True
