import datetime
import json
import os
import random
import time
from functools import wraps
from flask import current_app, session, g, render_template
from xlrd import xldate_as_tuple
from config import logging
import uuid
from tools_me.mysql_tools import SqlData


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


def now_year():
    filename = datetime.datetime.now().strftime("%Y")
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
        user_name = session.get('name')
        if not user_id:
            return render_template('user/login.html')
        else:
            # 当用户已登录，使用g变量记录用户的user_id，方便被装饰是的视图函数中可以直接使用
            g.user_id = user_id
            g.user_name = user_name
            # 执行被装饰的视图函数
            return view_func(*args, **kwargs)

    return wraaper


def admin_required(view_func):
    """自定义装饰器判断用户是否登录
    使用装饰器装饰函数时，会修改被装饰的函数的__name属性和被装饰的函数的说明文档
    为了不让装饰器影响被装饰的函数的默认的数据，我们会使用@wraps装饰器，提前对view_funcJ进行装饰
    """

    @wraps(view_func)
    def wraaper(*args, **kwargs):
        """具体实现判断用户是否登录的逻辑"""
        admin_id = session.get('admin_id')
        admin_name = session.get('admin_name')
        if not admin_id:
            return render_template('admin/admin_login.html')
        else:
            # 当用户已登录，使用g变量记录用户的user_id，方便被装饰是的视图函数中可以直接使用
            g.admin_id = admin_id
            g.admin_name = admin_name
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
        if not middle_id:
            return render_template('middle/login_middle.html')
        else:
            # 当用户已登录，使用g变量记录用户的user_id，方便被装饰是的视图函数中可以直接使用
            g.middle_id = middle_id
            # 执行被装饰的视图函数
            return view_func(*args, **kwargs)

    return wraaper


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


# 获取n天前的日期列表
def get_nday_list(n):
    before_n_days = []
    for i in range(1, n + 1)[::-1]:
        time_str = str(datetime.date.today() - datetime.timedelta(days=i))
        t_s = time_str.split('-')
        day_time = t_s[1] + '.' + t_s[2]
        s = float(day_time)
        before_n_days.append(s)
    return before_n_days


def make_name(n):
    name_dict = SqlData().search_name_info()
    last_name = name_dict.get('last_name')
    female = name_dict.get('female')
    female_len = len(female)
    last_len = len(last_name)
    name_list = list()
    for i in range(n):
        name = female[random.randint(0, female_len-1)] + " " + last_name[random.randint(0, last_len-1)]
        name_list.append(name)
    return name_list

make_name(1000)