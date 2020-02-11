"""
@version: python3.7
@author: ‘mengyuantan‘
@contact: tanmy1016@126.com
@time: 2019/12/31 17:05
"""

import numpy as np
import matplotlib.pyplot as plt
import datetime
from RefNode import RefNode
from RefCase import RefCase
from Helper import *


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


def get_response_by_case(from_node: RefNode, to_node: RefNode, case: RefCase):
    if (case == RefCase.T_TO_R and from_node.is_in_FOV(to_node)) or \
            case == RefCase.T_TO_W or \
            (case == RefCase.W_TO_W and not from_node.is_in_same_wall(to_node)) or \
            (case == RefCase.W_TO_R and from_node.is_in_FOV(to_node)):
        delay, cur_hn = from_node.get_delay_and_hn_by_case(to_node=to_node, case=case)
        hn_array = cur_hn * from_node.hn_array
        hn_array = np.insert(hn_array, 0, np.zeros(int(delay // DT)))[:TIME_ARRAY_LENGTH]
        return hn_array
    else:
        return np.zeros(TIME_ARRAY_LENGTH)


def plotting_array_by_node(node: RefNode, normalization: bool):
    # todo: complete the function of plotting
    hn_array = node.hn_array / np.max(node.hn_array) if normalization else node.hn_array
    plt.plot(hn_array)
    plt.show()


if __name__ == '__main__':
    WALL_NODE = init_wall_node()

    unit_impulse = np.zeros(TIME_ARRAY_LENGTH)
    unit_impulse[0] = 1

    # Tx_list = []
    # for i in np.linspace(0.95, 1.55, 60):
    #     for j in np.linspace(0.95, 1.55, 60):
    #         Tx_list.append(RefNode([i, j, ROOM_Z_LEN], unit_impulse))

    Tx_list = [RefNode([1.25, 1.25, ROOM_Z_LEN], unit_impulse),
               RefNode([1.25, 3.75, ROOM_Z_LEN], unit_impulse),
               RefNode([3.75, 1.25, ROOM_Z_LEN], unit_impulse),
               RefNode([3.75, 3.75, ROOM_Z_LEN], unit_impulse)]
    Rx_device = RefNode([0.1, 0.1, RX_HEIGHT], np.zeros(TIME_ARRAY_LENGTH))

    """
    Directed part. (Tx --> Rx)
    """
    # start_time = datetime.datetime.now()
    # for cur_node in Tx_list:
    #     Rx_device.hn_array += \
    #         get_response_by_case(from_node=cur_node, to_node=Rx_device, case=RefCase.T_TO_R)
    # end_time = datetime.datetime.now()
    # print("At directed light, program running %.3f seconds"
    #       % ((end_time - start_time).total_seconds()))

    """
    Reflection part
    """
    if REFLECT_TIMES > 0:
        """
        1st time reflection. (Tx --> Wall)
        """
        start_time = datetime.datetime.now()
        wall_node_hn_adding = np.zeros(shape=(len(WALL_NODE), TIME_ARRAY_LENGTH))
        for cur_node in Tx_list:
            for i in range(len(WALL_NODE)):
                wall_node_hn_adding[i] += \
                    get_response_by_case(from_node=cur_node, to_node=WALL_NODE[i],
                                         case=RefCase.T_TO_W)
        for i in range(len(WALL_NODE)):
            WALL_NODE[i].hn_array += RHO * wall_node_hn_adding[i]
        end_time = datetime.datetime.now()
        print("At first time reflection, program running %.3f seconds"
              % ((end_time - start_time).total_seconds()))

        """
        n time(s) reflection. (Wall --> Wall)
        """
        for times in range(REFLECT_TIMES - 1):
            start_time = datetime.datetime.now()
            wall_node_hn_adding = np.zeros(shape=(len(WALL_NODE), TIME_ARRAY_LENGTH))
            for i in range(len(WALL_NODE)):
                for j in range(len(WALL_NODE)):
                    wall_node_hn_adding[j] += \
                        get_response_by_case(from_node=WALL_NODE[i], to_node=WALL_NODE[j],
                                             case=RefCase.W_TO_W)
            for i in range(len(WALL_NODE)):
                WALL_NODE[i].hn_array += RHO * wall_node_hn_adding[i]
            end_time = datetime.datetime.now()
            print("At %d time(s) reflection, program running %.3f seconds"
                  % ((times + 1), ((end_time - start_time).total_seconds())))

        """
        get response from all WALL_NODE. (Wall --> Rx)
        """
        start_time = datetime.datetime.now()
        for i in range(len(WALL_NODE)):
            Rx_device.hn_array += D_WALL_X * get_response_by_case(
                from_node=WALL_NODE[i], to_node=Rx_device, case=RefCase.W_TO_R)
        end_time = datetime.datetime.now()
        print("At last time receive, program running %.3f seconds"
              % ((end_time - start_time).total_seconds()))

    plotting_array_by_node(node=Rx_device, normalization=True)
