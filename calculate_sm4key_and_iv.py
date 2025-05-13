import numpy as np

from method.FourD_chaos import calculate_chaos_initial_values, calculate_chaos_sequence
from method.coordinate_scrambling import extract_coordinates_from_shapefile


def generate_key_and_iv_combined(Z, W):
    """
    根据混沌序列 Z 和 W 生成 SM4 的加密密钥和 IV（结合两个序列计算）。
    Args:
        Z (np.ndarray): 混沌序列 Z。
        W (np.ndarray): 混沌序列 W。
    Returns:
        tuple: (密钥, IV)，均为 16 字节的字节流。
    """
    vertex_count = len(Z)

    step = vertex_count // 16  # 计算步长，均匀采样
    key = []
    iv = []

    # 生成SM4密钥
    for i in range(16):
        key_value = int(
            sum(
                (Z[j] * W[vertex_count - j - 1]) * (j + 1) * 256
                for j in range(i, vertex_count, step)
            ) % 256
        )
        key.append(key_value)

    # 生成 IV
    for i in range(16):
        iv_value = int(
            sum(
                (Z[j] + W[vertex_count - j - 1]) * (vertex_count - j) * 256
                for j in range(i, vertex_count, step)
            ) % 256
        )
        iv.append(iv_value)

    # 转换为字节流
    key_bytes = bytes(key)
    iv_bytes = bytes(iv)

    return key_bytes, iv_bytes

if __name__ == '__main__':
    shapefile_path = "../data/Si_Chuan/railways/gis_osm_railways_free_1.shp"
    file_size = 1024  # 文件大小
    key = "securekey"  # 密钥

    # 调用函数，读取 Shapefile 数据并获取顶点数和特征数，以及X,Y的坐标序列
    feature_count, vertex_count, x_coords, y_coords, data_indices = extract_coordinates_from_shapefile(shapefile_path)
    print("x_coords:", x_coords[:10])
    print("y_coords:", y_coords[:10])

    # 计算混沌序列的初始值
    ux, uy, uz, uw = calculate_chaos_initial_values(file_size, vertex_count, feature_count, key)
    print(f"初始值: ux={ux}, uy={uy}, uz={uz}, uw={uw}")

    # 解混沌系统方程，获取混沌序列
    t, X, Y, Z, W = calculate_chaos_sequence(10, 28, 8.0 / 3.0, 1, 16, ux, uy, uz, uw, V=vertex_count)

    # 截取后vertext_count的长度, 保证混沌序列和坐标序列长度一致
    X = X[-vertex_count:]
    Y = Y[-vertex_count:]
    Z = Z[-vertex_count:]
    W = W[-vertex_count:]

    # 生成密钥和 IV
    sm4_key, sm4_iv = generate_key_and_iv_combined(Z, W)

    print("SM4 密钥:", sm4_key)
    print("SM4 IV:", sm4_iv)
