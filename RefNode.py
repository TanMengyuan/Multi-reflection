"""
@version: python3.7
@author: ‘mengyuantan‘
@contact: tanmy1016@126.com
@time: 2019/12/31 16:51
"""


class RefNode:
    def __init__(self, pos, cur_hn):
        self.x, self.y, self.z = pos[0], pos[1], pos[2]
        self.position = [self.x, self.y, self.z]
        self.hn_array = cur_hn
