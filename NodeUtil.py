"""
@version: python3.7
@author: ‘mengyuantan‘
@contact: tanmy1016@126.com
@time: 2020/4/18 15:18
"""
from Helper import *
from RefNode import RefNode
from RefCase import RefCase


def g(tetha):
    return np.square(NN) / np.square(np.sin(FOV)) if 0 <= tetha < FOV else 0


def get_info(a_node: RefNode, b_node: RefNode):
    distance = np.sqrt(np.square(a_node.x - b_node.x) +
                       np.square(a_node.y - b_node.y) +
                       np.square(a_node.z - b_node.z))
    height = a_node.z - b_node.z
    tetha_irr = np.arccos(height / distance)
    return distance, height, tetha_irr


def get_delay_and_hn_by_case(a_node: RefNode, b_node: RefNode, case: RefCase):
    delay, hn = 0, 0
    # tetha_irr的结果是与吹直方向的夹角
    distance, height, tetha_irr = get_info(a_node=a_node, b_node=b_node)

    if height < 0:
        tetha_irr = np.pi - tetha_irr
    if case == RefCase.T_TO_W or case == RefCase.W_TO_W:
        tetha_irr = np.pi / 2 - tetha_irr
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


def is_in_same_wall(a_node: RefNode, b_node: RefNode):
    return (a_node.x == b_node.x and a_node.x in [0, ROOM_X_LEN]) or \
           (a_node.y == b_node.y and a_node.y in [0, ROOM_Y_LEN])


def is_in_FOV(a_node: RefNode, b_node: RefNode):
    distance, height, tetha_irr = get_info(a_node=a_node, b_node=b_node)
    return height > 0 and tetha_irr <= FOV
