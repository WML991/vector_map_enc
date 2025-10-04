import numpy as np
import geopandas as gpd
from method.FourD_chaos import calculate_index2


def extract_coordinates_from_shapefile(shapefile_path):

    gdf = gpd.read_file(shapefile_path)

    # 打印文件的基本信息
    print("文件的总特征数 (记录数):", len(gdf))
    print("文件的坐标系统:", gdf.crs)

    # 初始化坐标列表
    x_coords = []
    y_coords = []

    data_indices = []

    # 当前坐标序列的长度（起始索引）
    current_index = 0

    # 遍历每个特征（每个形状）
    for _, row in gdf.iterrows():
        geometry = row['geometry']

        # 如果几何是 Point（点），直接获取 x, y
        if geometry.geom_type == 'Point':
            x_coords.append(geometry.x)
            y_coords.append(geometry.y)

        # 如果几何是 MultiPoint（多点）或其他复杂形状，迭代获取所有坐标
        elif geometry.geom_type == 'MultiPoint':
            for point in geometry:
                x_coords.append(point.x)
                y_coords.append(point.y)


        elif geometry.geom_type == 'LineString':
            coords = list(geometry.coords)
            for coord in coords:
                x_coords.append(coord[0])
                y_coords.append(coord[1])

            # 记录起止索引
            data_indices.append((current_index, current_index + len(coords)))
            current_index += len(coords)  # 更新当前索引

        # 如果几何是 MultiLineString（多段线），拆分为多段处理
        elif geometry.geom_type == 'MultiLineString':
            for line in geometry.geoms:
                coords = list(line.coords)
                for coord in coords:
                    x_coords.append(coord[0])
                    y_coords.append(coord[1])

                # 记录起止索引
                data_indices.append((current_index, current_index + len(coords)))
                current_index += len(coords)  # 更新当前索引

        # 如果几何是 Polygon（单面）
        elif geometry.geom_type == 'Polygon':
            # 提取外环坐标
            exterior_coords = list(geometry.exterior.coords)
            for coord in exterior_coords:
                x_coords.append(coord[0])
                y_coords.append(coord[1])
            # 记录起止索引
            data_indices.append((current_index, current_index + len(exterior_coords)))
            current_index += len(exterior_coords)

            # 提取内环坐标（如果有）
            for interior in geometry.interiors:
                interior_coords = list(interior.coords)
                for coord in interior_coords:
                    x_coords.append(coord[0])
                    y_coords.append(coord[1])
                # 记录内环的起止索引
                data_indices.append((current_index, current_index + len(interior_coords)))
                current_index += len(interior_coords)

        # 如果几何是 MultiPolygon（多面）
        elif geometry.geom_type == 'MultiPolygon':
            # 遍历每个 Polygon
            for polygon in geometry.geoms:
                # 提取外环坐标
                exterior_coords = list(polygon.exterior.coords)
                for coord in exterior_coords:
                    x_coords.append(coord[0])
                    y_coords.append(coord[1])
                # 记录外环的起止索引
                data_indices.append((current_index, current_index + len(exterior_coords)))
                current_index += len(exterior_coords)

                # 提取内环坐标（如果有）
                for interior in polygon.interiors:
                    interior_coords = list(interior.coords)
                    for coord in interior_coords:
                        x_coords.append(coord[0])
                        y_coords.append(coord[1])
                    # 记录内环的起止索引
                    data_indices.append((current_index, current_index + len(interior_coords)))
                    current_index += len(interior_coords)

        else:
            print(f"跳过不支持的几何类型: {geometry.geom_type}")

    # 将坐标转为 numpy 数组
    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)

    # 计算顶点数和特征数
    F = len(gdf)    # 特征数 (总形状数)
    V = len(x_coords) # 顶点数
    print(f"特征数: {F}")
    print(f"顶点数: {V}")

    return F, V, x_coords, y_coords, data_indices


def scramble_coordinates(X, Y, x_coords, y_coords, vertex_count):

    indices_X = calculate_index2(X)
    indices_Y = calculate_index2(Y)

    for i in range(vertex_count):
        # 获取通过混沌序列计算出的索引
        idx_x = indices_X[i]  # 根据 X 序列得到 x 坐标交换位置
        idx_y = indices_Y[i]  # 根据 Y 序列得到 y 坐标交换位置

        # 交换 x 和 y 坐标的值
        x_coords[i], x_coords[idx_x] = x_coords[idx_x], x_coords[i]
        y_coords[i], y_coords[idx_y] = y_coords[idx_y], y_coords[i]

    return x_coords, y_coords


def unscramble_coordinates(X, Y, x_coords, y_coords, vertex_count):

    indices_X = calculate_index2(X)
    indices_Y = calculate_index2(Y)

    for i in range(vertex_count-1, -1, -1):    # vertex_count-1是起始值，中间的-1是结束(不包括在内)，最后一个-1是步长
        # 获取反向索引得到的原始位置
        idx_x = indices_X[i]  # 根据 X 序列恢复 x 坐标位置
        idx_y = indices_Y[i]  # 根据 Y 序列恢复 y 坐标位置

        # 交换坐标，恢复原始顺序
        x_coords[i], x_coords[idx_x] = x_coords[idx_x], x_coords[i]
        y_coords[i], y_coords[idx_y] = y_coords[idx_y], y_coords[i]

    return x_coords, y_coords
