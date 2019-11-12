# coding:utf-8

from threading import Lock
import operator
import threading
from tools_me.RSA_NAME.helen import QuanQiuFu


info = list()

lock = Lock()


def loop(card_info):
    global info
    card_no = card_info.get('card_no')
    try:
        resp = QuanQiuFu().query_card_info(card_no)
        if resp.get('resp_code') == '0000':
            detail = resp.get('response_detail')
            freeze_fee_all = detail.get('freeze_fee_all')
            balance = detail.get('balance')
            f_freeze = int(freeze_fee_all) / 100
            f_balance = int(balance) / 100
            remain = round(f_balance - f_freeze, 2)
        else:
            msg = resp.get('resp_msg')
            remain = msg
    except:
        remain = '查询失败!'
    card_info['remain'] = remain
    info.append(card_info)


def get_card_remain(loops):
    n = 1
    for i in loops:
        i['number'] = n
        n += 1
    lock.acquire()
    while True:
        loops_len = len(loops)
        num = 5
        if loops_len < 5:
            num = loops_len
        threads = []
        for i in range(num):
            data = loops.pop()
            t = threading.Thread(target=loop, args=(data, ))
            threads.append(t)
        for i in threads:  # start threads 此处并不会执行线程，而是将任务分发到每个线程，同步线程。等同步完成后再开始执行start方法
            i.start()
        for i in threads:  # jion()方法等待线程完成
            i.join()
        if len(loops) == 0:
            break
    lock.release()
    global info
    res = sorted(info, key=operator.itemgetter('number'))
    info = list()
    return res


if __name__ == '__main__':
    get_card_remain([{}, {}])
