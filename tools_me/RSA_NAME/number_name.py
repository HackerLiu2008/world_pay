# -*- coding:utf-8 -*-
import rsa
import base64


# 生成RSA公钥和秘钥,经过base64转码
(pubkey, privkey) = rsa.newkeys(1024)


# 经过base64编码
# pubkey = base64.encodebytes(pubkey.save_pkcs1())
# privkey = base64.encodebytes(privkey.save_pkcs1())

# 原始
pubkey = pubkey.save_pkcs1()
privkey =privkey.save_pkcs1()

# with open('pubkey.pem', 'wb+') as f:
#     f.write(pubkey)
#
# with open('privkey.pem', 'wb+') as f:
#     f.write(privkey)
print(pubkey)
print(privkey)


# 给java的pkcs1
privkey=str(privkey).replace('\\n','').replace("b'-----BEGIN RSA PRIVATE KEY-----",'').replace("-----END RSA PRIVATE KEY-----'",'').replace(' ','')
print(privkey)
