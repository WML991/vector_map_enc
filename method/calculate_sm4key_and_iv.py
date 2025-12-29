import numpy as np

from method.FourD_chaos import calculate_chaos_initial_values, calculate_chaos_sequence
from method.coordinate_scrambling import extract_coordinates_from_shapefile


def generate_key_and_iv_combined(Z, W):
    vertex_count = len(Z)

    step = vertex_count // 16  
    key = []
    iv = []

    for i in range(16):
        key_value = int(
            sum(
                (Z[j] * W[vertex_count - j - 1]) * (j + 1) * 256
                for j in range(i, vertex_count, step)
            ) % 256
        )
        key.append(key_value)

    for i in range(16):
        iv_value = int(
            sum(
                (Z[j] + W[vertex_count - j - 1]) * (vertex_count - j) * 256
                for j in range(i, vertex_count, step)
            ) % 256
        )
        iv.append(iv_value)

    key_bytes = bytes(key)
    iv_bytes = bytes(iv)

    return key_bytes, iv_bytes
