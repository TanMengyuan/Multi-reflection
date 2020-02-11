"""
@version: python3.7
@author: ‘mengyuantan‘
@contact: tanmy1016@126.com
@time: 2020/2/11 16:27
"""

from enum import Enum


class RefCase(Enum):
    T_TO_R = "T_TO_R"
    T_TO_W = "T_TO_W"
    W_TO_W = "W_TO_W"
    W_TO_R = "W_TO_R"
