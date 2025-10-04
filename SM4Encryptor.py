from decimal import Decimal

from method.gmalg.sm4_2 import SM4

class Encryptor:
    def __init__(self, key, iv):
        self.sm4 = SM4(key, iv)


    def encrypt(self,  input_data):
        # 将数据转换为Decimal，避免精度问题
        data = Decimal(str(input_data))
        # 统计小数点后的位数
        decimal_places = len(str(data).split('.')[1]) if '.' in str(data) else 0
        # 计算缩放因子
        scale_factor = 10 ** (decimal_places + 2)
        # 转换成整数进行加密
        int_data = int(data * scale_factor + decimal_places)
        # 将整数转换为字节串（16字节）
        byte_data = int_data.to_bytes(16, byteorder='big')
        encrypted = self.sm4.encrypt_cbc( byte_data)  # 使用CBC模式加密
        return encrypted


    def decrypt(self, encrypted_data):
        # 解密得到字节串
        decrypted = self.sm4.decrypt_cbc(encrypted_data)
        # 将字节串转换回整数
        decrypted_int = int.from_bytes(decrypted, byteorder='big')

        decimal_places = decrypted_int % 100
        decrypted_int = decrypted_int // 100

        # 计算缩放因子
        scale_factor = Decimal(10) ** (-decimal_places)
        # 将整数转换回 Decimal 类型浮动数
        result = Decimal(decrypted_int) * scale_factor
        return float(result)



if __name__ == '__main__':
    sm4 = Encryptor(b'1234567890abcdef', b'1234567890abcdef')

    encrypted = sm4.encrypt( 1.23456789)
    print(encrypted)
    decrypted = sm4.decrypt(encrypted)
    print(decrypted)
    assert decrypted == 1.23456789
    print("SM4 加解密测试通过")