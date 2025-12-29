import math
import time

import numpy as np
from method.gmalg.sm3 import sm3_hash

# 异或操作
def xor_strings(hex1, hex2):
    int1 = int(hex1, 16)    # 将16进制字符串转换为整数
    int2 = int(hex2, 16)
    return int1 ^ int2


# 定义四维混沌系统的微分方程
def chaos_system(x, y, z, w, a, b, c, d, e):
    """
    输入：当前状态 x, y, z, w 和参数 a, b, c, d, e
    输出：四个变量的导数 dx, dy, dz, dw
    """
    dx = a * (y - x)
    dy = b * x - y + e * w - x * z
    dz = x * y + x ** 2 - c * z
    dw = -d * y
    return dx, dy, dz, dw

def calculate_chaos_sequence(a, b, c, d, e, u_x, u_y, u_z, u_w, V, t_max=100, dt=0.001):
    """
    输入：四维混沌系统的参数 a, b, c, d, e 和初始条件 u_x, u_y, u_z, u_w
    输出：x, y, z, w 随时间变化的轨迹
    """

    t_steps = 1000 * math.floor(np.log2(V + 1)) + V     # 迭代次数为1000*floor[log2(V+1)]+V

    t = np.linspace(0, t_max, t_steps)  # 时间数组

    # 初始化存储混沌序列的数组
    x_vals = np.zeros(t_steps)
    y_vals = np.zeros(t_steps)
    z_vals = np.zeros(t_steps)
    w_vals = np.zeros(t_steps)

    # 设置初始条件
    x_vals[0] = u_x
    y_vals[0] = u_y
    z_vals[0] = u_z
    w_vals[0] = u_w

    # 使用二阶龙格-库塔法进行数值求解
    for i in range(1, t_steps):
        # 当前状态
        x, y, z, w = x_vals[i - 1], y_vals[i - 1], z_vals[i - 1], w_vals[i - 1]

        # 计算当前状态的导数（即系统的动态方程）
        dx1, dy1, dz1, dw1 = chaos_system(x, y, z, w, a, b, c, d, e)

        # 计算预测值（基于斜率预测）
        dx2, dy2, dz2, dw2 = chaos_system(x + dx1 * dt, y + dy1 * dt, z + dz1 * dt, w + dw1 * dt, a, b, c, d, e)

        # 使用加权平均的方式更新状态
        x_vals[i] = x + 0.5 * (dx1 + dx2) * dt
        y_vals[i] = y + 0.5 * (dy1 + dy2) * dt
        z_vals[i] = z + 0.5 * (dz1 + dz2) * dt
        w_vals[i] = w + 0.5 * (dw1 + dw2) * dt


    return t, x_vals, y_vals, z_vals, w_vals



def calculate_chaos_initial_values(file_size, vertex_count, feature_count, key, S_len=256):
    """计算混沌系统的初始值"""

    C = vertex_count % 100 + 1

    file_size_hash = sm3_hash(str(file_size))
    vertex_count_hash = sm3_hash(str(vertex_count))
    S = xor_strings(file_size_hash, vertex_count_hash)
    S_bin = bin(S)[2:].zfill(256)  # 转换为256位二进制

    s_list = [S_bin[i:i + 8] for i in range(0, 256, 8)]  # 每8位分为一组

    U_prev = S_bin  # 初始值是 S 的二进制表示
    U_list = []

    for i in range(32):
        input_data = s_list[31 - i] + key + U_prev  # 根据公式：s32||key||U_{i-1}
        U_prev = sm3_hash(input_data)
        U_list.append(U_prev)

    U32 = U_list[-1]  # 取最后一个 U 值
    e_list = [int(U32[i:i + 8], 16) for i in range(0, 64, 8)]  # 每8位转换为十六进制整数
    e1, e2, e3, e4, e5, e6, e7, e8 = e_list[:8]

    V = vertex_count
    F = feature_count

    def compute_initial_value(e_vals, mod_vals, c, V, F, S_len):
        numerator = (e_vals[0] ^ e_vals[1] ^ e_vals[2] ^ e_vals[3]) + (mod_vals[0] * mod_vals[1]) % S_len
        scaled_value = (c / (V * F)) * numerator
        return scaled_value - int(scaled_value)

    ux = compute_initial_value([e1, e3, e5, e7], [e2, e4], C, V, F, S_len)
    uy = compute_initial_value([e2, e4, e6, e8], [e3, e5], C, V, F, S_len)
    uz = compute_initial_value([e3, e5, e7, e1], [e4, e6], C, V, F, S_len)
    uw = compute_initial_value([e4, e6, e8, e2], [e1, e7], C, V, F, S_len)

    return ux, uy, uz, uw

def calculate_index2(Q):
    Q = np.array(Q)
    N = len(Q)
    scaled_arr = []
    for num in Q:
        # 获取小数部分
        decimal_part = str(num).split('.')[-1] if '.' in str(num) else ''
        # 计算小数位数
        decimal_places = len(decimal_part)
        # 放大 num * 10^(小数位数)
        scaled_num = num * (10 ** decimal_places)
        scaled_arr.append(scaled_num)
    indices_Q = np.mod(scaled_arr, N)
    indices_Q = indices_Q.astype(int)
    return indices_Q



