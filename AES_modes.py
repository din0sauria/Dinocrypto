#23 网安 dinosaur 
import base64
import time
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad

class ECB:
    def aes_decode(self, data, key):
        try:
            aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器
            decrypted_text = aes.decrypt(base64.decodebytes(bytes(data, encoding='utf8'))).decode("utf8")  # 解密
            decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]  # 去除多余补位
        except Exception as e:
            pass
        return decrypted_text
    
    def aes_encode(self, data, key):
        while len(data) % 16 != 0:  # 补足字符串长度为16的倍数
            data += (16 - len(data) % 16) * chr(16 - len(data) % 16)
        data = str.encode(data)
        aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器
        return str(base64.encodebytes(aes.encrypt(data)), encoding='utf8').replace('\n', '')  # 加密
    
    def main(self,key = 'asdfzxcvg0qwerab' ,data = "dinosuardinosaurdinosaur" ):
        print(">>ECB")
 
        mi = self.aes_encode(data, key)
        print("加密值：", mi)
        print("解密值：", self.aes_decode(mi, key))

class CBC:
    def aes_encode(self, key, content):
        key_bytes = bytes(key, encoding='utf-8')
        iv = get_random_bytes(16)  # 使用随机IV
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        content_padding = self.pkcs7padding(content)
        aes_encode_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
        result = base64.b64encode(iv + aes_encode_bytes).decode('utf-8')  # 包含IV
        return result

    def aes_decode(self, key, content):
        try:
            key_bytes = bytes(key, encoding='utf-8')
            iv = base64.b64decode(content)[:16]
            cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
            aes_encode_bytes = base64.b64decode(content)[16:]
            aes_decode_bytes = cipher.decrypt(aes_encode_bytes)
            result = self.pkcs7unpadding(aes_decode_bytes.decode('utf-8'))
        except Exception as e:
            result = ""
        return result

    def pkcs7padding(self, text):
        bs = AES.block_size
        padding = bs - len(text) % bs
        padding_text = chr(padding) * padding
        return text + padding_text

    def pkcs7unpadding(self, text):
        padding = ord(text[-1])
        return text[:-padding]

    def main(self,key = 'asdfqwerg01234ab',data = 'dinosuardinosaurdinosaur'):
        print(">>CBC")
        mi = self.aes_encode(key, data)
        print("加密值：", mi)
        print("解密值：", self.aes_decode(key, mi))

class OFB:
    def main(self,key = 'asdfqwerg01234ab',data = b"dinosaurdinosaurdinosaur"):
        print(">>OFB")
        key = get_random_bytes(16)
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_OFB, iv)
        encrypted_data = cipher.encrypt(data)
        print("加密值：", encrypted_data)
        cipher_dec = AES.new(key, AES.MODE_OFB, iv)
        decrypted_data = cipher_dec.decrypt(encrypted_data)
        print("解密值：", decrypted_data.decode('utf-8'))

class CFB:
    def aes_cfb_encode(self, data, key):
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CFB, iv)
        return base64.b64encode(iv + cipher.encrypt(data.encode('utf-8'))).decode('utf-8')

    def aes_cfb_decode(self, enc, key):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CFB, iv)
        return cipher.decrypt(enc[AES.block_size:]).decode('utf-8')

    def main(self,key = 'asdfzxcvg0qwerab',data = "dinosuardinosaurdinosaur"):
        print(">>CFB")
        encrypted_data = self.aes_cfb_encode(data, key)
        print("加密值：", encrypted_data)
        decrypted_data = self.aes_cfb_decode(encrypted_data, key)
        print("解密值：", decrypted_data)

class XCBC:
    # 这里需要设置你的32位字节密钥
    ENCRYPT_OR_DECRYPT_KEY = b'1234567890abcdef1234567890abcdef'
    # AES的块大小是16字节，所以IV也需要是16字节
    BLOCK_SIZE = AES.block_size
    # CBC模式和PKCS5Padding
    MODE = AES.MODE_CBC
    PADDING = 'pkcs7'
 
    def encrypt(self, password: str) -> str:
        cipher = AES.new(self.ENCRYPT_OR_DECRYPT_KEY, self.MODE)
        # CBC模式需要一个随机生成的IV
        iv = cipher.iv
        # 加密
        cipher = AES.new(self.ENCRYPT_OR_DECRYPT_KEY, self.MODE, iv)
        ciphertext = cipher.encrypt(pad(password.encode('utf-8'), self.BLOCK_SIZE, style=self.PADDING))
        # IV不需要保密，把IV和密文一起返回
        return base64.b64encode(iv + ciphertext).decode('utf-8')
 
    def decrypt(self, encrypted_password: str) -> str:
        encrypted_bytes = base64.b64decode(encrypted_password)
        iv = encrypted_bytes[:self.BLOCK_SIZE]
        ciphertext = encrypted_bytes[self.BLOCK_SIZE:]
        # 解密
        cipher = AES.new(self.ENCRYPT_OR_DECRYPT_KEY, self.MODE, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), self.BLOCK_SIZE, style=self.PADDING)
        return plaintext.decode('utf-8')
 
    def main(self,KEY = b'1234567890abcdef1234567890abcdef',data = "dinosuardinosaurdinosaur"):
        self.ENCRYPT_OR_DECRYPT_KEY=KEY
        print(">>XCBC")
        secret_util =  XCBC()
        encrypt_str = secret_util.encrypt(data)
        print("加密值：", encrypt_str)
        decrypt_str = secret_util.decrypt(encrypt_str)
        print("解密值：", decrypt_str)

class CTR:
    def aes_ctr_encode(self, data, key):
        ctr = AES.new(key.encode('utf-8'), AES.MODE_CTR, nonce=b'')
        return base64.b64encode(ctr.encrypt(data.encode('utf-8'))).decode('utf-8')

    def aes_ctr_decode(self, enc, key):
        ctr = AES.new(key.encode('utf-8'), AES.MODE_CTR, nonce=b'')
        return ctr.decrypt(base64.b64decode(enc)).decode('utf-8')

    def main(self,key = 'dinosaurdinosaur',data = "dinosuardinosaurdinosaur"):
        print(">>CTR")
        encrypted_data = self.aes_ctr_encode(data, key)
        print("加密值：", encrypted_data)
        decrypted_data = self.aes_ctr_decode(encrypted_data, key)
        print("解密值：", decrypted_data)

def en_de_test():
    aes = ECB()
    aes.main()

    cbc = CBC()
    cbc.main()

    ofb = OFB()
    ofb.main()

    cfb = CFB()
    cfb.main()

    xcpc = XCBC()
    xcpc.main()

    ctr = CTR()
    ctr.main()

def test2():
    ecb = ECB()
    ecb.main(key= 'asdfzxcvg0qwerab',data = "dinosuardinosaurdinosaur")
    ecb.main(key= 'asdfzxcvg0qwerab',data = "Dinosuardinosaurdinosaur")

    cbc = CBC()
    cbc.main(key='asdfzxcvg0qwerab',data = "dinosuardinosaurdinosaur")
    cbc.main(key='asdfzxcvg0qwerab',data = "Dinosuardinosaurdinosaur")

    ofb = OFB()
    ofb.main(key='asdfzxcvg0qwerab',data = b"dinosuardinosaurdinosaur")
    ofb.main(key='asdfzxcvg0qwerab',data = b"Dinosuardinosaurdinosaur")

    cfb = CFB()
    cfb.main(key='asdfzxcvg0qwerab',data = "dinosuardinosaurdinosaur")
    cfb.main(key='asdfzxcvg0qwerab',data = "Dinosuardinosaurdinosaur")


    xcpc = XCBC()
    xcpc.main(KEY= b'1234567890abcdef1234567890abcdef',data= "dinosuardinosaurdinosaur")
    xcpc.main(KEY= b'1234567890abcdef1234567890abcdef',data= "Dinosuardinosaurdinosaur")

    ctr = CTR()
    ctr.main(key='asdfzxcvg0qwerab',data = "dinosuardinosaurdinosaur")
    ctr.main(key='asdfzxcvg0qwerab',data = "Dinosuardinosaurdinosaur")

def test3():
    ecb = ECB()
    ecb.main(key= 'asdfzxcvg0qwerab',data = "dinosuardinosaurdinosaur")
    ecb.main(key= 'Asdfzxcvg0qwerab',data = "dinosuardinosaurdinosaur")

    cbc = CBC()
    cbc.main(key='asdfzxcvg0qwerab',data = "dinosuardinosaurdinosaur")
    cbc.main(key='Asdfzxcvg0qwerab',data = "dinosuardinosaurdinosaur")

    ofb = OFB()
    ofb.main(key='asdfzxcvg0qwerab',data = b"dinosuardinosaurdinosaur")
    ofb.main(key='Asdfzxcvg0qwerab',data = b"dinosuardinosaurdinosaur")

    cfb = CFB()
    cfb.main(key='asdfzxcvg0qwerab',data = "dinosuardinosaurdinosaur")
    cfb.main(key='Asdfzxcvg0qwerab',data = "dinosuardinosaurdinosaur")


    xcpc = XCBC()
    xcpc.main(KEY= b'1234567890abcdef1234567890abcdef',data= "dinosuardinosaurdinosaur")
    xcpc.main(KEY= b'0234567890abcdef1234567890abcdef',data= "dinosuardinosaurdinosaur")

    ctr = CTR()
    ctr.main(key='asdfzxcvg0qwerab',data = "dinosuardinosaurdinosaur")
    ctr.main(key='Asdfzxcvg0qwerab',data = "dinosuardinosaurdinosaur")

def test4():

    aes = ECB()
    cbc = CBC()
    ofb = OFB()
    cfb = CFB()
    xcpc = XCBC()
    ctr = CTR()

    key = 'asdfzxcvg0qwerab'
    data = "dinosuardinosaurdinosaur" * 1000  # 增大数据量以便更好地比较性能

    modes = {
        'ECB': aes,
        'CBC': cbc,
        'OFB': ofb,
        'CFB': cfb,
        'XCBC': xcpc,
        'CTR': ctr
    }

    results = []

    for mode_name, mode_instance in modes.items():
        start_time = time.time()
        for _ in range (int(1e4)): mode_instance.main()
        end_time = time.time()
        encode_time = end_time - start_time
        results.append((mode_name,encode_time))

    results.sort(key=lambda x: x[1])

    for mode_name,encode_time in results: print(f"{mode_name}: {encode_time}")
        



if __name__ == '__main__':
    en_de_test()
    #test2()
    #test3()
    #test4()