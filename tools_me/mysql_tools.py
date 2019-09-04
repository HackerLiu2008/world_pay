import json
import pymysql
import logging
from tools_me.other_tools import is_json


class SqlData(object):
    def __init__(self):
        # host = "rm-j6c3t1i83rgylsuamvo.mysql.rds.aliyuncs.com"
        host = "119.3.251.10"
        port = 3306
        user = "root"
        password = "lx7996"
        database = "buysys"
        self.connect = pymysql.Connect(
            host=host, port=port, user=user,
            passwd=password, db=database,
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    def account_to_dict(self, all_info):
        detail_list = list()
        for i in all_info:
            detail_dict = dict()
            # detail_dict["id"] = i[0]
            detail_dict["account"] = i[2]
            detail_dict["password"] = i[3]
            detail_dict["email"] = i[4]
            detail_dict["email_pw"] = i[5]
            detail_dict["pay_money"] = i[6]
            detail_dict["pay_num"] = i[7]
            detail_dict["reg_time"] = str(i[9])
            detail_dict["label"] = i[10]
            detail_dict['terrace'] = i[11]
            detail_dict["country"] = i[12]
            detail_dict["member_state"] = i[13]
            detail_dict["buy_state"] = i[14]
            detail_dict["note"] = i[16]
            detail_list.append(detail_dict)
        return detail_list

    def on_order_to_dict(self, all_info):
        detail_list = list()
        for i in all_info:
            detail_dict = dict()
            detail_dict["id"] = i[0]
            detail_dict['task_id'] = i[1]
            detail_dict["terrace"] = i[3]
            detail_dict["country"] = i[4]
            detail_dict["pay_method"] = i[5]
            detail_dict["store"] = i[6]
            detail_dict["asin"] = i[9]
            detail_list.append(detail_dict)
        return detail_list

    def account_action_detail(self, all_info):
        detail_list = list()
        for i in all_info:
            detail_dict = dict()
            detail_dict["id"] = i[0]
            detail_dict["account"] = i[1]
            detail_dict["goods"] = i[2]
            detail_dict["stores"] = i[3]
            detail_dict["member_time"] = i[4]
            detail_dict["first_buy_time"] = str(i[5])
            detail_dict["last_buy_time"] = str(i[6])
            detail_list.append(detail_dict)
        return detail_list

    def task_info_to_list(self, info, user_id):
        detail_list = list()
        for i in info:
            detail_dict = dict()
            detail_dict["sum_order_code"] = i[0]
            detail_dict["terrace"] = i[1]
            detail_dict["sum_num"] = i[2]
            detail_dict["serve_money"] = i[4]
            detail_dict["all_money"] = i[3]
            detail_dict["deal_num"] = i[5]
            detail_dict["customer_label"] = i[6]
            detail_dict["sum_time"] = str(i[7])
            detail_dict["sum_state"] = i[8]
            detail_dict["note"] = i[9]
            detail_dict["sum_money"] = i[10]
            detail_dict["pay_cus"] = i[11]
            detail_dict["pay_middle"] = i[12]
            detail_dict['task_plan'] = self.task_plan(i[0])
            detail_list.append(detail_dict)
        return detail_list

    def task_info_middle_list(self, info, user_id):
        detail_list = list()
        for i in info:
            detail_dict = dict()
            detail_dict["sum_order_code"] = i[0]
            detail_dict["terrace"] = i[1]
            detail_dict["sum_num"] = i[2]
            detail_dict["serve_money"] = i[4]
            detail_dict["all_money"] = i[3]
            detail_dict["deal_num"] = i[5]
            detail_dict["customer_label"] = i[6]
            detail_dict["sum_time"] = str(i[7])
            detail_dict["sum_state"] = i[8]
            detail_dict["note"] = i[9]
            detail_dict["sum_money"] = i[10]
            detail_dict["pay_cus"] = i[11]
            detail_dict["pay_middle"] = i[12]
            detail_dict["middle_money"] = i[13]
            detail_dict['task_plan'] = self.task_plan(i[0])
            detail_list.append(detail_dict)
        return detail_list

    def task_detail_list(self, info):
        detail_list = list()
        for i in info:
            detail_dict = dict()
            detail_dict['task_code'] = i[2]
            detail_dict['country'] = i[3]
            detail_dict['asin'] = i[4]
            detail_dict['key_word'] = i[5]
            detail_dict['kw_location'] = i[6]
            detail_dict['store_name'] = i[7]
            detail_dict['good_name'] = i[8]
            detail_dict['good_money'] = i[9]
            detail_dict['good_link'] = i[10]
            detail_dict['mail_method'] = i[11]
            detail_dict['pay_method'] = i[12]
            detail_dict['serve_class'] = i[13]
            detail_dict['buy_account'] = i[14]
            detail_dict['account_ps'] = i[15]
            detail_dict['task_run_time'] = str(i[16])
            detail_dict['task_state'] = i[17]
            detail_dict['brush_hand'] = i[18]
            detail_dict['note'] = i[24]
            detail_dict['review_title'] = i[25]
            if is_json(i[26]):
                link_dict = json.loads(i[26])
                key_list = list(link_dict.keys())
                s = ''
                for n in key_list:
                    s += n
                detail_dict['review_info'] = s
            else:
                detail_dict['review_info'] = i[26]
            detail_dict['feedback_info'] = i[27]
            detail_dict['urgent'] = i[30]
            detail_list.append(detail_dict)
        return detail_list

    def orders_to_dict(self, info):
        order_list = list()
        for i in info:
            order_data = dict()
            order_data['task_code'] = i[2]
            order_data['country'] = i[3]
            order_data['asin'] = i[4]
            order_data['key_word'] = i[5]
            order_data['kw_location'] = i[6]
            order_data['store_name'] = i[7]
            order_data['good_name'] = i[8]
            order_data['good_money'] = i[9]
            order_data['good_link'] = i[10]
            order_data['mail_method'] = i[11]
            order_data['pay_method'] = i[12]
            order_data['serve_class'] = i[13]
            order_data['buy_account'] = i[14]
            order_data['account_ps'] = i[15]
            order_data['task_run_time'] = str(i[16])
            order_data['task_state'] = i[17]
            order_data['brush_hand'] = i[18]
            order_data['note'] = i[24]
            order_data['review_title'] = i[25]
            if is_json(i[26]):
                link_dict = json.loads(i[26])
                key_list = list(link_dict.keys())
                s = ''
                for n in key_list:
                    s += n
                order_data['review_info'] = s
            else:
                order_data['review_info'] = i[26]
            order_data['feedback_info'] = i[27]
            order_data['urgent'] = i[30]
            order_data['customer_label'] = i[31]
            order_list.append(order_data)
        return order_list

    # 获取账号行为信息
    def search_account_action(self, buy_state, terrace, country, user_id):
        sql = "SELECT account_action.* FROM account_action LEFT JOIN account_info ON account_action.account_id=account" \
              "_info.id LEFT JOIN user_info ON user_info.id = account_info.user_id WHERE account_info.buy_state = '{}' " \
              "and account_info.terrace = '{}' and account_info.country = '{}' and user_info.id={}".format(buy_state,
                                                                                                           terrace,
                                                                                                           country,
                                                                                                           user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        action_list = list()
        for i in rows:
            action_data = dict()
            action_data['account_id'] = i[1]
            action_data['goods'] = i[2]
            action_data['stores'] = i[3]
            action_data['member_time'] = i[4]
            action_data['first_buy_time'] = i[5]
            action_data['last_buy_time'] = i[6]
            action_list.append(action_data)
        return action_list

    # 按数量查询账号信息
    def search_detail_account(self, num):
        sql = "SELECT * FROM account_info WHERE buy_state = '' limit  {}".format(num)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        detail_list = self.account_to_dict(rows)
        return detail_list

    # 查询所有账号标签
    def search_account_label(self, user_id):
        sql = "SELECT label FROM account_info WHERE user_id = {}".format(user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        label_list = list()
        for row in rows:
            label_list.append(row[0].strip())
        return label_list

    # 查询所有订单客户标签
    def search_task_all_label(self, user_id):
        sql = "SELECT customer_label FROM task_parent WHERE user_id = {}".format(user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        label_list = list()
        for row in rows:
            label_list.append(row[0].strip())
        return label_list

    # 查询没有分配账号的订单的信息
    def search_on_order(self, num):
        sql = "SELECT * FROM task_detail_info WHERE task_state = '' limit  {}".format(num)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        detail_list = self.on_order_to_dict(rows)
        return detail_list

    def search_task_store(self, task_code):
        sql = "SELECT store_name FROM task_detail_info WHERE task_code = '{}'".format(task_code)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def search_action_store(self, account):
        sql = "SELECT stores FROM account_action WHERE account = '{}'".format(account)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def search_account(self, user_id):
        sql = 'SELECT * FROM account_info WHERE user_id = {}'.format(user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info = self.account_to_dict(rows)
        return info

    def search_account_ing(self, field, buy_state, user_id):
        sql = "SELECT * FROM account_info WHERE {}='{}' AND user_id = {}".format(field, buy_state, user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info = self.account_to_dict(rows)
        return info

    # 根据不同条件查询账号信息
    def search_account_sql(self, sql, user_id):
        sql = "SELECT * FROM account_info WHERE user_id = {} {}".format(user_id, sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info = self.account_to_dict(rows)
        return info

    def search_task_parent(self, user_id):
        sql = "SELECT sum_order_code, terrace, sum_num, sum_money, serve_money, deal_num, " \
              "customer_label, sum_time, sum_state, note, good_money,pay_cus, pay_middle FROM task_parent WHERE user_id = {}".format(user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        task_list = self.task_info_to_list(rows, user_id)
        return task_list

    def search_task_on_asin(self, user_id, sum_code_sql='', label_sql='', asin_sql=''):
        sql = "SELECT sum_order_code FROM task_parent LEFT JOIN task_detail_info ON task_parent.id = task_detail_info." \
              "parent_id WHERE task_parent.user_id={} {} {} {}".format(user_id, sum_code_sql, label_sql, asin_sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        sum_code_list = list()
        for i in rows:
            sum_code_list.append(i[0])
        new_list = list(set(sum_code_list))
        result_list = list()
        for i in new_list:
            result = self.search_task_on_code('sum_order_code', i, user_id)
            result_list.append(result[0])
        return result_list

    def search_task_on_code(self, field, value, user_id):
        sql = "SELECT sum_order_code, terrace, sum_num, sum_money, serve_money, deal_num, " \
              "customer_label, sum_time, sum_state, note, good_money, pay_cus, pay_middle FROM task_parent WHERE {} = '{}' AND " \
              "user_id = {}".format(field, value, user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        task_list = self.task_info_to_list(rows, user_id)
        return task_list

    def search_order_one(self, field, value):
        sql = "SELECT {} FROM task_detail_info WHERE task_code = '{}' ".format(field, value)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def search_task_detail(self, sum_order_code, state_sql=''):
        sql = "SELECT task_detail_info.* FROM task_detail_info LEFT JOIN task_parent ON task_detail_info.parent_id = " \
              "task_parent.id  WHERE task_parent.sum_order_code = '{}' {}".format(sum_order_code, state_sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        results = self.task_detail_list(rows)
        return results

    #  按条件搜索小订单
    def search_task_field(self, user_id, label, state_sql=''):
        sql = "SELECT task_detail_info.* FROM task_detail_info LEFT JOIN task_parent ON task_detail_info.parent_id = " \
              "task_parent.id  WHERE task_parent.user_id = {} AND task_parent.customer_label='{}' {}".format(user_id, label, state_sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        results = self.task_detail_list(rows)
        return results

    # 根据订单号查某一个字段
    def search_task_one_field(self, field, sum_order_code):
        sql = "SELECT {} FROM task_parent WHERE sum_order_code='{}'".format(field, sum_order_code)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def search_one_task(self, task_code):
        sql = "SELECT asin, store_name FROM task_detail_info WHERE task_code = '{}'".format(task_code)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0], rows[0][1]

    def search_customer_login(self, main_user, account, password):
        sql = "SELECT * FROM customer_info LEFT JOIN user_info ON user_info.id = customer_info.user_id WHERE " \
              "user_info.user_name='{}' AND customer_info.account='{}' AND customer_info.pass_word='{}'"\
               .format(main_user, account, password)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def search_review_pic(self, task_code):
        sql = "SELECT pic_link FROM task_detail_info WHERE task_code='{}'".format(task_code)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def update_review_one(self, field, value, task_code):
        sql = "UPDATE task_detail_info SET {}='{}' WHERE task_code='{}'".format(field, value, task_code)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新客户标签失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def search_account_ps(self, account):
        sql = "SELECT password FROM account_info WHERE account = '{}'".format(account)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    # 查询账号的asin, store, first_buy_time
    def search_asin_store(self, account):
        sql = "SELECT goods, stores, first_buy_time FROM account_action LEFT JOIN account_info ON account_action." \
              "account_id = account_info.id WHERE account='{}'".format(account)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        row = rows[0]
        return row[0], row[1], row[2]

    # 查询用户标签所有信息
    def search_customer_detail(self, user_id):
        sql = "SELECT * FROM customer_info WHERE user_id={}".format(user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        list_info = list()
        for i in rows:
            detail_dict = dict()
            detail_dict['标签'] = i[2]
            detail_dict['账号'] = i[3]
            detail_dict['密码'] = i[4]
            detail_dict['折扣'] = i[5]
            detail_dict['备注'] = i[6]
            list_info.append(detail_dict)
        return list_info

    # 查询用户标签
    def search_user_cus(self, user_id):
        sql = "SELECT label FROM customer_info WHERE user_id={}".format(user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        label_list = list()
        for i in rows:
            label_list.append(i[0])
        return label_list

    # 查询主账号下的所有用户信息
    def search_cus_all(self, user_id, sql=''):
        sql = "SELECT * FROM customer_info WHERE user_id={} {}".format(user_id, sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info_list = list()
        for i in rows:
            info_dict = dict()
            info_dict['label'] = i[2]
            info_dict['account'] = i[3]
            info_dict['password'] = i[4]
            info_dict['amz_money'] = i[9]
            info_dict['note'] = i[6]
            info_list.append(info_dict)
        return info_list

    def search_cus_field(self, field, cus_id):
        sql = "SELECT {} FROM customer_info WHERE id={}".format(field, cus_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def search_cus_one_field(self, field, user_id, label):
        sql = "SELECT {} FROM customer_info WHERE user_id={} AND label='{}'".format(field, user_id, label)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    # 按标签查询客户信息
    def search_cus_of_label(self, field, user_id, sql=""):
        sql = "SELECT {} FROM customer_info WHERE user_id={} {}".format(field, user_id, sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def update_user_cus(self, field, value, user_id, label):
        sql = "UPDATE customer_info SET {}='{}' WHERE user_id={} AND label='{}'".format(field, value, user_id, label)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新客户标签失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def insert_user_cus(self, label, account, password, note, user_id):
        sql = "INSERT INTO customer_info(label, account, pass_word, note, user_id) VALUES('{}','{}','{}'," \
              "'{}',{})".format(label, account, password, note, user_id)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("插入客户标签行为失败" + str(e))
            self.connect.rollback()
        self.close_connect()

    def search_detail_order(self, account_id, label='', account='', pay_money=''):
        sql = "SELECT account_info.account,account_info.pay_money,account_info.pay_num,account_info.review_num," \
              "account_info.label,account_info.member_state,account_info.account_state,account_info.reg_time," \
              "account_action.last_buy_time FROM account_info LEFT JOIN account_action ON account_info.id=" \
              "account_action.account_id WHERE account_info.id = {} AND account_info.buy_state='' {} {} {}".\
               format(account_id, label, account, pay_money)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        # print(len(rows))
        if len(rows) == 0:
            return 'F'
        else:
            data = dict()
            row = rows[0]
            data['account'] = row[0]
            data['pay_money'] = row[1]
            data['pay_num'] = row[2]
            data['review_num'] = row[3]
            data['label'] = row[4]
            data['member_state'] = row[5]
            data['account_state'] = row[6]
            data['reg_time'] = str(row[7])
            data['last_buy_time'] = str(row[8])
            return data

    # 更新帐号是否有做过购买
    def update_account_state_one(self, buy_state, account):
        sql = "UPDATE account_info SET buy_state= '{}' WHERE account ='{}'".format(buy_state, account)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新是否已购买状态失败" + str(e))
            self.connect.rollback()
        self.close_connect()

    # 更新帐号的莫一条信息
    def update_account_one(self, field, value, account, user_id):
        sql = "UPDATE account_info SET {}= '{}' WHERE account ='{}' AND user_id={}".format(field, value, account,
                                                                                           user_id)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新是否已购买状态失败" + str(e))
            self.connect.rollback()
        self.close_connect()

    # 更新下单后要跟新账号信息和账号行为(没有第一次下单时间)
    def update_account_no_time(self, pay_money, goods, stores, first_buy_time, last_buy_time, account_state, account):
        sql = "UPDATE account_info LEFT JOIN account_action ON account_info.id=account_action.account_id SET " \
              "pay_money=pay_money+{},pay_num=pay_num+1,buy_state='',account_action.goods='{}',account_action.stores" \
              "='{}',account_action.first_buy_time='{}',account_action.last_buy_time='{}'{} WHERE account ='{}'".format(
            pay_money, goods, stores, first_buy_time, last_buy_time, account_state, account)

        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新是否已购买状态失败" + str(e))
            self.connect.rollback()
        self.close_connect()

    # 有第一次下单时间
    def update_account_have_time(self, pay_money, goods, stores, last_buy_time, account_state, account):
        sql = "UPDATE account_info LEFT JOIN account_action ON account_info.id=account_action.account_id SET " \
              "pay_money=pay_money+{},pay_num=pay_num+1,buy_state='',account_action.goods='{}',account_action.stores" \
              "='{}',account_action.last_buy_time='{}'{} WHERE account ='{}'".format(
            pay_money, goods, stores, last_buy_time, account_state, account)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新是否已购买状态失败" + str(e))
            self.connect.rollback()
        self.close_connect()

    # 更新下单后的信息
    def update_payed(self, order_num, good_money_real, mail_money, taxes_money, note, sum_money, task_code, task_state):
        sql = "UPDATE task_detail_info SET order_num='{}',good_money_real={},mail_money={},taxes_money={}," \
              "note='{}', sum_money={},task_state='{}' WHERE task_code='{}'".format(order_num, good_money_real,
                                                                                    mail_money, taxes_money, note,
                                                                                    sum_money, task_state, task_code)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error(str(e))
            self.connect.rollback()
        self.close_connect()

    def update_order_account(self, account, password, order_state, task_code):
        sql = "UPDATE task_detail_info SET buy_account='{}',account_ps='{}',task_state='{}' WHERE task_code='{}'". \
            format(account, password, order_state, task_code)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error(str(e))
            self.connect.rollback()
        self.close_connect()

    def search_user_info(self, user_name):
        sql = "SELECT id, pass_word, expire_time, us_time, terrace FROM user_info WHERE user_name = '{}'".format(user_name)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        try:
            user_data = dict()
            user_data['user_id'] = rows[0][0]
            user_data['pass_word'] = rows[0][1]
            user_data['expire_time'] = rows[0][2]
            user_data['us_time'] = rows[0][3]
            user_data['terrace'] = rows[0][4]
            return user_data
        except Exception as e:
            logging.error(str(e))
            return '账号或密码错误!'

    def search_account_detail(self, account, user_id):
        sql = "SELECT * FROM account_info LEFT JOIN address_card_info ON account_info.id = address_card_info.account_" \
              "id LEFT JOIN account_action ON account_info.id = account_action.account_id WHERE account_info.account=" \
              "'{}' AND account_info.user_id ={}".format(account, user_id)

        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        row = rows[0]
        account_data = dict()
        account_data['account'] = row[2]
        account_data['password'] = row[3]
        account_data['email'] = row[4]
        account_data['email_pw'] = row[5]
        account_data['pay_money'] = row[6]
        account_data['pay_num'] = row[7]
        account_data['review_num'] = row[8]
        account_data['reg_time'] = row[9]
        account_data['label'] = row[10]
        account_data['terrace'] = row[11]
        account_data['country'] = row[12]
        account_data['member_state'] = row[13]
        account_data['buy_state'] = row[14]
        account_data['account_state'] = row[15]
        account_data['note'] = row[16]
        account_data['full_name'] = row[19]
        account_data['phone_num'] = row[20]
        account_data['coun'] = row[21]
        account_data['province'] = row[22]
        account_data['city'] = row[23]
        account_data['zip_num'] = row[24]
        account_data['detail_address'] = row[25]
        account_data['card_num'] = row[26]
        account_data['sizeof'] = str(row[27])
        account_data['security_code'] = row[28]
        account_data['goods'] = row[31]
        account_data['stores'] = row[32]
        account_data['member_time'] = str(row[33])
        account_data['first_buy_time'] = str(row[34])
        account_data['last_buy_time'] = str(row[35])
        return account_data

    def search_user_field(self, field, user_id):
        sql = "SELECT {} FROM user_info WHERE id ={}".format(field, user_id)
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        return row[0][0]

    def search_order_task_code(self, task_code):
        sql = "SELECT * FROM task_detail_info WHERE task_code='{}'".format(task_code)
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        return row[0]

    def search_now_order(self, t1, t2, user_id):
        sql = "SELECT task_detail_info.*, task_parent.customer_label FROM task_detail_info LEFT JOIN task_parent ON task_detail_info.parent_id=" \
              "task_parent.id LEFT JOIN user_info ON user_info.id = task_parent.user_id WHERE task_run_time BETWEEN " \
              "'{}' and '{}' AND user_info.id = {} AND task_detail_info.task_state = '' AND task_parent.pay_cus != ''".format(t1, t2, user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        now_order_list = self.orders_to_dict(rows)
        return now_order_list

    def search_all_order(self, user_id, task_sql='', asin_sql='', order_num=''):
        sql = "SELECT task_detail_info.*, task_parent.customer_label FROM task_detail_info LEFT JOIN task_parent ON task_detail_info.parent_id=" \
              "task_parent.id LEFT JOIN user_info ON user_info.id = task_parent.user_id WHERE user_info.id = {} {}" \
              " {} {}".format(user_id, task_sql, asin_sql, order_num)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        now_order_list = self.orders_to_dict(rows)
        return now_order_list

    def search_order_of_state(self, buy_state, user_id):
        sql = "SELECT task_detail_info.*, task_parent.customer_label FROM task_detail_info LEFT JOIN task_parent ON task_detail_info.parent_id=" \
              "task_parent.id LEFT JOIN user_info ON user_info.id = task_parent.user_id WHERE user_info.id = {} AND " \
              "task_detail_info.task_state = '{}' AND task_parent.pay_cus != ''".format(user_id, buy_state)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        now_order_list = self.orders_to_dict(rows)
        return now_order_list

    def search_order_of_overdue(self, t, user_id):
        sql = "SELECT task_detail_info.*, task_parent.customer_label FROM task_detail_info LEFT JOIN task_parent ON task_detail_info.parent_id=" \
              "task_parent.id LEFT JOIN user_info ON user_info.id = task_parent.user_id WHERE task_run_time < '{}' AND " \
              "user_info.id = {} AND task_detail_info.task_state = '' AND task_parent.pay_cus != ''"\
               .format(t, user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        now_order_list = self.orders_to_dict(rows)
        return now_order_list

    def update_user_field(self, field, value, user_id):
        sql = "UPDATE user_info SET {} = {} WHERE id = {}".format(field, value, user_id)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error(str(e))
            self.connect.rollback()
        self.close_connect()

    # 更新订单时间
    def update_order_time(self, run_time, task_code):
        sql = "UPDATE task_detail_info SET task_run_time='{}' WHERE task_code='{}'".format(run_time, task_code)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error(str(e))
            self.connect.rollback()
        self.close_connect()

    # 跟新详细订单的一个字段
    def update_order_repair(self, value, task_code):
        sql = "UPDATE task_detail_info SET buy_account='',account_ps='',task_run_time='{}',task_state=''," \
              "order_num='',good_money_real=0,mail_money=0,taxes_money=0,sum_money=0 WHERE task_code='{}'".\
               format(value, task_code)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error(str(e))
            self.connect.rollback()
        self.close_connect()

    def update_order_state(self, task_code):
        sql = "UPDATE task_detail_info SET task_state='已取消' WHERE task_code='{}'".format(task_code)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error(str(e))
            self.connect.rollback()
        self.close_connect()

    # 更新分配状态,买家号到订单表格
    def update_task_info(self, task_state, buy_account, task_id):
        sql = "UPDATE task_detail_info SET task_state = '{}', buy_account = '{}' WHERE id ='{}'".format(task_state,
                                                                                                        buy_account,
                                                                                                        task_id)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新订单信息失败" + str(e))
            self.connect.rollback()
        self.close_connect()

    def update_task_user(self, sum_state, note, key_word, sum_order_code):
        sql = "UPDATE task_detail_info LEFT JOIN task_parent ON task_detail_info.parent_id=task_parent.id SET " \
              "sum_state = '{}', task_parent.note='{}',task_detail_info.key_word='{}' WHERE task_parent.sum_order_co" \
              "de ='{}'".format(sum_state, note, key_word, sum_order_code)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新订单信息失败" + str(e))
            self.connect.rollback()
        self.close_connect()

    # 更新data_time时间参数到数据库的方法
    def update_data_time(self, account, data_time):
        sql = "UPDATE account_action SET last_buy_time='{}' WHERE account='{}';".format(data_time, account)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新data_time失败" + str(e))
            self.connect.rollback()
        self.close_connect()

    # 更新用户行为到行为信息表
    def update_action(self, goods, stores, first_buy_time, last_buy_time, account_id):
        sql = "UPDATE account_action SET goods='{}', stores='{}', first_buy_time='{}', last_buy_time='{}' " \
              "WHERE account_id='{}';".format(goods, stores, first_buy_time, last_buy_time, account_id)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新账号行为失败" + str(e))
            self.connect.rollback()
        self.close_connect()

    def update_account(self, password, label, terrace, country, member, note, account):
        sql = "UPDATE account_info SET password='{}', label='{}', terrace='{}', country='{}', member_state='{}', note='{}' " \
              "WHERE account='{}';".format(password, label, terrace, country, member, note, account)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新账号行为失败" + str(e))
            self.connect.rollback()
        self.close_connect()

    def update_task_detail(self, run_time, serve_class, brush_hand, note, task_code):
        sql = "UPDATE task_detail_info SET task_run_time='{}', serve_class='{}', brush_hand='{}', note='{}' WHERE task_code='{}';". \
            format(run_time, serve_class, brush_hand, note, task_code)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新订单时间失败" + str(e))
            self.connect.rollback()
        self.close_connect()

    def update_user_info(self, pass_word, user_id):
        sql = "UPDATE user_info SET pass_word = '{}' WHERE id={}".format(pass_word, user_id)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error(str(e))
            self.connect.rollback()
        self.close_connect()

    # 更新一个字段的task_parent 表
    def update_task_one(self, field, value, sum_order_code):
        sql = "UPDATE task_parent SET {} = '{}' WHERE sum_order_code='{}'".format(field, value, sum_order_code)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error(str(e))
            self.connect.rollback()
        self.close_connect()

    def del_account(self, account, user_id):
        sql = "DELETE FROM account_info WHERE account = '{}' AND user_id = {}".format(account, user_id)
        self.cursor.execute(sql)
        self.connect.commit()
        self.close_connect()

    def del_task(self, sum_order_code, user_id):
        sql = "DELETE FROM task_parent WHERE sum_order_code = '{}' AND user_id = {}".format(sum_order_code, user_id)
        self.cursor.execute(sql)
        self.connect.commit()
        self.close_connect()

    def insert_account_detail(self, user_id, account, password, email, email_pw, pay_money, reg_time, label, terrace,
                              country,
                              member_state, full_name, phone_num, coun, province, city, zip_num, detail_address,
                              card_num, sizeof, security_code):

        sql = "INSERT INTO account_info(user_id, account, password, email, email_pw, pay_money, reg_time, label, " \
              "terrace, country, member_state) VALUES ({},'{}','{}','{}','{}',{},'{}','{}','{}','{}','{}')".format(
            user_id, account,
            password,
            email, email_pw,
            pay_money,
            reg_time,
            label, terrace,
            country,
            member_state)

        try:
            self.cursor.execute(sql)
            self.connect.commit()
            last_id = self.search_last_id('account_info')
            sql = "INSERT INTO address_card_info(account_id,full_name,phone_num,country,province,city,zip_num," \
                  "detail_address,card_num,sizeof,security_code) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}'," \
                  "'{}','{}','{}')".format(last_id, full_name, phone_num, coun, province, city, zip_num, detail_address,
                                           card_num, sizeof, security_code)
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("插入买家账号行为失败" + str(e))
            self.connect.rollback()
        self.close_connect()

    def insert_task_parent(self, user_id, sum_order_code):
        sql_parent = "INSERT INTO task_parent(user_id, sum_order_code) VALUES ('{}','{}')". \
            format(user_id, sum_order_code)
        # print(sql_parent)
        try:
            self.cursor.execute(sql_parent)
            self.connect.commit()
            last_id = self.search_last_id('task_parent')
            return last_id

        except Exception as e:
            logging.error("插入任务订单行为失败" + str(e))
            self.connect.rollback()
        self.close_connect()

    def insert_task_detail(self, parent_id, task_code, country, asin, key_word, kw_location, store_name, good_name,
                           good_money, good_link, pay_method, task_run_time, serve_class, mail_method, note,
                           review_title, review_info, feedback_info):
        sql = "INSERT INTO task_detail_info(parent_id,task_code,country,asin,key_word,kw_location,store_name," \
              "good_name,good_money,good_link,pay_method,task_run_time, serve_class, mail_method, note, review_title, " \
              "review_info, feedback_info) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}'," \
              "'{}',\"{}\",\"{}\",\"{}\",\"{}\")".format(parent_id, task_code, country, asin, key_word, kw_location, store_name,
                                                 good_name, good_money, good_link, pay_method, task_run_time,
                                                 serve_class, mail_method, note, review_title, review_info,
                                                 feedback_info)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("插入任务订单行为失败" + str(e))
            self.connect.rollback()
        self.close_connect()

    def search_last_id(self, table_name):
        sql = "select id from {} order by id DESC limit 1".format(table_name)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def search_finish_order(self, sum_order_code, sql=''):
        sql = "SELECT COUNT(*) FROM task_detail_info WHERE task_code LIKE '%{}%' {}".format(sum_order_code, sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def task_plan(self, sum_order_code):
        sql = "AND task_state != '' AND task_state != '已分配'"
        complete = self.search_finish_order(sum_order_code)
        finish = self.search_finish_order(sum_order_code, sql=sql)
        results1 = int(finish) / int(complete)
        results2 = results1 * 100
        results = "%.2f%%" % results2
        return results

    def close_connect(self):
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()

    def search_middle_login(self, main_user, account, password):
        sql = "SELECT * FROM middle_info LEFT JOIN user_info ON user_info.id = middle_info.user_id WHERE " \
              "user_info.user_name='{}' AND middle_info.account='{}' AND middle_info.password='{}'" \
            .format(main_user, account, password)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    # 查询所有中介的信息
    def search_middle_field(self, field, user_id):
        sql = "SELECT {} FROM  middle_info WHERE user_id={}".format(field, user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    # 查询一个中介的信息
    def search_one_middle_field(self, field, user_id, name):
        sql = "SELECT {} FROM  middle_info WHERE user_id={} AND name='{}'".format(field, user_id, name)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def search_of_middle_id(self, field, middle_id):
        sql = "SELECT {} FROM  middle_info WHERE id={}".format(field, middle_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def insert_middle(self, user_id, name, account, password, discount):
        sql_parent = "INSERT INTO middle_info(user_id, name, account, password, discount) VALUES ({},'{}','{}','{}',{})". \
            format(user_id, name, account, password, discount)
        try:
            self.cursor.execute(sql_parent)
            self.connect.commit()

        except Exception as e:
            logging.error("插入任务订单行为失败" + str(e))
            self.connect.rollback()
        self.close_connect()

    # 跟新数字类型
    def update_middle_dis(self, field, value, name, user_id):
        sql = "UPDATE middle_info SET {}={} WHERE user_id={} AND name='{}'".format(field, value, user_id, name)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error(str(e))
            self.connect.rollback()
        self.close_connect()

    # 更新字符串类型
    def update_middle_field(self, field, value, name, user_id):
        sql = "UPDATE middle_info SET {}='{}' WHERE user_id={} AND name='{}'".format(field, value, user_id, name)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error(str(e))
            self.connect.rollback()
        self.close_connect()

    def del_middle(self, name, user_id):
        sql = "DELETE FROM middle_info WHERE name='{}'AND user_id={}".format(name, user_id)
        self.cursor.execute(sql)
        self.connect.commit()
        self.close_connect()

    def search_task_on_middle(self, middle_id, user_id):
        sql = "SELECT sum_order_code, terrace, sum_num, sum_money, serve_money, deal_num, customer_label, sum_time, " \
              "sum_state, task_parent.note, good_money, pay_cus, pay_middle, middle_money FROM task_parent LEFT JOIN customer_info ON task_parent.cust" \
              "omer_label=customer_info.label WHERE customer_info.middle_id = '{}' AND " \
              "task_parent.user_id = {} AND task_parent.pay_cus='已支付'".format(middle_id, user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        task_list = self.task_info_middle_list(rows, user_id)
        return task_list


if __name__ == "__main__":
    s = SqlData()
