from operator import index

import numpy as np
import geopandas as gpd
from method.FourD_chaos import calculate_index2


def extract_coordinates_from_shapefile(shapefile_path):
    gdf = gpd.read_file(shapefile_path)
    x_coords = []
    y_coords = []
    data_indices = []
    current_index = 0

    for _, row in gdf.iterrows():
        geometry = row['geometry']
        if geometry.geom_type == 'Point':
            x_coords.append(geometry.x)
            y_coords.append(geometry.y)
        elif geometry.geom_type == 'MultiPoint':
            for point in geometry:
                x_coords.append(point.x)
                y_coords.append(point.y)
        elif geometry.geom_type == 'LineString':
            coords = list(geometry.coords)
            for coord in coords:
                x_coords.append(coord[0])
                y_coords.append(coord[1])
            data_indices.append((current_index, current_index + len(coords)))
            current_index += len(coords) 
        elif geometry.geom_type == 'MultiLineString':
            for line in geometry.geoms:
                coords = list(line.coords)
                for coord in coords:
                    x_coords.append(coord[0])
                    y_coords.append(coord[1])
                data_indices.append((current_index, current_index + len(coords)))
                current_index += len(coords) 
        elif geometry.geom_type == 'Polygon':
            exterior_coords = list(geometry.exterior.coords)
            for coord in exterior_coords:
                x_coords.append(coord[0])
                y_coords.append(coord[1])
            data_indices.append((current_index, current_index + len(exterior_coords)))
            current_index += len(exterior_coords)
            for interior in geometry.interiors:
                interior_coords = list(interior.coords)
                for coord in interior_coords:
                    x_coords.append(coord[0])
                    y_coords.append(coord[1])
                data_indices.append((current_index, current_index + len(interior_coords)))
                current_index += len(interior_coords)
        elif geometry.geom_type == 'MultiPolygon':
            for polygon in geometry.geoms:
                exterior_coords = list(polygon.exterior.coords)
                for coord in exterior_coords:
                    x_coords.append(coord[0])
                    y_coords.append(coord[1])
                data_indices.append((current_index, current_index + len(exterior_coords)))
                current_index += len(exterior_coords)
                for interior in polygon.interiors:
                    interior_coords = list(interior.coords)
                    for coord in interior_coords:
                        x_coords.append(coord[0])
                        y_coords.append(coord[1])
                    data_indices.append((current_index, current_index + len(interior_coords)))
                    current_index += len(interior_coords)

        else:
            print(f"跳过不支持的几何类型: {geometry.geom_type}")

    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)

    F = len(gdf)    # 特征数 (总形状数)
    V = len(x_coords) # 顶点数
    print(f"特征数: {F}")
    print(f"顶点数: {V}")

    return F, V, x_coords, y_coords, data_indices


def scramble_coordinates(X, Y, x_coords, y_coords, vertex_count):

    indices_X = calculate_index2(X)
    indices_Y = calculate_index2(Y)
    print("indices_X:",indices_X)

    for i in range(vertex_count):
        idx_x = indices_X[i]  
        idx_y = indices_Y[i]  
        x_coords[i], x_coords[idx_x] = x_coords[idx_x], x_coords[i]
        y_coords[i], y_coords[idx_y] = y_coords[idx_y], y_coords[i]

    return x_coords, y_coords


def unscramble_coordinates(X, Y, x_coords, y_coords, vertex_count):

    indices_X = calculate_index2(X)
    indices_Y = calculate_index2(Y)

    for i in range(vertex_count-1, -1, -1):   
        idx_x = indices_X[i]  
        idx_y = indices_Y[i]  

        x_coords[i], x_coords[idx_x] = x_coords[idx_x], x_coords[i]
        y_coords[i], y_coords[idx_y] = y_coords[idx_y], y_coords[i]

    return x_coords, y_coords

