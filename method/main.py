import os

# import numpy as np
import time

from FourD_chaos import calculate_chaos_initial_values, calculate_chaos_sequence
from coordinate_scrambling import extract_coordinates_from_shapefile, scramble_coordinates, unscramble_coordinates
from method.calculate_sm4key_and_iv import generate_key_and_iv_combined
from method.gmalg.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
from  dynamic_selection_sequence import dynamic_selection

from SM4Encryptor import Encryptor

from test.final_test import effect_dispaly


if __name__ == '__main__':
    shapefile_path =  "../data/Si_Chuan/nature/gis_osm_natural_free_1.shp"
    # shapefile_path = "../data/Si_Chuan/buildings/gis_osm_buildings_a_free_1.shp"
    # shapefile_path = "../data/Si_Chuan/railways/gis_osm_railways_free_1.shp"
    file_size = os.path.getsize(shapefile_path) / 1024 # 文件大小
    # print(f"{file_size}KB")
    user_key = "securekey"  # 密钥
    sm4_key = b'\x00' * 16  # 16 字节密钥（全零初始化）
    iv = b'\x00' * 16  # 16 字节 IV（全零初始化）

    # 调用函数，读取 Shapefile 数据并获取顶点数和特征数，以及X,Y的坐标序列
    feature_count, vertex_count, x_coords, y_coords, data_indices = extract_coordinates_from_shapefile(shapefile_path)

    effect_dispaly.display_original_map(x_coords, y_coords, data_indices)

    # 计算混沌序列的初始值
    ux, uy, uz, uw = calculate_chaos_initial_values(file_size, vertex_count, feature_count, user_key)
    print(f"初始值: ux={ux}, uy={uy}, uz={uz}, uw={uw}")

    # 解混沌系统方程，获取混沌序列
    t, X, Y, Z, W = calculate_chaos_sequence(10, 28, 8.0 / 3.0, 1, 16, ux, uy, uz, uw, V=vertex_count)

    # 截取后vertext_count的长度, 保证混沌序列和坐标序列长度一致
    X = X[-vertex_count:]
    Y = Y[-vertex_count:]
    Z = Z[-vertex_count:]
    W = W[-vertex_count:]

    # 动态选择混沌序列进行置乱
    # 动态的选择混沌序列，两个用于置乱，两个用于加密中的计算
    Q1, Q2, Q3, Q4 = dynamic_selection(X, Y, Z, W, x_coords, y_coords)

    time_start = time.time()

    # 置乱坐标
    x_coords_scrambled, y_coords_scrambled = scramble_coordinates(Q1, Q2, x_coords, y_coords, vertex_count)

    # 置乱后的矢量图
    effect_dispaly.display_scrambled_map(x_coords_scrambled, y_coords_scrambled, data_indices)


    # 生成密钥和 IV
    sm4_key, iv = generate_key_and_iv_combined(Q3, Q4)
    print("SM4 密钥:", sm4_key.hex())
    print("SM4 IV:", iv.hex())


    # 执行SM4加密
    encrypted_values_x = []
    encrypted_values_y = []

    # 创建SM4加密器
    sm4_Encryptor = Encryptor(sm4_key, iv)

    for x, y in zip(list(x_coords_scrambled), list(y_coords_scrambled)):
        # 加密
        encrypted_value_x = sm4_Encryptor.encrypt(x)
        encrypted_value_y = sm4_Encryptor.encrypt(y)
        encrypted_values_x.append(encrypted_value_x)
        encrypted_values_y.append(encrypted_value_y)

    time_end = time.time()
    print('加密时间:', time_end - time_start)

    # 加密后的矢量图
    effect_dispaly.display_encrypted_map(encrypted_values_x, encrypted_values_y, data_indices)

    # 执行SM4解密
    decrypted_values_x = []
    decrypted_values_y = []

    # 创建SM4解密器

    for encrypted_value_x, encrypted_value_y in zip(encrypted_values_x, encrypted_values_y):
        # 解密
        decrypted_value_x = sm4_Encryptor.decrypt(encrypted_value_x)
        decrypted_value_y = sm4_Encryptor.decrypt(encrypted_value_y)
        decrypted_values_x.append(decrypted_value_x)
        decrypted_values_y.append(decrypted_value_y)

    # 解密后的矢量图
    effect_dispaly.display_decrypted_map(decrypted_values_x, decrypted_values_y, data_indices)

    # 解置乱，恢复原始坐标
    Original_x_coords, Original_y_coords = unscramble_coordinates(Q1, Q2, decrypted_values_x, decrypted_values_y, vertex_count)

    # 解置乱后的矢量图
    effect_dispaly.display_unscrambled_map(Original_x_coords, Original_y_coords, data_indices)





    # # 绘制图像
    # # 原始矢量图
    # effect_dispaly.display_original_effect(x_coords, y_coords)
    #
    # # 置乱后的矢量图
    # effect_dispaly.display_scrambled_effect(x_coords_scrambled, y_coords_scrambled)
    #
    # # 加密后的矢量图
    # effect_dispaly.display_encrypted_effect(encrypted_values_x, encrypted_values_y)
    #
    # # 解密后的矢量图
    # effect_dispaly.display_decrypted_effect(decrypted_values_x, decrypted_values_y)
    #
    # # 解置乱后的矢量图
    # effect_dispaly.display_unscrambled_effect(Original_x_coords, Original_y_coords)







    # 打印原始的 x 和 y
    # print("X Coordinates:", x_coords)
    # print("Y Coordinates:", y_coords)
    # # 打印解密后的 x 和 y
    # print("X Coordinates befor decryption:", list(x_coords))
    #
    # print("X Coordinates after decryption:", decrypted_values_x)
    #
    # print("Y Coordinates befor decryption:", list(y_coords))
    # print("Y Coordinates after decryption:", decrypted_values_y)
    #
    # print(len(decrypted_values_x))
    # print(len(decrypted_values_y))




