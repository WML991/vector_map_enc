import os

import numpy as np
import time

from FourD_chaos import calculate_chaos_initial_values, calculate_chaos_sequence
from coordinate_scrambling import extract_coordinates_from_shapefile, scramble_coordinates, unscramble_coordinates
from method.calculate_sm4key_and_iv import generate_key_and_iv_combined
from method.gmalg.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
from dynamic_selection_sequence import dynamic_selection

from SM4Encryptor import Encryptor

from test.final_test import effect_dispaly


if __name__ == '__main__':
    shapefile_path =  "../data/Si_Chuan/nature/gis_osm_natural_free_1.shp"
    file_size = os.path.getsize(shapefile_path) / 1024 
    user_key = "securekey"  
    sm4_key = b'\x00' * 16  
    iv = b'\x00' * 16  

    feature_count, vertex_count, x_coords, y_coords, data_indices = extract_coordinates_from_shapefile(shapefile_path)

    ux, uy, uz, uw = calculate_chaos_initial_values(file_size, vertex_count, feature_count, user_key)
    print(f"初始值: ux={ux}, uy={uy}, uz={uz}, uw={uw}")

    t, X, Y, Z, W = calculate_chaos_sequence(10+10**(-8), 28, 8.0 / 3.0, 1, 16, ux, uy, uz, uw, V=vertex_count)

    X = X[-vertex_count:]
    Y = Y[-vertex_count:]
    Z = Z[-vertex_count:]
    W = W[-vertex_count:]

 
    Q1, Q2, Q3, Q4 = dynamic_selection(X, Y, Z, W, x_coords, y_coords)

    x_coords_scrambled, y_coords_scrambled = scramble_coordinates(Q1, Q2, x_coords, y_coords, vertex_count)

    sm4_key, iv = generate_key_and_iv_combined(Q3, Q4)
    print("SM4 密钥:", sm4_key.hex())
    print("SM4 IV:", iv.hex())

    for i in range(len(x_coords)):
        x_coords_scrambled[i] = x_coords_scrambled[i]+180
        y_coords_scrambled[i] = y_coords_scrambled[i]+180

    encrypted_values_x = []
    encrypted_values_y = []

    sm4_Encryptor = Encryptor(sm4_key, iv)

    for x, y in zip(list(x_coords_scrambled), list(y_coords_scrambled)):
        encrypted_value_x = sm4_Encryptor.encrypt(x)
        encrypted_value_y = sm4_Encryptor.encrypt(y)
        encrypted_values_x.append(encrypted_value_x)
        encrypted_values_y.append(encrypted_value_y)

    decrypted_values_x = []
    decrypted_values_y = []

    for encrypted_value_x, encrypted_value_y in zip(encrypted_values_x, encrypted_values_y):
        decrypted_value_x = sm4_Encryptor.decrypt(encrypted_value_x)
        decrypted_value_y = sm4_Encryptor.decrypt(encrypted_value_y)
        decrypted_values_x.append(decrypted_value_x)
        decrypted_values_y.append(decrypted_value_y)

    effect_dispaly.display_decrypted_map(decrypted_values_x, decrypted_values_y, data_indices)

    Original_x_coords, Original_y_coords = unscramble_coordinates(Q1, Q2, decrypted_values_x, decrypted_values_y, vertex_count)

    for i in range(len(Original_x_coords)):
        Original_x_coords[i] = Original_x_coords[i]-180
        Original_y_coords[i] = Original_y_coords[i]-180
