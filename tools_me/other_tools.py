import datetime
import json
import os
import time
from functools import wraps
from itertools import combinations
from flask import current_app, session, g, render_template
from xlrd import xldate_as_tuple
from config import logging
import uuid

ALLOWED_EXTENSIONS = ['xls', 'xlsx']


def allowe_file(filename):
    '''
    限制上传的文件格式
    :param filename:
    :return:
    '''
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def change_filename(filename):
    '''
    修改文件名称
    :param filename:
    :return:
    '''
    fileinfo, fext = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + fext
    return filename


def now_filename():
    filename = datetime.datetime.now().strftime("%Y%m%d")
    return filename


def now_day():
    filename = datetime.datetime.now().strftime("%Y-%m-%d")
    return filename


def xianzai_time():
    now_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now_datetime


def sum_code():
    now_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    sum_order_code = now_datetime + str(uuid.uuid1())[:5]
    return sum_order_code


def save_file(file, filename, account_path):
    if allowe_file(filename):
        bigpath = os.path.join(current_app.root_path, account_path, now_filename())
        if not os.path.exists(bigpath):
            try:
                os.makedirs(bigpath)
            except:
                logging.info("warning 创建目录失败")
                return "创建目录失败, 看日志去%s" % bigpath
        new_name = change_filename(filename)
        filepath = bigpath + "/" + new_name
        try:
            file.save(filepath)
        except Exception as e:
            logging.error("写入文件出错:" + str(e))

        return str(filepath)


def excel_to_data(num):
    t = xldate_as_tuple(num, 0)
    year = t[0]
    month = t[1]
    day = t[2]
    s = "{}-{}-{}".format(year, month, day)
    return s


# datatime格式时间转换成时间戳格式,
def datatime_to_timenum(tss1):
    timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


# 验证两个日期大小
def verify_login_time(before_time, now_time):
    seconds = datatime_to_timenum(now_time) - datatime_to_timenum(before_time) + 1
    if seconds > 0:
        return True
    else:
        return


def login_required(view_func):
    """自定义装饰器判断用户是否登录
    使用装饰器装饰函数时，会修改被装饰的函数的__name属性和被装饰的函数的说明文档
    为了不让装饰器影响被装饰的函数的默认的数据，我们会使用@wraps装饰器，提前对view_funcJ进行装饰
    """

    @wraps(view_func)
    def wraaper(*args, **kwargs):
        """具体实现判断用户是否登录的逻辑"""
        user_id = session.get('user_id')
        user_name = session.get('user_name')
        us_time = session.get('us_time')
        pass_word = session.get('pass_word')
        expire_time = session.get('expire_time')
        terrace = session.get('terrace')
        if not user_id:
            return render_template('user/login.html')
        else:
            # 当用户已登录，使用g变量记录用户的user_id，方便被装饰是的视图函数中可以直接使用
            g.user_id = user_id
            g.user_name = user_name
            g.us_time = us_time
            g.pass_word = pass_word
            g.expire_time = expire_time
            g.terrace = terrace
            # 执行被装饰的视图函数
            return view_func(*args, **kwargs)

    return wraaper


def customer_required(view_func):
    """自定义装饰器判断用户是否登录
    使用装饰器装饰函数时，会修改被装饰的函数的__name属性和被装饰的函数的说明文档
    为了不让装饰器影响被装饰的函数的默认的数据，我们会使用@wraps装饰器，提前对view_funcJ进行装饰
    """

    @wraps(view_func)
    def wraaper(*args, **kwargs):
        """具体实现判断用户是否登录的逻辑"""
        cus_id = session.get('cus_id')
        cus_account = session.get('customer_account')
        cus_label = session.get('customer_label')
        cus_discount = session.get('customer_discount')
        cus_user_id = session.get('customer_user_id')
        if not cus_label:
            return render_template('customer/login_customer.html')
        else:
            # 当用户已登录，使用g变量记录用户的user_id，方便被装饰是的视图函数中可以直接使用
            g.cus_label = cus_label
            g.cus_id = cus_id
            g.cus_account = cus_account
            g.cus_discount = cus_discount
            g.cus_user_id = cus_user_id
            # 执行被装饰的视图函数
            return view_func(*args, **kwargs)

    return wraaper


def middle_required(view_func):
    """自定义装饰器判断用户是否登录
    使用装饰器装饰函数时，会修改被装饰的函数的__name属性和被装饰的函数的说明文档
    为了不让装饰器影响被装饰的函数的默认的数据，我们会使用@wraps装饰器，提前对view_funcJ进行装饰
    """

    @wraps(view_func)
    def wraaper(*args, **kwargs):
        """具体实现判断用户是否登录的逻辑"""
        middle_id = session.get('middle_id')
        middle_user_id = session.get('middle_user_id')
        middle_name = session.get('middle_name')
        if not middle_id:
            return render_template('middle/login.html')
        else:
            # 当用户已登录，使用g变量记录用户的user_id，方便被装饰是的视图函数中可以直接使用
            g.middle_id = middle_id
            g.middle_user_id = middle_user_id
            g.middle_name = middle_name
            # 执行被装饰的视图函数
            return view_func(*args, **kwargs)

    return wraaper


def check_param(terrace, country, store, asin, store_group, asin_group):
    terrace_info = ''
    country_info = ''
    store_day = ''
    asin_day = ''
    store_info = ''
    asin_info = ''
    if terrace == 'AMZ':
        terrace_info = "AMZ"
    if terrace == 'SMT':
        terrace_info = 'SMT'
    if country == '0':
        country_info = '美国'
    if country == '1':
        country_info = "德国"
    if country == '2':
        country_info = '英国'
    if country == '3':
        country_info = '法国'
    if country == '4':
        country_info = '俄罗斯'
    if country == '5':
        country_info = '意大利'
    if country == '6':
        country_info = '新加坡'
    if country == '7':
        country_info = '印度'
    if country == '8':
        country_info = '西班牙'
    if country == '9':
        country_info = '日本'
    if country == '10':
        country_info = '澳洲'
    if country == '11':
        country_info = '印尼'
    if country == '12':
        country_info = '泰国'
    if country == '13':
        country_info = '马来西亚'
    if country == '14':
        country_info = '台湾'
    if country == '15':
        country_info = '越南'
    if country == '16':
        country_info = '菲律宾'
    if store == '0':
        store_day = 0
    if store == '1':
        store_day = 7
    if store == '2':
        store_day = 15
    if asin == '0':
        asin_day = 0
    if asin == '1':
        asin_day = 20
    if asin == '2':
        asin_day = 30
    if store_group == '0':
        store_info = 2
    if store_group == '1':
        store_info = 3
    if asin_group == '0':
        asin_info = 2
    if asin_group == '1':
        asin_info = 3
    return terrace_info, country_info, store_day, asin_day, store_info, asin_info


# 时间戳转换成datatime格式字符串,timeStamp必须是str类型
def timenum_to_datatime(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


# 验证datatime格式日期大小
def verify_data_time(before_time, now_time, day_num):
    seconds = datatime_to_timenum(now_time) - datatime_to_timenum(before_time)
    interval_seconds = day_num * 24 * 60 * 60
    if seconds > interval_seconds:
        return True
    else:
        return False


def combine(temp_list, n):
    '''
    根据n获得列表中的所有可能组合（n个元素为一组）
    '''
    end_list = []
    temp_list2 = []
    for c in combinations(temp_list, n):
        temp_list2.append(c)
    end_list.extend(temp_list2)
    return end_list


# 去除重复的组合,返回可用的account字典
def repeat_asin(account_action_asin):
    # 将所有的组合汇总到同一个list
    key_list = list(account_action_asin.keys())
    tem_list = list()
    for i in key_list:
        asin_com = account_action_asin.get(i)
        tem_list.extend(asin_com)

    # 取出重合的组合
    index = 0
    tem_list_1 = list()
    for i in tem_list:
        new_list = tem_list[0:index] + tem_list[index + 1:]
        for n in new_list:
            if set(i).issubset(set(n)) and i not in tem_list_1:
                tem_list_1.append(i)
        index += 1

    # 将含有相同组合的账号删除
    for i in key_list:
        asin_com = account_action_asin.get(i)
        for n in tem_list_1:
            if n in asin_com:
                del account_action_asin[i]

    # 返回过滤后的符合要求的账号
    return account_action_asin


def filter_by_time(account_action_list, last_day):
    index = 0
    match_list = list()
    for i in account_action_list:
        last_buy_time = i.get('last_buy_time')
        if last_buy_time:
            now_data_time = timenum_to_datatime(time.time())
            # INTERVAL_LAST_BUY:限定间隔上次购买多少天(int类型),last_buy_time上次购买商品时间,now_time当前时间
            results = verify_data_time(str(last_buy_time), now_data_time, last_day)
            if results:
                match_list.append(account_action_list[index])
            index += 1
        else:
            match_list.append(account_action_list[index])
            index += 1
    return match_list


def filter_by_store(match_of_time, store_name, store, store_group):
    match_of_store = list()
    if store == 0:
        for one_action in match_of_time:
            stores = one_action.get('stores')
            if stores:
                store_list = list(json.loads(stores).keys())
                if store_name not in store_list:
                    match_of_store.append(one_action)
            else:
                match_of_store.append(one_action)
    if store != 0:
        for one_action in match_of_time:
            # [{},{},{}]
            stores = one_action.get('stores')
            if stores:
                stores_data = json.loads(stores)
                now_time = xianzai_time()
                store_list = list(stores_data.keys())
                for good in store_list:
                    if store_name == good and verify_data_time(stores_data.get(good), now_time, store):
                        match_of_store.append(one_action)
                    else:
                        match_of_store.append(one_action)
            else:
                match_of_store.append(one_action)

    have_store = dict()
    has_store = dict()
    for one_action in match_of_store:
        stores = one_action.get('stores')
        account_id = one_action.get('account_id')
        if stores:
            stores_data = json.loads(stores)
            store_name_list = list(stores_data.keys())
            if store_group <= len(store_name_list):
                one_store_group = combine(store_name_list, store_group)
                have_store[account_id] = one_store_group
            else:
                has_store[account_id] = ''
        else:
            has_store[account_id] = ''

    results = repeat_asin(have_store)
    has_store.update(results)
    keys_list = has_store.keys()
    successful_list = list()
    for key in keys_list:
        index = 0
        for i in match_of_time:
            account_id = i.get('account_id')
            if key == account_id:
                successful_list.append(match_of_time[index])
            index += 1
    return successful_list


def filter_by_asin(match_of_store, asin_name, asin, asin_group):
    match_of_asin = list()
    if asin == 0:
        for one_action in match_of_store:
            stores = one_action.get('goods')
            if stores:
                store_list = list(json.loads(stores).keys())
                if asin_name not in store_list:
                    match_of_asin.append(one_action)
            else:
                match_of_asin.append(one_action)
    if asin != 0:
        for one_action in match_of_store:
            # [{},{},{}]
            stores = one_action.get('goods')
            if stores:
                stores_data = json.loads(stores)
                now_time = xianzai_time()
                store_list = list(stores_data.keys())
                for good in store_list:
                    if asin_name == good and verify_data_time(stores_data.get(good), now_time, asin):
                        match_of_asin.append(one_action)
                    else:
                        match_of_asin.append(one_action)
            else:
                match_of_asin.append(one_action)

    have_store = dict()
    has_store = dict()
    for one_action in match_of_asin:
        stores = one_action.get('goods')
        account_id = one_action.get('account_id')
        if stores:
            stores_data = json.loads(stores)
            store_name_list = list(stores_data.keys())
            if asin_group <= len(store_name_list):
                one_store_group = combine(store_name_list, asin_group)
                have_store[account_id] = one_store_group
            else:
                has_store[account_id] = ''
        else:
            has_store[account_id] = ''

    results = repeat_asin(have_store)
    has_store.update(results)
    keys_list = list(has_store.keys())
    return keys_list


def asin_num(asin_list):
    res = {}
    for i in asin_list:
        res[i] = res.get(i, 0) + 1
    asin_num_dict = dict(zip([k for k in res.keys()], [v for v in res.values()]))
    return asin_num_dict


def date_to_week(t):
    date = datetime.datetime.strptime(t, '%Y-%m-%d')
    week = date.weekday()
    return week


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except:
        return False
    return True


def transferContent(content):
    if content is None:
        return None
    else:
        string = ""
        for i in content:
            if i == "'":
                i = "\\'"
                string += i
            elif i == '"':
                s = '\\"'
                string += s
            else:
                string += i
        return string
