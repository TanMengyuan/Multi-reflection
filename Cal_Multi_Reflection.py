"""
@version: python3.7
@author: ‘mengyuantan‘
@contact: tanmy1016@126.com
@time: 2019/12/31 17:05
"""

import numpy as np
import matplotlib.pyplot as plt
import copy
from Ref_Node import RefNode
from Helper import TIME_ARRAY_LENGTH, WALL_NODE, C, DT, REFLECT_TIMES


def get_response(node):
    hn_array = []
    ori_hn_array = copy.deepcopy(node.hn_array)
    for each in WALL_NODE:
        d, cur_hn = node.get_distance_and_hn(each)
        delay = d / C
        cur_hn_array = ori_hn_array
        cur_hn_array *= cur_hn
        cur_hn_array = np.insert(cur_hn_array, 0, [0 for _ in range(int(delay // DT))])[:TIME_ARRAY_LENGTH]
        hn_array.append(cur_hn_array)

    return hn_array


def plotting_array(array):
    # todo: complete the function of plotting
    plt.plot(array)
    plt.show()


if __name__ == '__main__':
    """
    This is a demo, Tx at (0, 0, 0).
    """
    tmp = np.zeros(TIME_ARRAY_LENGTH)
    tmp[0:1] = 1
    demo = RefNode([0, 0, 0], tmp)

    """
    1st time reflection. (Tx --> Wall)
    """
    adding = get_response(demo)
    for i in range(len(WALL_NODE)):
        WALL_NODE[i].hn_array += adding[i]
        # print(WALL_NODE[i].hn_array)

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
    get response from all WALL_NODE. (Wall --> Rx)
    """
    # todo: calculate the Hn_array on the Rx by get from all WALL_NODE

    """
    Check result
    """
    for i in range(len(WALL_NODE)):
        plotting_array(WALL_NODE[i].hn_array)
