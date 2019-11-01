import json
import logging
import operator
import re
from flask import request, render_template, jsonify, session, g
from tools_me.mysql_tools import SqlData
from tools_me.other_tools import admin_required, sum_code, xianzai_time, get_nday_list
from tools_me.parameter import RET, MSG
from tools_me.send_sms.send_sms import CCP
from . import admin_blueprint


@admin_blueprint.route('/del_acc/', methods=['POST'])
@admin_required
def del_account():
    try:
        data = json.loads(request.form.get('data'))
        user_name = data.get('user_name')
        user_id = SqlData().search_user_field_name('id', user_name)
        SqlData().del_account_info(user_id)
        return jsonify({"code": RET.OK, "msg": MSG.OK})
    except Exception as e:
        logging.error(str(e))
        return jsonify({"code": RET.SERVERERROR, "msg": MSG.SERVERERROR})


@admin_blueprint.route('/cus_log', methods=['GET'])
@admin_required
def cus_log():
    page = request.args.get('page')
    limit = request.args.get('limit')

    cus_name = request.args.get('cus_name')
    time_range = request.args.get('time_range')
    time_sql = ""
    cus_sql = ""
    if time_range:
        min_time = time_range.split(' - ')[0]
        max_time = time_range.split(' - ')[1] + ' 23:59:59'
        time_sql = "AND log_time BETWEEN " + "'" + min_time + "'" + " and " + "'" + max_time + "'"
    if cus_name:
        cus_sql = "AND customer='" + cus_name + "'"

    task_info = SqlData().search_account_log(cus_sql, time_sql)
    results = {"code": RET.OK, "msg": MSG.OK, "count": 0, "data": ""}
    if len(task_info) == 0:
        results['MSG'] = MSG.NODATA
        return jsonify(results)
    page_list = list()
    task_info = sorted(task_info, key=operator.itemgetter('log_time'))
    task_info = list(reversed(task_info))
    for i in range(0, len(task_info), int(limit)):
        page_list.append(task_info[i:i + int(limit)])
    results['data'] = page_list[int(page) - 1]
    results['count'] = len(task_info)
    return jsonify(results)


@admin_blueprint.route('/account_trans/', methods=['GET'])
@admin_required
def account_trans():
    page = request.args.get('page')
    limit = request.args.get('limit')

    time_range = request.args.get('time_range')
    cus_name = request.args.get('cus_name')
    trans_card = request.args.get('trans_card')
    trans_type = request.args.get('trans_type')
    time_sql = ""
    card_sql = ""
    cus_sql = ""
    type_sql = ""
    if time_range:
        min_time = time_range.split(' - ')[0]
        max_time = time_range.split(' - ')[1] + ' 23:59:59'
        time_sql = "AND account_trans.do_date BETWEEN " + "'" + min_time + "'" + " and " + "'" + max_time + "'"
    if trans_card:
        card_sql = "AND account_trans.card_no = '" + trans_card + "'"
    if cus_name:
        cus_sql = "AND account.name='" + cus_name + "'"
    if trans_type:
        type_sql = "AND account_trans.trans_type = '" + trans_type + "'"

    task_info = SqlData().search_trans_admin(cus_sql, card_sql, time_sql, type_sql)
    results = {"code": RET.OK, "msg": MSG.OK, "count": 0, "data": ""}
    if len(task_info) == 0:
        results['MSG'] = MSG.NODATA
        return jsonify(results)
    page_list = list()
    task_info = sorted(task_info, key=operator.itemgetter('date'))

    task_info = list(reversed(task_info))
    for i in range(0, len(task_info), int(limit)):
        page_list.append(task_info[i:i + int(limit)])
    results['data'] = page_list[int(page) - 1]
    results['count'] = len(task_info)
    return jsonify(results)


@admin_blueprint.route('/card_all', methods=['GET'])
@admin_required
def card_info_all():
    try:
        limit = request.args.get('limit')
        page = request.args.get('page')

        field = request.args.get('field')
        value = request.args.get('value')

        if field == "card_cus":
            account_id = SqlData().search_user_field_name('id', value)
            sql = "WHERE account_id=" + str(account_id)
        elif field:
            sql = "WHERE " + field + " LIKE '%" + value + "%'"
        else:
            sql = ""

        results = dict()
        results['code'] = RET.OK
        results['msg'] = MSG.OK
        info_list = SqlData().search_card_info_admin(sql)
        if not info_list:
            results['code'] = RET.OK
            results['msg'] = MSG.NODATA
            return jsonify(results)
        # info_list = sorted(info_list, key=operator.itemgetter('start_time'))
        page_list = list()
        for i in range(0, len(info_list), int(limit)):
            page_list.append(info_list[i:i + int(limit)])
        results['data'] = page_list[int(page) - 1]
        results['count'] = len(info_list)
        return jsonify(results)
    except Exception as e:
        logging.error(str(e))
        return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


@admin_blueprint.route('/sub_middle_money', methods=['POST'])
@admin_required
def sub_middle_money():
    info_id = request.args.get('id')
    n_time = xianzai_time()
    SqlData().update_middle_sub('已确认', n_time, int(info_id))
    return jsonify({"code": RET.OK, "msg": MSG.OK})


@admin_blueprint.route('/middle_money', methods=['GET'])
@admin_required
def middle_money():
    try:
        limit = request.args.get('limit')
        page = request.args.get('page')
        results = dict()
        results['code'] = RET.OK
        results['msg'] = MSG.OK
        info_list = SqlData().search_middle_money_admin()
        if not info_list:
            results['code'] = RET.OK
            results['msg'] = MSG.NODATA
            return jsonify(results)
        info_list = sorted(info_list, key=operator.itemgetter('start_time'))
        page_list = list()
        info_list = list(reversed(info_list))
        for i in range(0, len(info_list), int(limit)):
            page_list.append(info_list[i:i + int(limit)])
        results['data'] = page_list[int(page) - 1]
        results['count'] = len(info_list)
        return jsonify(results)
    except Exception as e:
        logging.error(str(e))
        return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


@admin_blueprint.route('/card_info/', methods=['GET'])
@admin_required
def card_info():
    limit = request.args.get('limit')
    page = request.args.get('page')
    user_id = request.args.get('u_id')
    results = dict()
    results['code'] = RET.OK
    results['msg'] = MSG.OK
    data = SqlData().search_card_info(user_id, '', '', '', '')
    if len(data) == 0:
        results['code'] = RET.SERVERERROR
        results['msg'] = MSG.NODATA
        return jsonify(results)
    data = sorted(data, key=operator.itemgetter('act_time'))
    page_list = list()
    data = list(reversed(data))
    for i in range(0, len(data), int(limit)):
        page_list.append(data[i:i + int(limit)])
    results['data'] = page_list[int(page) - 1]
    results['count'] = len(data)
    return jsonify(results)


@admin_blueprint.route('/acc_to_middle/', methods=['GET', 'POST'])
@admin_required
def acc_to_middle():
    if request.method == 'GET':
        cus_list = SqlData().search_cus_list()
        context = dict()
        context['cus_list'] = cus_list
        return render_template('admin/acc_to_middle.html', **context)
    if request.method == 'POST':
        results = {"code": RET.OK, "msg": MSG.OK}
        data = json.loads(request.form.get('data'))
        name = data.get('name')
        field = data.get('field')
        value = data.get('value')
        bind_cus = data.get('bind_cus')
        del_cus = data.get('del_cus')
        if value:
            if field == 'card_price':
                try:
                    value = float(value)
                    SqlData().update_middle_field_int('card_price', value, name)
                except:
                    return jsonify({'code': RET.SERVERERROR, 'msg': '提成输入值错误!请输入数字类型!'})
            else:
                SqlData().update_middle_field_str(field, value, name)

        if bind_cus:
            middle_id_now = SqlData().search_user_field_name('middle_id', bind_cus)
            # 判断该客户是否已经绑定中介账号
            if middle_id_now:
                results['code'] = RET.SERVERERROR
                results['msg'] = '该客户已经绑定中介!请解绑后重新绑定!'
                return jsonify(results)
            middle_id = SqlData().search_middle_name('id', name)
            user_id = SqlData().search_user_field_name('id', bind_cus)
            SqlData().update_user_field_int('middle_id', middle_id, user_id)
        if del_cus:
            user_id = SqlData().search_user_field_name('id', del_cus)
            middle_id_now = SqlData().search_user_field_name('middle_id', del_cus)
            middle_id = SqlData().search_middle_name('id', name)
            # 判断这个客户是不是当前中介的客户,不是则无权操作
            if middle_id_now != middle_id:
                results['code'] = RET.SERVERERROR
                results['msg'] = '该客户不是当前中介客户!无权删除!'
                return jsonify(results)
            SqlData().update_user_field_int('middle_id', 'NULL', user_id)
        return jsonify(results)


@admin_blueprint.route('/middle_info/', methods=['GET'])
@admin_required
def middle_info():
    page = request.args.get('page')
    limit = request.args.get('limit')
    results = {"code": RET.OK, "msg": MSG.OK, "count": 0, "data": ""}
    task_info = SqlData().search_middle_info()
    if len(task_info) == 0:
        results['MSG'] = MSG.NODATA
        return jsonify(results)
    page_list = list()
    task_info = list(reversed(task_info))
    for i in range(0, len(task_info), int(limit)):
        page_list.append(task_info[i:i + int(limit)])
    results['data'] = page_list[int(page) - 1]
    results['count'] = len(task_info)
    return jsonify(results)


@admin_blueprint.route('/add_middle/', methods=['POST'])
@admin_required
def add_middle():
    results = {"code": RET.OK, "msg": MSG.OK}
    try:
        data = json.loads(request.form.get('data'))
        name = data.get('name')
        account = data.get('account')
        password = data.get('password')
        phone_num = data.get('phone_num')
        create_price = float(data.get('create_price'))
        note = data.get('note1')
        ret = SqlData().search_middle_ed(name)
        if ret:
            results['code'] = RET.SERVERERROR
            results['msg'] = '该中介名已存在!'
            return jsonify(results)
        '''
        ret = re.match(r"^1[35789]\d{9}$", phone_num)
        if not ret:
            results['code'] = RET.SERVERERROR
            results['msg'] = '请输入符合规范的电话号码!'
            return jsonify(results)
        '''
        SqlData().insert_middle(account, password, name, phone_num, create_price, note)
        return jsonify(results)
    except Exception as e:
        logging.error(e)
        results['code'] = RET.SERVERERROR
        results['msg'] = RET.SERVERERROR
        return jsonify(results)


@admin_blueprint.route('/add_account/', methods=['POST'])
@admin_required
def add_account():
    results = {"code": RET.OK, "msg": MSG.OK}
    try:
        data = json.loads(request.form.get('data'))
        name = data.get('name')
        account = data.get('account')
        password = data.get('password')
        phone_num = data.get('phone_num')
        create_price = float(data.get('create_price'))
        refund = float(data.get('refund'))
        min_top = float(data.get('min_top'))
        max_top = float(data.get('max_top'))
        note = data.get('note')
        ed_name = SqlData().search_user_field_name('account', name)
        if ed_name:
            results['code'] = RET.SERVERERROR
            results['msg'] = '该用户名已存在!'
            return jsonify(results)
        if phone_num:
            ret = re.match(r"^1[35789]\d{9}$", phone_num)
            if not ret:
                results['code'] = RET.SERVERERROR
                results['msg'] = '请输入符合规范的电话号码!'
                return jsonify(results)
        else:
            phone_num = ""
        SqlData().insert_account(account, password, phone_num, name, create_price, refund, min_top, max_top, note)
        return jsonify(results)
    except Exception as e:
        logging.error(e)
        results['code'] = RET.SERVERERROR
        results['msg'] = MSG.SERVERERROR
        return jsonify(results)


@admin_blueprint.route('/top_msg', methods=['GET', 'POST'])
@admin_required
def top_msg():
    if request.method == 'GET':
        push_json = SqlData().search_admin_field('top_push')
        info_list = list()
        if push_json:
            push_dict = json.loads(push_json)
            for i in push_dict:
                info_dict = dict()
                info_dict['user'] = i
                info_dict['email'] = push_dict.get(i)
                info_list.append(info_dict)
        context = dict()
        context['info_list'] = info_list
        return render_template('admin/top_msg.html', **context)
    if request.method == 'POST':
        try:
            results = {"code": RET.OK, "msg": MSG.OK}
            data = json.loads(request.form.get('data'))
            top_people = data.get('top_people')
            email = data.get('email')
            push_json = SqlData().search_admin_field('top_push')
            if not push_json:
                info_dict = dict()
                info_dict[top_people] = email
            else:
                info_dict = json.loads(push_json)
                if top_people in info_dict and email == '删除':
                    info_dict.pop(top_people)
                else:
                    info_dict[top_people] = email
            json_info = json.dumps(info_dict, ensure_ascii=False)
            SqlData().update_admin_field('top_push', json_info)
            return jsonify(results)
        except Exception as e:
            logging.error(str(e))
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


@admin_blueprint.route('/ex_change', methods=['GET', 'POST'])
@admin_required
def ex_change():
    if request.method == 'GET':
        return render_template('admin/exchange_edit.html')
    if request.method == 'POST':
        try:
            results = {"code": RET.OK, "msg": MSG.OK}
            data = json.loads(request.form.get('data'))
            exchange = data.get('exchange')
            ex_range = data.get('ex_range')
            hand = data.get('hand')
            dollar_hand = data.get('dollar_hand')
            if exchange:
                SqlData().update_admin_field('ex_change', float(exchange))
            if ex_range:
                SqlData().update_admin_field('ex_range', float(ex_range))
            if hand:
                SqlData().update_admin_field('hand', float(hand))
            if dollar_hand:
                SqlData().update_admin_field('dollar_hand', float(dollar_hand))
            return jsonify(results)
        except Exception as e:
            logging.error(str(e))
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


@admin_blueprint.route('/change_pass', methods=['GET', 'POST'])
@admin_required
def change_pass():
    if request.method == 'GET':
        return render_template('admin/admin_edit.html')
    if request.method == 'POST':
        results = {"code": RET.OK, "msg": MSG.OK}
        data = json.loads(request.form.get('data'))
        old_pass = data.get('old_pass')
        new_pass_one = data.get('new_pass_one')
        new_pass_two = data.get('new_pass_two')
        if new_pass_two != new_pass_one:
            results['code'] = RET.SERVERERROR
            results['msg'] = '两次输入密码不一致!'
            return jsonify(results)
        password = SqlData().search_admin_field('password')
        if old_pass != password:
            results['code'] = RET.SERVERERROR
            results['msg'] = '密码错误!'
            return jsonify(results)
        SqlData().update_admin_field('password', new_pass_one)
        return jsonify(results)


@admin_blueprint.route('/admin_info', methods=['GET'])
@admin_required
def admin_info():
    account, password, name, balance = SqlData().admin_info()
    context = dict()
    context['account'] = account
    context['password'] = password
    context['name'] = name
    context['balance'] = balance
    return render_template('admin/admin_info.html', **context)


@admin_blueprint.route('/top_history', methods=['GET'])
@admin_required
def top_history():
    page = request.args.get('page')
    limit = request.args.get('limit')

    acc_name = request.args.get('acc_name')
    order_num = request.args.get('order_num')
    time_range = request.args.get('time_range')

    results = {"code": RET.OK, "msg": MSG.OK, "count": 0, "data": ""}

    name_sql = ""
    order_sql = ""
    time_sql = ""
    if acc_name:
        name_sql = "account.name ='" + acc_name + "'"
    if order_num:
        order_sql = "top_up.pay_num = '" + order_num + "'"
    if time_range:
        min_time = time_range.split(' - ')[0]
        max_time = time_range.split(' - ')[1] + ' 23:59:59'
        time_sql = "top_up.time BETWEEN " + "'" + min_time + "'" + " and " + "'" + max_time + "'"

    if name_sql and time_sql and order_sql:
        sql_all = "WHERE " + name_sql + " AND " + order_sql + " AND " + time_sql
    elif name_sql and order_sql:
        sql_all = "WHERE " + name_sql + " AND " + order_sql
    elif time_sql and order_sql:
        sql_all = "WHERE " + time_sql + " AND " + order_sql
    elif name_sql and time_sql:
        sql_all = "WHERE " + name_sql + " AND " + time_sql
    elif name_sql:
        sql_all = "WHERE " + name_sql
    elif order_sql:
        sql_all = "WHERE " + order_sql
    elif time_range:
        sql_all = "WHERE " + time_sql
    else:
        sql_all = ""

    task_info = SqlData().search_top_history(sql_all)

    if len(task_info) == 0:
        results['MSG'] = MSG.NODATA
        return jsonify(results)
    page_list = list()
    task_info = sorted(task_info, key=operator.itemgetter('time'))
    task_info = list(reversed(task_info))
    for i in range(0, len(task_info), int(limit)):
        page_list.append(task_info[i:i + int(limit)])
    data = page_list[int(page) - 1]

    # 处理不同充值类型的显示方式(系统, 退款)
    info_list_1 = list()
    for n in data:
        trans_type = n.get('trans_type')
        if trans_type == '系统':
            n['refund'] = ''
        else:
            n['refund'] = n.get('money')
            n['money'] = ''
        info_list_1.append(n)

    # 查询当次充值时的账号总充值金额
    info_list = list()
    for o in info_list_1:
        x_time = o.get('time')
        user_id = o.get('user_id')
        sum_money = SqlData().search_time_sum_money(x_time, user_id)
        o['sum_balance'] = round(sum_money, 2)
        info_list.append(o)
    results['data'] = info_list
    results['count'] = len(task_info)
    return jsonify(results)


@admin_blueprint.route('/top_up', methods=['POST'])
@admin_required
def top_up():
    results = {"code": RET.OK, "msg": MSG.OK}
    try:
        data = request.form.get('money')
        name = request.form.get('name')
        pay_num = sum_code()
        t = xianzai_time()
        money = float(data)
        before = SqlData().search_user_field_name('balance', name)
        balance = before + money
        user_id = SqlData().search_user_field_name('id', name)
        # 更新账户余额
        SqlData().update_user_balance(money, user_id)
        # 更新客户充值记录
        SqlData().insert_top_up(pay_num, t, money, before, balance, user_id, '系统')

        phone = SqlData().search_user_field_name('phone_num', name)

        if phone:

            CCP().send_Template_sms(phone, [name, t, money], 478898)

        return jsonify(results)

    except Exception as e:
        logging.error(e)
        results['code'] = RET.SERVERERROR
        results['msg'] = MSG.SERVERERROR
        return jsonify(results)


@admin_blueprint.route('/edit_parameter', methods=['GET', 'POST'])
@admin_required
def edit_parameter():
    if request.method == 'GET':
        return render_template('admin/edit_parameter.html')
    if request.method == 'POST':
        results = {"code": RET.OK, "msg": MSG.OK}
        try:
            data = json.loads(request.form.get('data'))
            print(data)
            name = data.get('name_str')
            create_price = data.get('create_price')
            refund = data.get('refund')
            min_top = data.get('min_top')
            max_top = data.get('max_top')
            password = data.get('password')
            user_name = data.get('user_name')
            if create_price:
                SqlData().update_account_field('create_price', float(create_price), name)
            if refund:
                SqlData().update_account_field('refund', float(refund), name)
            if min_top:
                SqlData().update_account_field('min_top', float(min_top), name)
            if max_top:
                SqlData().update_account_field('max_top', float(max_top), name)
            if password:
                SqlData().update_account_field_str('password', password, name)
            if user_name:
                password = SqlData().search_user_field_name('password', user_name)
                if password:
                    return jsonify({'code': RET.SERVERERROR, 'msg': '该用户名已存在,请更换用户名后重试!'})
                SqlData().update_account_field_str('name', user_name, name)
            return jsonify(results)
        except Exception as e:
            logging.error(e)
            results['code'] = RET.SERVERERROR
            results['msg'] = MSG.SERVERERROR
            return jsonify(results)


@admin_blueprint.route('/account_info', methods=['GET'])
@admin_required
def account_info():
    page = request.args.get('page')
    limit = request.args.get('limit')
    customer = request.args.get('customer')
    results = {"code": RET.OK, "msg": MSG.OK, "count": 0, "data": ""}
    if customer:
        sql = "WHERE name LIKE '%" + customer + "%'"
    else:
        sql = ''
    task_one = SqlData().search_account_info(sql)
    if len(task_one) == 0:
        results['MSG'] = MSG.NODATA
        return jsonify(results)
    task_info = list()
    for u in task_one:
        u_id = u.get('u_id')
        card_count = SqlData().search_card_count(u_id, '')
        out_money = SqlData().search_trans_sum(u_id)
        u['card_num'] = card_count
        u['out_money'] = out_money
        task_info.append(u)
    page_list = list()
    task_info = list(reversed(task_info))
    for i in range(0, len(task_info), int(limit)):
        page_list.append(task_info[i:i + int(limit)])
    results['data'] = page_list[int(page) - 1]
    results['count'] = len(task_info)
    return jsonify(results)


@admin_blueprint.route('/card_list_html', methods=['GET'])
@admin_required
def card_list_html():
    user_id = request.args.get('user_id')
    context = dict()
    context['user_id'] = user_id
    return render_template('admin/card_list.html', **context)


@admin_blueprint.route('/line_chart', methods=['GET'])
@admin_required
def test():
    day_list = get_nday_list(30)
    account_list = SqlData().search_user_field_admin()
    data = list()
    if account_list:
        for u_id in account_list:
            info_dict = dict()
            count_list = list()
            for i in day_list:
                sql_str = "AND act_time BETWEEN '" + str(i) + ' 00:00:00' + "'" + " and '" + str(i) + " 23:59:59'"
                account_id = u_id.get('id')
                card_count = SqlData().search_card_count(account_id, sql_str)
                count_list.append(card_count)
            info_dict['name'] = u_id.get('name')
            info_dict['data'] = count_list
            data.append(info_dict)
    else:
        data = [{'name': '无客户', 'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}]

    results = dict()
    results['code'] = RET.OK
    results['msg'] = MSG.OK
    results['data'] = data
    results['xAx'] = day_list
    return jsonify(results)


@admin_blueprint.route('/logout', methods=['GET'])
@admin_required
def logout():
    session.pop('admin_id')
    session.pop('admin_name')
    return render_template('admin/admin_login.html')


@admin_blueprint.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin/admin_login.html')

    if request.method == 'POST':
        results = dict()
        results['code'] = RET.OK
        results['msg'] = MSG.OK
        try:
            data = json.loads(request.form.get('data'))
            account = data.get('account')
            password = data.get('password')
            admin_id, name = SqlData().search_admin_login(account, password)
            session['admin_id'] = admin_id
            session['admin_name'] = name
            return jsonify(results)

        except Exception as e:
            logging.error(str(e))
            results['code'] = RET.SERVERERROR
            results['msg'] = MSG.PSWDERROR
            return jsonify(results)


@admin_blueprint.route('/', methods=['GET'])
@admin_required
def index():
    '''
    查询主页面信息
    :return:
    '''
    admin_name = g.admin_name
    spent = SqlData().search_trans_sum_admin()
    sum_balance = SqlData().search_user_sum_balance()
    card_use = SqlData().search_card_status("WHERE account_id != ''")
    card_no = SqlData().search_card_status("WHERE account_id is null AND activation != ''")
    ex_change = SqlData().search_admin_field('ex_change')
    ex_range = SqlData().search_admin_field('ex_range')
    hand = SqlData().search_admin_field('hand')
    dollar_hand = SqlData().search_admin_field('dollar_hand')
    context = dict()
    context['admin_name'] = admin_name
    context['spent'] = spent
    context['advance'] = sum_balance
    context['card_use'] = card_use
    context['card_no'] = card_no
    context['ex_change'] = ex_change
    context['ex_range'] = ex_range
    context['hand'] = hand
    context['dollar_hand'] = dollar_hand
    return render_template('admin/index.html', **context)
