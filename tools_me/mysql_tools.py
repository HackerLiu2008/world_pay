import json
import pymysql
import logging
from flask import jsonify
from tools_me.other_tools import is_json
from tools_me.parameter import RET, MSG


class SqlData(object):
    def __init__(self):
        host = "127.0.0.1"
        port = 3306
        user = "root"
        password = "admin"
        database = "world_pay"
        self.connect = pymysql.Connect(
            host=host, port=port, user=user,
            passwd=password, db=database,
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    def close_connect(self):
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()

    # 一下是用户方法-----------------------------------------------------------------------------------------------------

    # 登录查询
    def search_user_info(self, user_name):
        sql = "SELECT id, password, name FROM account WHERE BINARY account = '{}'".format(user_name)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        try:
            user_data = dict()
            user_data['user_id'] = rows[0][0]
            user_data['password'] = rows[0][1]
            user_data['name'] = rows[0][2]
            return user_data
        except Exception as e:
            logging.error(str(e))
            return '账号或密码错误!'

    # 查询用户首页数据信息
    def search_user_index(self, user_id):
        sql = "SELECT create_price, refund, min_top, max_top, balance FROM account WHERE id = {}".format(user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        user_info = dict()
        user_info['create_card'] = rows[0][0]
        user_info['refund'] = rows[0][1]
        user_info['min_top'] = rows[0][2]
        user_info['max_top'] = rows[0][3]
        user_info['balance'] = rows[0][4]
        return user_info

    # 用户基本信息资料
    def search_user_detail(self, user_id):
        sql = "SELECT account, phone_num, balance FROM account WHERE id = {}".format(user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        user_info = dict()
        user_info['account'] = rows[0][0]
        user_info['phone_num'] = rows[0][1]
        user_info['balance'] = rows[0][2]
        return user_info

    # 查询用户的某一个字段信息
    def search_user_field(self, field, user_id):
        sql = "SELECT {} FROM account WHERE id = {}".format(field, user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    # 更新用户的某一个字段信息(str)
    def update_user_field(self, field, value, user_id):
        sql = "UPDATE account SET {} = '{}' WHERE id = {}".format(field, value, user_id)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新用户字段" + field + "失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    # 一下是中介使用方法-------------------------------------------------------------------------------------------------

    # 查询中介登录信息

    def search_middle_login(self, account):
        sql = "SELECT id, password FROM middle WHERE BINARY account='{}'".format(account)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    # 查询中介的你某一个字段信息
    def search_middle_field(self, field, middle_id):
        sql = "SELECT {} FROM middle WHERE id={}".format(field, middle_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

        # 用户基本信息资料

    def search_middle_detail(self, middle_id):
        sql = "SELECT account, phone_num, card_price FROM middle WHERE id = {}".format(middle_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        user_info = dict()
        user_info['account'] = rows[0][0]
        user_info['phone_num'] = rows[0][1]
        user_info['card_price'] = rows[0][2]
        return user_info

    # 更新用户的某一个字段信息(str)
    def update_middle_field(self, field, value, middle_id):
        sql = "UPDATE middle SET {} = '{}' WHERE id = {}".format(field, value, middle_id)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新中介字段" + field + "失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    # 以下是终端使用接口-------------------------------------------------------------------------------------------------

    # 验证登录
    def search_admin_login(self, account, password):
        sql = "SELECT id, name FROM admin WHERE BINARY account='{}' AND BINARY password='{}'".format(account, password)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0], rows[0][1]


if __name__ == "__main__":
    s = SqlData()
