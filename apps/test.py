from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5, pkcs1_15
from Crypto.Hash import MD5
from urllib.parse import urlencode, quote, unquote
import base64, json, requests, datetime, time
import urllib.parse


def rsa_sign(data):
    private_key_file = open('G:\\world_pay\\tools_me\\RSA_NAME\\new_pri.pem', 'r')
    pri_key = RSA.importKey(private_key_file.read())
    signer = PKCS1_v1_5.new(pri_key)
    hash_obj = my_hash(data)
    signature = base64.b64encode(signer.sign(hash_obj))
    private_key_file.close()
    return signature

def rsa_verify(signature, data):
    public_key_file = open('app_public_key.pem', 'r')
    pub_key = RSA.importKey(public_key_file.read())
    hash_obj = my_hash(data)
    verifier = PKCS1_v1_5.new(pub_key)
    public_key_file.close()
    return verifier.verify(hash_obj, base64.b64decode(signature))


def my_hash(data):
    return MD5.new(data.encode('utf-8'))


if __name__ == '__main__':
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'api_name': 'epaylinks_umps_user_query_acct_info',
        'ver': '1.0',
        'format': 'json',
        'app_id': 'tjvdm5wlX2oKN8rB8idvA2Fi',
        'terminal_no': '36248614',
        'card_no': '0103000589761585',
        'timestamp': ts,
    }
    print(ts)
    sort_keys = sorted(data.keys())
    kv_list = []
    for key in sort_keys:
        kv_list.append(str(key)+'='+str(data[key]))
    data_str = '&'.join(kv_list)

    sign = rsa_sign(data_str)
    print(sign)
    data['sign'] = sign.decode()

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    res = requests.post('https://www.globalcash.hk/openapi/service', data=data, headers=headers)

    print(res.json())