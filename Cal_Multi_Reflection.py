"""
@version: python3.7
@author: ‘mengyuantan‘
@contact: tanmy1016@126.com
@time: 2019/12/31 17:05
"""

import numpy as np
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


if __name__ == '__main__':
    """
    This is a demo, Tx at (0, 0, 0), Hn array from 3 to 15 are 12
    """
    tmp = np.zeros(TIME_ARRAY_LENGTH)
    tmp[3:15] = 12
    demo = RefNode([0, 0, 0], tmp)

    """
    1st time reflection
    """
    adding = get_response(demo)
    for i in range(len(WALL_NODE)):
        WALL_NODE[i].hn_array += adding[i]
        # print(WALL_NODE[i].hn_array)

    """
    n time(s) reflection
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
    for i in range(len(WALL_NODE)):
        print(WALL_NODE[i].hn_array)
