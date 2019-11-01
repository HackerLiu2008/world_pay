import re
import requests
from .mysql_tools import SqlData


def ex_change():
    try:
        data = {
            'erectDate': '',
            'nothing': '',
            'pjname': '1316'
        }

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/54.0.2840.99 Safari/537.36'}

        url = 'http://srh.bankofchina.com/search/whpj/search.jsp'

        resp = requests.post(url, headers=headers, data=data)

        resp_text = resp.text

        title = re.findall('<td>(.*?)</td>', resp_text)

        return title[3]

    except Exception as e:
        print(e)
        return '9999999'


res = ex_change()
res = float(res)/100
SqlData().update_admin_field('ex_change', float(res))



