# coding:utf-8

import base64
from Crypto.Cipher import AES


class USE_AES:
    """
    AES
    除了MODE_SIV模式key长度为：32, 48, or 64,
    其余key长度为16, 24 or 32
    详细见AES内部文档
    CBC模式传入iv参数
    本例使用常用的ECB模式
    """

    def __init__(self, key):
        if len(key) > 32:
            key = key[:32]
        self.key = self.to_16(key)

    def to_16(self, key):
        """
        转为16倍数的bytes数据
        :param key:
        :return:
        """
        key = bytes(key, encoding="utf8")
        while len(key) % 32 != 0:
            key += b'\0'
            # print("to_16")
        return key  # 返回bytes

    def aes(self):
        return AES.new(self.key, AES.MODE_ECB) # 初始化加密器

    def encrypt(self, text):
        aes = self.aes()
        return str(base64.encodebytes(aes.encrypt(self.to_16(text))),
                   encoding='utf8').replace('\n', '')  # 加密

    def decodebytes(self, text):
        aes = self.aes()
        return str(aes.decrypt(base64.decodebytes(bytes(
            text, encoding='utf-8'))).rstrip(b'\0').decode("utf-8"))  # 解密


if __name__ == '__main__':
    # aes_test = USE_AES("e9abe30a15422ae73bc39aa89ccd75d52f72c3ff")
    aes_test = USE_AES("e9fc52c72346ecc9")
    encrypt = aes_test.encrypt('蔡志伟')
    decode = aes_test.decodebytes(encrypt)
    print(encrypt)
    print(decode)