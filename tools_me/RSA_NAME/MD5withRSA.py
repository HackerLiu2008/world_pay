from Crypto.PublicKey import RSA
import base64
from Crypto.Hash import SHA1,MD5
from Crypto.Signature import pkcs1_15


def get_private_key(filepath):
    return RSA.import_key(open(filepath).read())


def get_public_key(filepath):
    return RSA.importKey(open(filepath).read())


def rsa_MD5sign(message, privatekey_filepath):
    #读取私钥信息用于加签
    private_key = get_private_key(privatekey_filepath)
    print(private_key)
    hash_obj = MD5.new(message)
    print(hash_obj)
    # print(pkcs1_15.new(private_key).can_sign())  #check wheather object of pkcs1_15 can be signed
    #base64编码打印可视化
    signature = base64.b64encode(pkcs1_15.new(private_key).sign(hash_obj))
    print(signature)
    return signature


def rsa_MD5signverify(message,signature,publickey_filepath):
    #读取公钥信息用于验签
    public_key = get_public_key(publickey_filepath)
    #message做“哈希”处理，RSA签名这么要求的
    hash_obj = MD5.new(message)
    try:
        #因为签名被base64编码，所以这里先解码，再验签
        pkcs1_15.new(public_key).verify(hash_obj,base64.b64decode(signature))
        print('The signature is valid.')
        return True
    except (ValueError,TypeError):
        print('The signature is invalid.')


if __name__ == '__main__':
    private_key = """-----BEGIN ENCRYPTED PRIVATE KEY-----
MIICYAIBAAKBgQCvobO+YleFShQP8sCZrQDP/hhLrtEBxHBtX3yhkbPmq5B7d0yxWqDxROciagvv39noJA6Zfs3B6jr4nJtVBM8RvrvgSBcYbQmZwkNN9LGhR20KyVVVuo0NDg53dQoTYgiPGynUYv+ANPvBywHK23tgnnR2rkpnfMBGf9bB8/ZcsQIDAQABAoGAbm7GjldXoL/LjZud7wMRF7c1n6D0WqAh8SOxQgZTkB8gYgHJf1r1B7/DdagoiVO/uG+znmBVEDEvk1MlAUqvdPngBVwmsI/pvCr+akNmRbZg3xA2qq0u4zXiaU8Jhix7bsSskoMZU3ky25Zsy9Vkg7vi2OeQ5LW81Zij5KQ+IAECRQC9ibMXQN1gxh6d3Mae2CMVjm2c9v8+WFH8P9nweDSkHWqVQgzpbWzzfuX9aeNTYoL1CpRwsyuSSaLfIC+wnT1vQIHYcQI9AO03rV78LWcCRBHDoHQG4X8IWLIdf/+Aok2bHKSnUW0EYNINcCgOh9pqprSVwy+29AZubVp9/t5SgFjoQQJEY5yZ5c+uSSz2bErajCLVlX+sNgFNtete8y5vkMTsDZB0MotrE8bxqqr3no5m7azpXHU5/Fz9uj0+/vsAdVa+Mdj6JNECPFacFXiwqgMKGMBDpLm4KWywJ3IgwzMOTDP5hiO300ryZkdLEMAPThq5BdS5OWKacc5HUzXO+tdBWAseAQJFAINoOEXr/jaDt2Lvco8750hSuwWjl5GulgyEb6kEpqtgZHgseZ6otDb8di6B4zZN0PNlh1haQAWJpbWuC62WlbeD7TgA
-----END ENCRYPTED PRIVATE KEY-----"""
    public_key =  """-----BEGIN PUBLIC KEY-----
MIGJAoGBAK+hs75iV4VKFA/ywJmtAM/+GEuu0QHEcG1ffKGRs+arkHt3TLFaoPFE5yJqC+/f2egkDpl+zcHqOvicm1UEzxG+u+BIFxhtCZnCQ030saFHbQrJVVW6jQ0ODnd1ChNiCI8bKdRi/4A0+8HLAcrbe2CedHauSmd8wEZ/1sHz9lyxAgMBAAE=
-----END PUBLIC KEY-----"""
    message = b'123456'
    privatekey_filepath = "G:\\world_pay\\tools_me\\RSA_NAME\\privkey.pem"
    publickey_filepath = "G:\\world_pay\\tools_me\\RSA_NAME\\pubkey.pem"

    # create_rsa_key()
    signature = rsa_MD5sign(message, privatekey_filepath)
    # print('signature:',signature)
    # signature是java程序使用相同公钥对字符串"123456"的MD5withRSA签名结果
    # signature='n6iuYyfl4vVvOWSVCAlLpK/1ZWscRIYn2Gaql6DcozkXgtfn2r3CnWQPMB4gt+GW2HT7G7ML+B0wMpRPMWwo9VHh5EJzghTiMkRqgjoOAfDNC0gg7fvZVW4XwUv9NdRDh9ij2DO4PmwvQG6JV7mMp1+y6ox89r0MA2w9O5oKaeY='
    # print(rsa_MD5signverify(message,signature,publickey_filepath))