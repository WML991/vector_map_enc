# import math
#
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D  # 导入3D绘图库
#
# # 定义四维混沌系统的微分方程
# def chaos_system(x, y, z, w, a, b, c, d, e):
#
#     dx = a * (y - x)
#     dy = b * x - y + e * w - x * z
#     dz = x * y + x ** 2 - c * z
#     dw = -d * y
#     return dx, dy, dz, dw
#
#
# def solve_chaos_system(a, b, c, d, e, u_x, u_y, u_z, u_w,V, t_max=100, dt=0.001):
#
#     t_steps = 1000 * math.floor(np.log2(V + 1)) + V
#     t = np.linspace(0, t_max, t_steps)  # 生成时间序列
#
#     # 初始化存储混沌序列的数组
#     x_vals = np.zeros(t_steps)
#     y_vals = np.zeros(t_steps)
#     z_vals = np.zeros(t_steps)
#     w_vals = np.zeros(t_steps)
#
#     # 设置初始条件
#     x_vals[0] = u_x
#     y_vals[0] = u_y
#     z_vals[0] = u_z
#     w_vals[0] = u_w
#
#     # 四阶龙格-库塔法数值求解
#     for i in range(1, t_steps):
#         x, y, z, w = x_vals[i - 1], y_vals[i - 1], z_vals[i - 1], w_vals[i - 1]
#
#         dx1, dy1, dz1, dw1 = chaos_system(x, y, z, w, a, b, c, d, e)
#
#         dx2, dy2, dz2, dw2 = chaos_system(
#             x + dx1 * dt / 2, y + dy1 * dt / 2, z + dz1 * dt / 2, w + dw1 * dt / 2, a, b, c, d, e
#         )
#         dx3, dy3, dz3, dw3 = chaos_system(
#             x + dx2 * dt / 2, y + dy2 * dt / 2, z + dz2 * dt / 2, w + dw2 * dt / 2, a, b, c, d, e
#         )
#
#         dx4, dy4, dz4, dw4 = chaos_system(
#             x + dx3 * dt, y + dy3 * dt, z + dz3 * dt, w + dw3 * dt, a, b, c, d, e
#         )
#
#         # 更新状态
#         x_vals[i] = x + (dx1 + 2 * dx2 + 2 * dx3 + dx4) * dt / 6
#         y_vals[i] = y + (dy1 + 2 * dy2 + 2 * dy3 + dy4) * dt / 6
#         z_vals[i] = z + (dz1 + 2 * dz2 + 2 * dz3 + dz4) * dt / 6
#         w_vals[i] = w + (dw1 + 2 * dw2 + 2 * dw3 + dw4) * dt / 6
#
#     return t, x_vals, y_vals, z_vals, w_vals
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
