"""
@version: python3.7
@author: ‘mengyuantan‘
@contact: tanmy1016@126.com
@time: 2019/12/31 17:05
"""

import matplotlib.pyplot as plt
import datetime
from RefNode import RefNode
from RefCase import RefCase
from Helper import *
from NodeUtil import *


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
    if (case == RefCase.T_TO_R and is_in_FOV(from_node, to_node)) or \
            case == RefCase.T_TO_W or \
            (case == RefCase.W_TO_W and not is_in_same_wall(from_node, to_node)) or \
            (case == RefCase.W_TO_R and is_in_FOV(from_node, to_node)):
        delay, cur_hn = get_delay_and_hn_by_case(a_node=from_node, b_node=to_node, case=case)
        hn_array = cur_hn * from_node.hn_array
        hn_array = np.insert(hn_array, 0, np.zeros(int(delay // DT)))[:TIME_ARRAY_LENGTH]
        return hn_array
    else:
        return np.zeros(TIME_ARRAY_LENGTH)


def plotting_array_by_node(node: RefNode, color: str, normalization=False, limit_y=False):
    # hn_array = node.hn_array / np.max(node.hn_array) if normalization else node.hn_array
    hn_array = node.hn_array / hn_max if normalization else node.hn_array
    plt.plot(hn_array, color)
    if limit_y:
        plt.ylim(-0.05, 1.05)
    plt.show()


if __name__ == '__main__':
    WALL_NODE = init_wall_node()

    unit_impulse = np.zeros(TIME_ARRAY_LENGTH)
    unit_impulse[0] = 1

    Tx_position = [[1.25, 1.25, ROOM_Z_LEN],
                   [1.25, 3.75, ROOM_Z_LEN],
                   [3.75, 1.25, ROOM_Z_LEN],
                   [3.75, 3.75, ROOM_Z_LEN]]

    # 4 LED array
    # Tx_list = []
    # for pos in Tx_position:
    #     for i in np.linspace(pos[0] - 0.3, pos[0] + 0.3, 60):
    #         for j in np.linspace(pos[1] - 0.3, pos[1] + 0.3, 60):
    #             Tx_list.append(RefNode([i, j, ROOM_Z_LEN], unit_impulse))

    # Single LED array (most possible)
    # Tx_list = []
    # pos = Tx_position[0]
    # for i in np.linspace(pos[0] - 0.3, pos[0] + 0.3, 60):
    #     for j in np.linspace(pos[1] - 0.3, pos[1] + 0.3, 60):
    #         Tx_list.append(RefNode([i, j, ROOM_Z_LEN], unit_impulse))

    # 4-lamps
    Tx_list = []
    for pos in Tx_position:
        Tx_list.append(RefNode(pos, unit_impulse))

    # Single lamp
    # Tx_list = [RefNode(Tx_position[0], unit_impulse)]

    Rx_position = [0.01, 0.01, RX_HEIGHT]
    Rx_device = RefNode(Rx_position, np.zeros(TIME_ARRAY_LENGTH))
    Rx_device_directed_part = RefNode(Rx_position, np.zeros(TIME_ARRAY_LENGTH))
    Rx_device_reflection_part = RefNode(Rx_position, np.zeros(TIME_ARRAY_LENGTH))

    """
    Directed part. (Tx --> Rx)
    """
    start_time = datetime.datetime.now()

    for cur_node in Tx_list:
        Rx_device.hn_array += \
            get_response_by_case(from_node=cur_node, to_node=Rx_device, case=RefCase.T_TO_R)
        Rx_device_directed_part.hn_array += \
            get_response_by_case(from_node=cur_node, to_node=Rx_device, case=RefCase.T_TO_R)

    end_time = datetime.datetime.now()
    print("At directed light, program running %.3f seconds"
          % ((end_time - start_time).total_seconds()))

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
            WALL_NODE[i].hn_array += wall_node_hn_adding[i]

        end_time = datetime.datetime.now()
        print("At 1st time reflection, program running %.3f seconds"
              % ((end_time - start_time).total_seconds()))

        for times in range(1, REFLECT_TIMES):
            """
            n time(s) reflection. (Wall --> Wall)
            """
            start_time = datetime.datetime.now()

            wall_node_hn_adding = np.zeros(shape=(len(WALL_NODE), TIME_ARRAY_LENGTH))
            for i in range(len(WALL_NODE)):
                for j in range(len(WALL_NODE)):
                    wall_node_hn_adding[j] += \
                        get_response_by_case(from_node=WALL_NODE[i], to_node=WALL_NODE[j],
                                             case=RefCase.W_TO_W)
            for i in range(len(WALL_NODE)):
                WALL_NODE[i].hn_array += wall_node_hn_adding[i]

            end_time = datetime.datetime.now()
            print("At %dth times reflection, program running %.3f seconds"
                  % ((times + 1), ((end_time - start_time).total_seconds())))

        """
        get response from all WALL_NODE. (Wall --> Rx)
        """
        for i in range(len(WALL_NODE)):
            Rx_device.hn_array += get_response_by_case(
                from_node=WALL_NODE[i], to_node=Rx_device, case=RefCase.W_TO_R)
            Rx_device_reflection_part.hn_array += get_response_by_case(
                from_node=WALL_NODE[i], to_node=Rx_device, case=RefCase.W_TO_R)

    hn_max = np.max(Rx_device.hn_array)
    dir_part = np.sum(Rx_device_directed_part.hn_array)
    ref_part = np.sum(Rx_device_reflection_part.hn_array)
    print("{:.2f} %".format(100 * ref_part / dir_part))

    plotting_array_by_node(node=Rx_device_directed_part, color="r",
                           normalization=True, limit_y=True)
    plotting_array_by_node(node=Rx_device_reflection_part, color="b",
                           normalization=True, limit_y=True)
