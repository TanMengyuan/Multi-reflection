"""
@version: python3.7
@author: ‘mengyuantan‘
@contact: tanmy1016@126.com
@time: 2019/12/31 16:51
"""

from Helper import *
from RefCase import RefCase


def g(tetha):
    return np.square(NN) / np.square(np.sin(FOV)) if 0 <= tetha < FOV else 0


class RefNode:
    def __init__(self, pos, cur_hn):
        self.x, self.y, self.z = pos[0], pos[1], pos[2]
        self.position = [self.x, self.y, self.z]
        self.hn_array = cur_hn

    def get_info(self, to_node):
        distance = np.sqrt(np.square(self.x - to_node.x) +
                           np.square(self.y - to_node.y) +
                           np.square(self.z - to_node.z))
        height = self.z - to_node.z
        tetha_irr = np.arccos(height / distance)
        return distance, height, tetha_irr

    def get_delay_and_hn_by_case(self, to_node, case):
        delay, hn = 0, 0
        distance, height, tetha_irr = self.get_info(to_node)

        tetha_irr = (np.pi / 2 - tetha_irr) % (np.pi / 2) \
            if case == RefCase.T_TO_W or case == RefCase.W_TO_W else tetha_irr
        tetha_irr_comp = np.pi / 2 - tetha_irr

        if case == RefCase.T_TO_R:
            hn = (((MM + 1) * A_PD) / (2 * np.pi * np.square(distance))) * \
                 np.cos(tetha_irr) ** MM * g(tetha_irr) * np.cos(tetha_irr)
        elif case == RefCase.T_TO_W:
            hn = np.cos(tetha_irr) * np.cos(tetha_irr_comp) ** MM / \
                 (np.pi * np.square(distance))
        elif case == RefCase.W_TO_W:
            hn = RHO * np.cos(tetha_irr) * np.cos(tetha_irr_comp) / \
                 (np.pi * np.square(distance))
        elif case == RefCase.W_TO_R:
            hn = D_WALL_X * RHO * (((MM + 1) * A_PD) / (2 * np.pi * np.square(distance))) * \
                 np.cos(tetha_irr_comp) * g(tetha_irr) * np.cos(tetha_irr)
        delay = distance / C
        return delay, hn

    def is_in_same_wall(self, to_node):
        return (self.x == to_node.x and self.x in [0, ROOM_X_LEN]) or \
               (self.y == to_node.y and self.y in [0, ROOM_Y_LEN])

    def is_in_FOV(self, to_node):
        distance, height, tetha_irr = self.get_info(to_node)
        return height > 0 and tetha_irr <= FOV
