"""
@version: python3.7
@author: ‘mengyuantan‘
@contact: tanmy1016@126.com
@time: 2019/12/31 17:05
"""

import numpy as np
import matplotlib.pyplot as plt
import copy
from RefNode import RefNode
from Helper import TIME_ARRAY_LENGTH, C, DT, REFLECT_TIMES
from Helper import ROOM_X_LEN, ROOM_Y_LEN, ROOM_Z_LEN, RX_HEIGHT
from Helper import MARGIN_X, MARGIN_Y, MARGIN_Z, WALL_NODE_NUM_X, WALL_NODE_NUM_Y, WALL_NODE_NUM_Z


def create_wall_node():
    wall_node = []
    for x in [0, ROOM_X_LEN]:
        for y in np.linspace(MARGIN_X, ROOM_X_LEN - MARGIN_X, WALL_NODE_NUM_X):
            for z in np.linspace(MARGIN_Z, ROOM_Z_LEN - MARGIN_Z, WALL_NODE_NUM_Z):
                wall_node.append(RefNode([x, y, z], np.zeros(TIME_ARRAY_LENGTH)))
    for y in [0, ROOM_X_LEN]:
        for x in np.linspace(MARGIN_X, ROOM_X_LEN - MARGIN_X, WALL_NODE_NUM_X):
            for z in np.linspace(MARGIN_Z, ROOM_Z_LEN - MARGIN_Z, WALL_NODE_NUM_Z):
                wall_node.append(RefNode([x, y, z], np.zeros(TIME_ARRAY_LENGTH)))

    return wall_node


def get_response(node):
    hn_array = []
    ori_hn_array = copy.deepcopy(node.hn_array)
    for each in WALL_NODE:
        cur_hn_array = np.zeros(TIME_ARRAY_LENGTH)
        if not node.is_in_same_wall(each):
            delay, cur_hn = node.get_delay_and_hn(each)
            cur_hn_array = ori_hn_array
            cur_hn_array *= cur_hn
            cur_hn_array = np.insert(cur_hn_array, 0, [0 for _ in range(int(delay // DT))])[:TIME_ARRAY_LENGTH]
        hn_array.append(cur_hn_array)

    return hn_array


def receive_response(to_node):
    hn_array = np.zeros(TIME_ARRAY_LENGTH)
    for each in WALL_NODE:
        if to_node.is_in_FOV(each):
            delay, cur_hn = to_node.get_delay_and_hn(each)
            cur_hn_array = copy.deepcopy(each.hn_array)
            cur_hn_array *= cur_hn
            cur_hn_array = np.insert(cur_hn_array, 0, [0 for _ in range(int(delay // DT))])[:TIME_ARRAY_LENGTH]
            hn_array += cur_hn_array

    return hn_array


def plotting_array(node):
    # todo: complete the function of plotting
    plt.plot(node.hn_array)
    plt.show()


if __name__ == '__main__':
    WALL_NODE = create_wall_node()

    """
    This is a demo.
    """
    tmp = np.zeros(TIME_ARRAY_LENGTH)
    tmp[0:1] = 1
    Tx_demo = [RefNode([1, 1, ROOM_Z_LEN], tmp),
               RefNode([2, 2, ROOM_Z_LEN], tmp),
               RefNode([1, 2, ROOM_Z_LEN], tmp)]

    """
    1st time reflection. (Tx --> Wall)
    """
    adding = np.zeros(shape=(len(WALL_NODE), TIME_ARRAY_LENGTH))
    for cur_node in Tx_demo:
        adding += get_response(cur_node)
    for i in range(len(WALL_NODE)):
        WALL_NODE[i].hn_array += adding[i]
    # adding = get_response(demo)
    # for i in range(len(WALL_NODE)):
    #     WALL_NODE[i].hn_array += adding[i]

    """
    n time(s) reflection. (Wall --> Wall)
    """
    for times in range(REFLECT_TIMES):
        adding = np.zeros(shape=(len(WALL_NODE), TIME_ARRAY_LENGTH))
        for cur_node in WALL_NODE:
            adding += get_response(cur_node)
        for i in range(len(WALL_NODE)):
            WALL_NODE[i].hn_array += adding[i]

    """
    Check result
    """
    # for i in range(len(WALL_NODE)):
    #     plotting_array(WALL_NODE[i])

    """
    get response from all WALL_NODE. (Wall --> Rx)
    """
    Rx_demo = RefNode([1, 1, RX_HEIGHT], np.zeros(TIME_ARRAY_LENGTH))
    Rx_response = receive_response(Rx_demo)
    Rx_demo.hn_array = Rx_response
    plotting_array(Rx_demo)


