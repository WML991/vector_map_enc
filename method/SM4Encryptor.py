from decimal import Decimal

from method.gmalg.sm4_2 import SM4

class Encryptor:
    def __init__(self, key, iv):
        self.sm4 = SM4(key, iv)


    def encrypt(self,  input_data):
        data = Decimal(str(input_data))
        decimal_places = len(str(data).split('.')[1]) if '.' in str(data) else 0
        scale_factor = 10 ** (decimal_places + 2)
        int_data = int(data * scale_factor + decimal_places)
        byte_data = int_data.to_bytes(16, byteorder='big')
        encrypted = self.sm4.encrypt_cbc( byte_data) 
        return encrypted


    def decrypt(self, encrypted_data):
        decrypted = self.sm4.decrypt_cbc(encrypted_data)
        decrypted_int = int.from_bytes(decrypted, byteorder='big')
        decimal_places = decrypted_int % 100
        decrypted_int = decrypted_int // 100
        scale_factor = Decimal(10) ** (-decimal_places)
        result = Decimal(decrypted_int) * scale_factor
        return float(result)
