from method.gmalg.sm3 import sm3_hash
from chaotic_system import solve_chaos_system


# 异或操作
def xor_strings(hex1, hex2):
    int1 = int(hex1, 16)    # 将16进制字符串转换为整数
    int2 = int(hex2, 16)
    return int1 ^ int2

    # 初始化参数
file_size = 1024  # 文件大小（字节）
vertex_count = 10  # 顶点数量
feature_count = 5  # 特征数量
key = "securekey"  # 加密密钥

# 系统参数
a, b, c, d, e = 10, 28, 8 / 3, 1, 16  # 混沌系统参数
S_len = 256  # S 的长度
C = vertex_count % 100 +1

# 第一步：计算 S = SM3(File size) ⊕ SM3(顶点数)
file_size_hash = sm3_hash(str(file_size))
vertex_count_hash = sm3_hash(str(vertex_count))
S = xor_strings(file_size_hash, vertex_count_hash)
S_bin = bin(S)[2:].zfill(256)  # 转换为256位二进制
print("S (256位二进制):", S_bin)

# 第二步：分割 S 为 s1, s2, ..., s32
s_list = [S_bin[i:i + 8] for i in range(0, 256, 8)]  # 每8位分为一组
print("s_list (分组后):", s_list)

# 第三步：计算 U1, U2, ..., U32
U_prev = S_bin  # 初始值是 S 的二进制表示
U_list = []

for i in range(32):
    input_data = s_list[31 - i] + key + U_prev  # 根据公式：s32||key||U_{i-1}
    U_prev = sm3_hash(input_data)
    U_list.append(U_prev)
    # print(f"U{i + 1}: {U_prev}")

# 第四步：将 U32 分割为 e1, e2, ..., e8
U32 = U_list[-1]  # 取最后一个 U 值
e_list = [int(U32[i:i + 8], 16) for i in range(0, 64, 8)]  # 每8位转换为十六进制整数
e1, e2, e3, e4, e5, e6, e7, e8 = e_list[:8]
# print("e1, e2, e3, e4, e5, e6, e7, e8:", e1, e2, e3, e4, e5, e6, e7, e8)

# 第五步：计算初始值 ux, uy, uz, uw
V = vertex_count
F = feature_count

def compute_initial_value(e_vals, mod_vals, c, V, F, S_len):
    """通用初值计算公式"""
    numerator = (e_vals[0] ^ e_vals[1] ^ e_vals[2] ^ e_vals[3]) + (mod_vals[0] * mod_vals[1]) % S_len
    scaled_value = (c / (V * F)) * numerator
    return scaled_value - int(scaled_value)

ux = compute_initial_value([e1, e3, e5, e7], [e2, e4], C, V, F, S_len)
uy = compute_initial_value([e2, e4, e6, e8], [e3, e5], C, V, F, S_len)
uz = compute_initial_value([e3, e5, e7, e1], [e4, e6], C, V, F, S_len)
uw = compute_initial_value([e4, e6, e8, e2], [e1, e7], C, V, F, S_len)

print(f"初始值: ux={ux}, uy={uy}, uz={uz}, uw={uw}")

t, x_vals, y_vals, z_vals, w_vals = solve_chaos_system(a, b, c, d, e, ux, uy, uz, uw)
# x的前100个值,带提示
print(f"x的前100个值: {x_vals[:100]}")
print(f"y的前100个值: {y_vals[:100]}")
print(f"z的前100个值: {z_vals[:100]}")
print(f"w的前100个值: {w_vals[:100]}")




