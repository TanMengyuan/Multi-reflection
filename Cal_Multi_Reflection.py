"""
@version: python3.7
@author: ‘mengyuantan‘
@contact: tanmy1016@126.com
@time: 2019/12/31 17:05
"""

import numpy as np
import matplotlib.pyplot as plt
import copy
from enum import Enum
import datetime
from RefNode import RefNode
from Helper import *


class RefCase(Enum):
    T_TO_W = "T_TO_W"
    W_TO_W = "W_TO_W"
    W_TO_R = "W_TO_R"


def init_wall_node():
    wall_node = []
    for x in [0, ROOM_X_LEN]:
        for y in np.linspace(MARGIN_Y, ROOM_Y_LEN - MARGIN_Y, WALL_NODE_NUM_Y):
            for z in np.linspace(MARGIN_Z, ROOM_Z_LEN - MARGIN_Z, WALL_NODE_NUM_Z):
                wall_node.append(RefNode([x, y, z], np.zeros(TIME_ARRAY_LENGTH)))
    for y in [0, ROOM_Y_LEN]:
        for x in np.linspace(MARGIN_X, ROOM_X_LEN - MARGIN_X, WALL_NODE_NUM_X):
            for z in np.linspace(MARGIN_Z, ROOM_Z_LEN - MARGIN_Z, WALL_NODE_NUM_Z):
                wall_node.append(RefNode([x, y, z], np.zeros(TIME_ARRAY_LENGTH)))

    return wall_node


def get_response_by_case(node: RefNode, case: RefCase):
    # todo: case1: Tx --> Wall; case2: Wall --> Wall; case3: Wall --> Rx (Wall node is default.)
    if case == RefCase.T_TO_W:
        pass
    elif case == RefCase.W_TO_W:
        pass
    elif case == RefCase.W_TO_R:
        pass

    return


def get_response(node):
    hn_array = []
    for each in WALL_NODE:
        ori_hn_array = copy.deepcopy(node.hn_array)
        cur_hn_array = np.zeros(TIME_ARRAY_LENGTH)
        if not node.is_in_same_wall(each):
            delay, cur_hn = node.get_delay_and_hn(each)
            cur_hn_array = ori_hn_array
            cur_hn_array *= cur_hn
            cur_hn_array = np.insert(cur_hn_array, 0,
                                     np.zeros(int(delay // DT)))[:TIME_ARRAY_LENGTH]
        hn_array.append(cur_hn_array)

    return hn_array


# might not be use --> change to get_response_by_case
def receive_response(to_node):
    hn_array = np.zeros(TIME_ARRAY_LENGTH)
    for each in WALL_NODE:
        if to_node.is_in_FOV(each):
            delay, cur_hn = to_node.get_delay_and_hn(each)
            cur_hn_array = copy.deepcopy(each.hn_array)
            cur_hn_array *= cur_hn
            cur_hn_array = np.insert(cur_hn_array, 0,
                                     np.zeros(int(delay // DT)))[:TIME_ARRAY_LENGTH]
            hn_array += cur_hn_array

    return hn_array


def plotting_array(node):
    # todo: complete the function of plotting
    plt.plot(node.hn_array)
    plt.show()


if __name__ == '__main__':
    WALL_NODE = init_wall_node()

    """
    This is a demo.
    """
    tmp = np.zeros(TIME_ARRAY_LENGTH)
    tmp[0] = 1
    Tx_demo = [RefNode([1, 1, ROOM_Z_LEN], tmp),
               RefNode([2, 2, ROOM_Z_LEN], tmp),
               RefNode([1, 2, ROOM_Z_LEN], tmp)]

    """
    1st time reflection. (Tx --> Wall)
    """
    adding = np.zeros(shape=(len(WALL_NODE), TIME_ARRAY_LENGTH))
    start_time = datetime.datetime.now()
    for cur_node in Tx_demo:
        adding += get_response(cur_node)
    for i in range(len(WALL_NODE)):
        WALL_NODE[i].hn_array += adding[i]
    end_time = datetime.datetime.now()
    print("At first time reflection, program running %.2f seconds"
          % ((end_time - start_time).total_seconds()))

    """
    n time(s) reflection. (Wall --> Wall)
    """
    for times in range(REFLECT_TIMES):
        # At nth time
        start_time = datetime.datetime.now()
        adding = np.zeros(shape=(len(WALL_NODE), TIME_ARRAY_LENGTH))
        for cur_node in WALL_NODE:
            adding += get_response(cur_node)
        for i in range(len(WALL_NODE)):
            WALL_NODE[i].hn_array += adding[i]
        end_time = datetime.datetime.now()
        print("At %d time reflection, program running %.2f seconds"
              % ((times + 1), ((end_time - start_time).total_seconds())))

    """
    Check result
    """
    # for i in range(len(WALL_NODE)):
    #     plotting_array(WALL_NODE[i])

    """
    get response from all WALL_NODE. (Wall --> Rx)
    """
    Rx_demo = RefNode([0.1, 0.1, RX_HEIGHT], np.zeros(TIME_ARRAY_LENGTH))
    start_time = datetime.datetime.now()
    Rx_response = receive_response(Rx_demo)
    end_time = datetime.datetime.now()
    print("At last time reflection, program running %.2f seconds"
          % ((end_time - start_time).total_seconds()))
    Rx_demo.hn_array = Rx_response
    plotting_array(Rx_demo)
