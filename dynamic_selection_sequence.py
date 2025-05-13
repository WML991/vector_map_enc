import numpy as np
from math import floor

#
def dynamic_selection(X, Y, Z, W ,x_coords, y_coords):

    Qx = floor(np.mod((x_coords.max() - x_coords.min()), 4))
    Qy = floor(np.mod(y_coords.mean(), 4))

    if Qy == Qx:
        Qy = np.mod(Qy + 1, 4)

    # 创建序列映射字典
    index_map = {0: X, 1: Y, 2: Z, 3: W}

    # 根据 Qx 和 Qy 选择置乱序列
    Q1 = index_map[Qx]
    Q2 = index_map[Qy]

    # 获取剩余的两个序列
    remaining_indices = {0, 1, 2, 3} - {Qx, Qy}
    Q3 = index_map[remaining_indices.pop()]
    Q4 = index_map[remaining_indices.pop()]

    return Q1, Q2, Q3, Q4
