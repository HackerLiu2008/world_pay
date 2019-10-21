import pymysql
import logging


class SqlData(object):
    def __init__(self):
        host = "114.116.236.27"
        # host = "127.0.0.1"
        port = 3306
        user = "root"
        password = "gute123"
        # password = "admin"
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
        sql = "SELECT create_price, refund, min_top, max_top, balance, sum_balance FROM account WHERE id = {}".format(user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        user_info = dict()
        user_info['create_card'] = rows[0][0]
        user_info['refund'] = rows[0][1]
        user_info['min_top'] = rows[0][2]
        user_info['max_top'] = rows[0][3]
        user_info['balance'] = rows[0][4]
        user_info['sum_balance'] = rows[0][5]
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

    def update_user_field_int(self, field, value, user_id):
        sql = "UPDATE account SET {} = {} WHERE id = {}".format(field, value, user_id)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新用户字段" + field + "失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def update_user_bala(self, field, value, user_id):
        sql = "UPDATE account SET {} = {} WHERE id = {}".format(field, value, user_id)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新用户字段" + field + "失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def search_top_history_acc(self, user_id):
        sql = "SELECT * FROM top_up WHERE account_id={}".format(user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info_list = list()
        if not rows:
            return info_list
        else:
            for i in rows:
                info_dict = dict()
                info_dict['pay_num'] = i[1]
                info_dict['time'] = str(i[2])
                info_dict['money'] = i[3]
                info_dict['before_balance'] = i[4]
                info_dict['balance'] = i[5]
                info_list.append(info_dict)
            return info_list

    def search_activation(self):
        sql = "SELECT activation from card_info WHERE card_no is null AND card_name = '' AND account_id is null LIMIT 1"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if not rows:
            return False
        return rows[0][0]

    def search_activation_count(self):
        sql = "SELECT COUNT(activation) from card_info WHERE card_no is null AND account_id is null AND card_name = ''"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if not rows:
            return False
        return rows[0][0]

    def update_card_info_field(self, field, value, activation):
        sql = "UPDATE card_info SET {}='{}' WHERE activation='{}'".format(field, value, activation)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新卡信息失败!")
            self.connect.rollback()
        self.close_connect()

    def search_card_field(self, field, crad_no):
        sql = "SELECT {} from card_info WHERE card_no='{}'".format(field, crad_no)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if not rows:
            return False
        return rows[0][0]

    def update_card_info(self, card_no, pay_passwd, act_time, card_name, label, expire, cvv, account_id, activation):
        sql = "UPDATE card_info SET card_no = '{}', pay_passwd='{}', act_time='{}', card_name='{}', label='{}', expire = '{}'," \
              " cvv = '{}', account_id = {} WHERE activation = '{}'".format(card_no, pay_passwd, act_time, card_name, label,
                                                                            expire, cvv, account_id, activation)

        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新卡信息失败!")
            self.connect.rollback()
        self.close_connect()

    def search_card_info(self, user_id):
        sql = "SELECT * FROM card_info WHERE account_id={}".format(user_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info_list = list()
        if not rows:
            return info_list
        else:
            for i in rows:
                info_dict = dict()
                info_dict['card_no'] = "\t" + i[2]
                info_dict['act_time'] = str(i[4])
                info_dict['card_name'] = i[5]
                info_dict['label'] = i[6]
                expire = i[7]
                if expire:
                    info_dict['expire'] = expire[4:6] + "/" + expire[2:4]
                else:
                    info_dict['expire'] = ""
                info_dict['cvv'] = "\t" + i[8]
                info_list.append(info_dict)
            return info_list

    def search_card_select(self, user_id, name_sql, card_sql, label, time_sql):
        sql = "SELECT * FROM card_info WHERE account_id={} {} {} {} {}".format(user_id, name_sql, card_sql, label, time_sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info_list = list()
        if not rows:
            return info_list
        else:
            for i in rows:
                info_dict = dict()
                info_dict['card_no'] = "\t" + i[2]
                info_dict['act_time'] = str(i[4])
                info_dict['card_name'] = i[5]
                info_dict['label'] = i[6]
                expire = i[7]
                if expire:
                    info_dict['expire'] = expire[4:6] + "/" + expire[2:4]
                else:
                    info_dict['expire'] = ""
                info_dict['expire'] = i[7]
                info_dict['cvv'] = "\t" + i[8]
                info_list.append(info_dict)
            return info_list

    def insert_account_trans(self, date, trans_type, do_type, num, card_no, do_money, hand_money, before_balance, balance, account_id):
        sql = "INSERT INTO account_trans(do_date, trans_type, do_type, num, :wq, do_money, hand_money, before_balance," \
              " balance, account_id) VALUES('{}','{}','{}',{},'{}',{},{},{},{},{})".format(date, trans_type, do_type,
                                                num, card_no, do_money, hand_money, before_balance, balance, account_id)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("添加用户交易记录失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def search_account_trans(self, account_id, card_sql, time_sql):
        sql = "SELECT * FROM account_trans WHERE account_id = {} {} {}".format(account_id, card_sql, time_sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info_list = list()
        if not rows:
            return info_list
        for i in rows:
            info_dict = dict()
            info_dict['date'] = str(i[1])
            info_dict['trans_type'] = i[2]
            info_dict['do_type'] = i[3]
            info_dict['num'] = i[4]
            info_dict['card_no'] = "\t" + i[5]
            info_dict['do_money'] = i[6]
            info_dict['hand_money'] = i[7]
            info_dict['before_balance'] = i[8]
            info_dict['balance'] = i[9]
            info_list.append(info_dict)
        return info_list

    def search_trans_sum(self, account_id):
        sql = "SELECT SUM(do_money), SUM(hand_money) FROM account_trans WHERE trans_type='支出' AND account_id={}".format(account_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if not rows[0][0]:
            return 0
        do_money = rows[0][0]
        hand_money = rows[0][1]
        sum_money = do_money + hand_money
        return sum_money

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

    def search_user_field_middle(self, middle_id):
        sql = "SELECT id, name FROM account WHERE middle_id = {}".format(middle_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        account_list = list()
        if not rows:
            return account_list
        for i in rows:
            info_dict = dict()
            info_dict['id'] = i[0]
            info_dict['name'] = i[1]
            account_list.append(info_dict)
        return account_list

    def search_user_middle_info(self, middle_id):
        sql = "SELECT id, name, sum_balance, balance FROM account WHERE middle_id = {}".format(middle_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        account_list = list()
        if not rows:
            return account_list
        for i in rows:
            info_dict = dict()
            info_dict['id'] = i[0]
            info_dict['name'] = i[1]
            info_dict['sum_balance'] = i[2]
            info_dict['balance'] = i[3]
            account_list.append(info_dict)
        return account_list

    def search_card_count(self, account_id, time_range):
        sql = "SELECT COUNT(*) FROM card_info WHERE account_id={} {}".format(account_id, time_range)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def insert_middle_money(self, middle_id, start_time, end_time, card_num, create_price, sum_money, create_time, pay_status, detail):
        sql = "INSERT INTO middle_money(middle_id, start_time, end_time, card_num, create_price, sum_money," \
              " create_time, pay_status, detail) VALUES ({},'{}','{}',{},{},{},'{}','{}','{}')".format(
               middle_id, start_time, end_time, card_num, create_price, sum_money, create_time, pay_status, detail)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("插入中介开卡费记录失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def search_middle_money(self, middle_id):
        sql = "SELECT * FROM middle_money WHERE middle_id={}".format(middle_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info_list = list()
        if not rows:
            return info_list
        for i in rows:
            info_dict = dict()
            info_dict['id'] = i[0]
            info_dict['start_time'] = str(i[2])
            info_dict['end_time'] = str(i[3])
            info_dict['card_num'] = i[4]
            info_dict['create_price'] = i[5]
            info_dict['sum_money'] = i[6]
            info_dict['create_time'] = str(i[7])
            info_dict['pay_status'] = i[8]
            if i[9]:
                info_dict['pay_time'] = str(i[9])
            else:
                info_dict['pay_time'] = ""
            info_list.append(info_dict)
        return info_list

    def search_middle_money_field(self, field, info_id):
        sql = "SELECT {} FROM middle_money WHERE id={}".format(field, info_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    # 以下是终端使用接口-------------------------------------------------------------------------------------------------

    # 验证登录
    def search_admin_login(self, account, password):
        sql = "SELECT id, name FROM admin WHERE BINARY account='{}' AND BINARY password='{}'".format(account, password)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0], rows[0][1]

    def search_account_info(self, info):
        sql = "SELECT * FROM account {}".format(info)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        account_list = list()
        if not rows:
            return account_list
        else:
            for i in rows:
                account_dict = dict()
                account_dict['u_id'] = i[0]
                account_dict['account'] = i[1]
                account_dict['password'] = i[2]
                account_dict['name'] = i[4]
                account_dict['create_price'] = i[5]
                account_dict['refund'] = i[6]
                account_dict['min_top'] = i[7]
                account_dict['max_top'] = i[8]
                account_dict['balance'] = i[9]
                account_dict['sum_balance'] = i[10]
                account_list.append(account_dict)
            return account_list

    def update_account_field(self, field, value, name):
        sql = "UPDATE account SET {}={} WHERE name='{}'".format(field, value, name)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新用户字段" + field + "失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def search_user_field_name(self, field, name):
        sql = "SELECT {} FROM account WHERE name = '{}'".format(field, name)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if not rows:
            return False
        return rows[0][0]

    def update_user_balance(self, money, id):
        sql = "UPDATE account set sum_balance=sum_balance+{}, balance=balance+{} WHERE id={}".format(money, money, id)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新用户余额失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def insert_top_up(self, pay_num, now_time, money, before_balance, balance, account_id):
        sql = "INSERT INTO top_up(pay_num, time, money, before_balance, balance, account_id) VALUES ('{}','{}',{},{},{},{})".format(pay_num, now_time, money, before_balance, balance, account_id)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("插入用户充值记录失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def search_top_history(self, sql_line):
        sql = "SELECT * FROM top_up LEFT JOIN account ON account.id=top_up.account_id {}".format(sql_line)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info_list = list()
        if not rows:
            return info_list
        else:
            for i in rows:
                info_dict = dict()
                info_dict['pay_num'] = i[1]
                info_dict['time'] = str(i[2])
                info_dict['money'] = i[3]
                info_dict['before_balance'] = i[4]
                info_dict['balance'] = i[5]
                info_dict['name'] = i[11]
                info_list.append(info_dict)
            return info_list

    def admin_info(self):
        sql = "SELECT account, password, name, balance FROM admin"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0], rows[0][1], rows[0][2], rows[0][3]

    def search_admin_field(self, field):
        sql = "SELECT {} FROM admin".format(field)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def update_admin_field(self, field, value):
        sql = "UPDATE admin SET {}='{}'".format(field, value)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新ADMIN字段失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def insert_account(self, account, password, phone_num, name, create_price, refund, min_top, max_top, note):
        sql = "INSERT INTO account(account, password, phone_num, name, create_price, refund, min_top, max_top, note) " \
              "VALUES ('{}','{}','{}','{}',{},{},{},{},'{}')".format(account, password, phone_num, name, create_price, refund, min_top, max_top, note)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("添加用户失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def search_middle_ed(self, name):
        sql = "SELECT COUNT(*) FROM middle WHERE name ='{}'".format(name)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def insert_middle(self, account, password, name, phone_num, card_price, note):
        sql = "INSERT INTO middle(account, password, name, phone_num, card_price, note) " \
              "VALUES ('{}','{}','{}','{}',{},'{}')".format(account, password, name, phone_num, card_price, note)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("添加中介失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def search_middle_info(self):
        sql = "SELECT * FROM middle"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info_list = list()
        if not rows:
            return info_list
        for i in rows:
            info_dict = dict()
            middle_id = i[0]
            info_dict['cus_num'] = self.search_acc_middle(middle_id)
            info_dict['account'] = i[1]
            info_dict['password'] = i[2]
            info_dict['name'] = i[3]
            info_dict['phone_num'] = i[4]
            info_dict['card_price'] = i[5]
            info_list.append(info_dict)
        return info_list

    def search_acc_middle(self, middle_id):
        sql = "SELECT COUNT(*) FROM account WHERE middle_id={}".format(middle_id)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def search_cus_list(self):
        sql = "SELECT name FROM account"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        cus_list = list()
        if not rows:
            return cus_list
        for i in rows:
            cus_list.append(i[0])
        return cus_list

    def update_middle_field_int(self, field, value, name):
        sql = "UPDATE middle SET {} = {} WHERE name = '{}'".format(field, value, name)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新中介字段" + field + "失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def update_middle_field_str(self, field, value, name):
        sql = "UPDATE middle SET {} = '{}' WHERE name = '{}'".format(field, value, name)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新中介字段" + field + "失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def search_middle_name(self, field, name):
        sql = "SELECT {} FROM middle WHERE name='{}'".format(field, name)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def search_name_info(self):
        sql = "SELECT last_name, female, man FROM name_info"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        last_name = list()
        female = list()
        for i in rows:
            last_name.append(i[0])
            female.append(i[1])
            female.append(i[2])
        info_dict = dict()
        info_dict['last_name'] = last_name
        info_dict['female'] = female
        return info_dict

    def search_middle_id(self):
        sql = "SELECT id FROM middle"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info_list = list()
        if not rows:
            return info_list
        for i in rows:
            info_list.append(i[0])
        return info_list

    def search_user_field_admin(self):
        sql = "SELECT id, name FROM account".format()
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        account_list = list()
        if not rows:
            return account_list
        for i in rows:
            info_dict = dict()
            info_dict['id'] = i[0]
            info_dict['name'] = i[1]
            account_list.append(info_dict)
        return account_list

    def search_middle_money_admin(self):
        sql = "SELECT middle_money.*, middle.`name` FROM middle_money LEFT JOIN middle ON middle.id = middle_money.middle_id"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info_list = list()
        if not rows:
            return info_list
        for i in rows:
            info_dict = dict()
            info_dict['id'] = i[0]
            info_dict['start_time'] = str(i[2])
            info_dict['end_time'] = str(i[3])
            info_dict['card_num'] = i[4]
            info_dict['create_price'] = i[5]
            info_dict['sum_money'] = i[6]
            info_dict['create_time'] = str(i[7])
            info_dict['pay_status'] = i[8]
            if i[9]:
                info_dict['pay_time'] = str(i[9])
            else:
                info_dict['pay_time'] = ""
            info_dict['name'] = i[12]
            info_list.append(info_dict)
        return info_list

    def update_middle_sub(self, pay_status, pay_time, info_id):
        sql = "UPDATE middle_money SET pay_status = '{}', pay_time = '{}' WHERE id = {}".format(pay_status, pay_time, info_id)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("更新中介费确认失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def search_card_info_admin(self, sql_line):
        sql = "SELECT * FROM card_info {}".format(sql_line)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info_list = list()
        for i in rows:
            info_dict = dict()
            info_dict['activation'] = i[1]
            if i[2]:
                info_dict['card_no'] = "\t" + i[2]
            else:
                info_dict['card_no'] = ""
            info_dict['pay_passwd'] = i[3]
            if i[4]:
                info_dict['act_time'] = str(i[4])
            else:
                info_dict['act_time'] = ""
            info_dict['card_name'] = i[5]
            info_dict['label'] = i[6]
            info_dict['expire'] = i[7]
            info_dict['cvv'] = i[8]
            if i[9]:
                name = self.search_user_field('name', i[9])
                info_dict['account_name'] = name
            else:
                info_dict['account_name'] = ""
            info_list.append(info_dict)
        return info_list

    def search_trans_admin(self, cus_sql, card_sql, time_sql, type_sql):
        sql = "SELECT account_trans.*, account.name FROM account_trans LEFT JOIN account ON account_trans.account_id" \
              " = account.id WHERE account_trans.do_date != '' {} {} {} {}".format(cus_sql, card_sql, time_sql, type_sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info_list = list()
        if not rows:
            return info_list
        for i in rows:
            info_dict = dict()
            info_dict['date'] = str(i[1])
            info_dict['trans_type'] = i[2]
            info_dict['do_type'] = i[3]
            info_dict['num'] = i[4]
            info_dict['card_no'] = "\t" + i[5]
            info_dict['do_money'] = i[6]
            info_dict['hand_money'] = i[7]
            info_dict['before_balance'] = i[8]
            info_dict['balance'] = i[9]
            info_dict['cus_name'] = i[11]
            info_list.append(info_dict)
        return info_list

    def search_trans_sum_admin(self):
        sql = "SELECT SUM(do_money), SUM(hand_money) FROM account_trans WHERE trans_type='支出'"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        if not rows[0][0]:
            return 0
        do_money = rows[0][0]
        hand_money = rows[0][1]
        sum_money = do_money + hand_money
        return sum_money

    def search_user_sum_balance(self):
        sql = "SELECT SUM(sum_balance) FROM account"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]

    def insert_account_log(self, n_time, customer, balance, out_money, sum_balance):
        sql = "INSERT INTO account_log(log_time, customer, balance, out_money, sum_balance) VALUES ('{}','{}',{},{},{})".format(n_time, customer, balance, out_money, sum_balance)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            logging.error("添加用户余额记录失败!" + str(e))
            self.connect.rollback()
        self.close_connect()

    def search_account_log(self, cus_sql, time_sql):
        sql = "SELECT * FROM account_log WHERE log_time != '' {} {}".format(cus_sql, time_sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        info_list = list()
        if not rows:
            return info_list
        for i in rows:
            info_dict = dict()
            info_dict['log_time'] = str(i[1])
            info_dict['customer'] = i[2]
            info_dict['balance'] = i[3]
            info_dict['out_money'] = i[4]
            info_dict['sum_balance'] = i[5]
            info_list.append(info_dict)
        return info_list

    def search_card_status(self, sql_line):
        sql = "SELECT COUNT(*) FROM card_info {}".format(sql_line)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows[0][0]


if __name__ == "__main__":
    s = SqlData()
    s.search_name_info()
