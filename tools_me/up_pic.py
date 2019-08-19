from qiniu import Auth, put_file


def up_photo(key, file_path, bucket_name):
    access_key = 'KgHe4AAvPJStXOlhxGB3ds-3ndsUxS-wypBwKAgW'
    secret_key = '6l1ujW79c4Zwo5XmpznDLTdQLaobW3As3r9fnol1'

    q = Auth(access_key, secret_key)

    token = q.upload_token(bucket_name, key, 3600)

    ret, info = put_file(token, key, file_path)

    return info.status_code, ret.get('key')
