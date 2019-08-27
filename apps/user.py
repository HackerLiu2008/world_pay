import json
import logging
from tools_me.other_tools import verify_login_time, xianzai_time, login_required
from tools_me.parameter import RET, MSG
from . import user_blueprint
from flask import render_template, request, jsonify, redirect, url_for, session, g
from tools_me.mysql_tools import SqlData


@user_blueprint.route('/edit_user', methods=['GET'])
@login_required
def ch_pass_html():
    return render_template('user/edit_user.html')


@user_blueprint.route('/smt_pay', methods=['GET', 'POST'])
@login_required
def smt_pay():
    user_id = g.user_id
    if request.method == 'GET':
        pay_discount = SqlData().search_user_field('pay_discount', user_id)
        context = dict()
        if not pay_discount:
            context['info_list'] = ["暂无支付方式及汇率!"]
        else:
            pay_dict = json.loads(pay_discount)
            info_list = list()
            for key, value in pay_dict.items():
                s = '支付方式: ' + str(key) + ", 汇率: " + str(value)
                info_list.append(s)
            context['info_list'] = info_list
        return render_template('user/smt_pay.html', **context)
    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        pay_method = data.get('pay_method')
        pay_dis = data.get('pay_discount')
        pay_discount = SqlData().search_user_field('pay_discount', user_id)
        pay_dict = json.loads(pay_discount)
        if not pay_dis:
            if pay_method in pay_dict:
                pay_dict.pop(pay_method)
                pay_json = json.dumps(pay_dict, ensure_ascii=False)
                SqlData().update_user_field('pay_discount', "'" + pay_json + "'", user_id)
                return jsonify({'code': RET.OK, 'msg': MSG.OK})
            else:
                return jsonify({'code': RET.SERVERERROR, 'msg': '没有该支付方式!!!'})
        if not pay_discount:
            pay_dict = dict()
            pay_dict[pay_method] = float(pay_dis)
            pay_json = json.dumps(pay_dict, ensure_ascii=False)
            SqlData().update_user_field('pay_discount', "'" + pay_json + "'", user_id)
        else:
            pay_dict = json.loads(pay_discount)
            pay_dict[pay_method] = float(pay_dis)
            pay_json = json.dumps(pay_dict, ensure_ascii=False)
            SqlData().update_user_field('pay_discount', "'" + pay_json + "'", user_id)
        return jsonify({'code': RET.OK, 'msg': MSG.OK})


@user_blueprint.route('/smt_serve', methods=['GET', 'POST'])
@login_required
def smt_serve():
    user_id = g.user_id
    if request.method == 'GET':
        amz_serve = SqlData().search_user_field('amz_serve', user_id)
        if not amz_serve:
            context = {'serve_list': ['暂无收费标准!']}
        else:
            serve_dict = json.loads(amz_serve)
            serve_list = list()
            for key, value in sorted(serve_dict.items()):
                if key == 'bili':
                    s = '留评比例: ' + str(value) + "%"
                else:
                    s = "服务类型: " + str(key) + ", 单价: " + str(value)
                serve_list.append(s)
            context = {'serve_list': serve_list}
        return render_template('user/smt_serve_money.html', **context)
    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        bili = data.get('bili')
        pc_money = data.get('pc_money')
        app_money = data.get('app_money')
        text_money = data.get('text_money')
        image_money = data.get('image_money')
        sunday_money = data.get('sunday_money')
        smt_serve = SqlData().search_user_field('amz_serve', user_id)
        if not smt_serve:
            serve_dict = dict()
        else:
            serve_dict = json.loads(smt_serve)
        if bili:
            serve_dict['bili'] = int(bili)
        if pc_money:
            serve_dict['pc_money'] = float(pc_money)
        if app_money:
            serve_dict['app_money'] = float(app_money)
        if text_money:
            serve_dict['text_money'] = float(text_money)
        if image_money:
            serve_dict['image_money'] = float(image_money)
        if sunday_money:
            serve_dict['sunday_money'] = float(sunday_money)

        serve_json = json.dumps(serve_dict)
        SqlData().update_user_field('amz_serve', "'" + serve_json + "'", user_id)
        return jsonify({'code': RET.OK, 'msg': MSG.OK})


@user_blueprint.route('/amz_serve_money', methods=['GET', 'POST'])
@login_required
def amz_serve():
    user_id = g.user_id
    if request.method == 'GET':
        label = request.args.get('label')
        context = {'label': label}
        return render_template('user/amz_serve_money.html', **context)
    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        bili = data.get('bili')
        money = data.get('money')
        label = data.get('label')
        sql = "AND label='" + label + "'"
        field = 'amz_money'
        amz_serve = SqlData().search_cus_of_label(field, user_id, sql)
        if not amz_serve:
            serve_dict = dict()
            serve_dict[bili] = int(money)
        else:
            serve_dict = json.loads(amz_serve)
            serve_dict[bili] = int(money)
        serve_json = json.dumps(serve_dict)
        SqlData().update_user_cus('amz_money', serve_json, user_id, label)
        return jsonify({'code': RET.OK, 'msg': MSG.OK})


@user_blueprint.route('/amz_customer_detail', methods=['GET', 'POST'])
@login_required
def amz_customer_detail():
    user_id = g.user_id
    results = {'code': RET.OK, 'msg': MSG.OK}
    if request.method == 'GET':
        try:
            limit = request.args.get('limit')
            page = request.args.get('page')
            label = request.args.get('label')
            if label:
                sql = "AND label = '" + str(label) + "'"
                info_list = SqlData().search_cus_all(user_id, sql=sql)
            else:
                info_list = SqlData().search_cus_all(user_id)
            new_list = list()
            for i in info_list:
                amz_money = i.get('amz_money')
                if not amz_money:
                    i['0'] = ''
                    i['10'] = ''
                    i['20'] = ''
                    i['30'] = ''
                    i['40'] = ''
                    i['50'] = ''
                    i['60'] = ''
                    i['70'] = ''
                    i['80'] = ''
                    i['90'] = ''
                    i['100'] = ''
                    i['feedback'] = ''
                    new_list.append(i)
                else:
                    money_dict = json.loads(amz_money)
                    i['0'] = money_dict.get('0')
                    i['10'] = money_dict.get('10')
                    i['20'] = money_dict.get('20')
                    i['30'] = money_dict.get('30')
                    i['40'] = money_dict.get('40')
                    i['50'] = money_dict.get('50')
                    i['60'] = money_dict.get('60')
                    i['70'] = money_dict.get('70')
                    i['80'] = money_dict.get('80')
                    i['90'] = money_dict.get('90')
                    i['100'] = money_dict.get('100')
                    i['feedback'] = money_dict.get('feedback')
                    new_list.append(i)
            page_list = list()
            for i in range(0, len(new_list), int(limit)):
                page_list.append(new_list[i:i + int(limit)])
            results['data'] = page_list[int(page) - 1]
            results['count'] = len(new_list)
            return jsonify(results)
        except Exception as e:
            logging.info(str(e))
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.NODATA})


@user_blueprint.route('/amz_money', methods=['GET'])
@login_required
def amz_money():
    user_id = g.user_id
    terrace = SqlData().search_user_field('terrace', user_id)
    if terrace != "AMZ":
        return '该账号没有操作AMZ权限!'
    if request.method == 'GET':
        return render_template('user/amz_money.html')
    if request.method == 'POST':
        try:
            data_list = SqlData().search_customer_detail(user_id)
            str_list = list()
            for i in data_list:
                one_str = ''
                for key, value in i.items():
                    s = str(key) + ':' + str(value) + ', '
                    one_str += s
                str_list.append(one_str)
            context = {'detail_list': str_list}
            return render_template('customer/customer_detail.html', **context)
        except Exception as e:
            logging.error(str(e))
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.NODATA})


@user_blueprint.route('/customer_detail', methods=['GET'])
@login_required
def customer_detail():
    user_id = g.user_id
    terrace = SqlData().search_user_field('terrace', user_id)
    if terrace != 'SMT':
        return '此账号没有查看SMT信息权限!'
    if request.method == 'GET':
        try:
            data_list = SqlData().search_customer_detail(user_id)
            str_list = list()
            for i in data_list:
                one_str = ''
                for key, value in i.items():
                    s = str(key) + ':' + str(value) + ', '
                    one_str += s
                str_list.append(one_str)
            context = {'detail_list': str_list}
            return render_template('customer/customer_detail.html', **context)
        except Exception as e:
            logging.error(str(e))
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.NODATA})


@user_blueprint.route('/amz_customer', methods=['GET', 'POST'])
@login_required
def amz_customer():
    user_id = g.user_id
    terrace = SqlData().search_user_field('terrace', user_id)
    if terrace != 'AMZ':
        return "此帐号没有添加AMZ客户权限!"
    if request.method == 'GET':
        return render_template('user/amz_customer.html')
    elif request.method == "POST":
        data = json.loads(request.form.get('data'))
        add_cus = data.get('add_cus')
        account = data.get('account')
        password = data.get('password')
        note = data.get('note')
        try:
            label_list = SqlData().search_user_cus(user_id)
            if add_cus in label_list:
                if account:
                    SqlData().update_user_cus('account', account, user_id, add_cus)
                if password:
                    SqlData().update_user_cus('pass_word', password, user_id, add_cus)
                if note:
                    SqlData().update_user_cus('note', note, user_id, add_cus)
            if add_cus not in label_list:
                if not account:
                    account = ''
                if not password:
                    password = ''
                if not note:
                    note = ''
                SqlData().insert_user_cus(add_cus, account, password, note, user_id)
            return jsonify({'code': RET.OK, 'msg': MSG.OK})

        except Exception as e:
            logging.error(str(e))
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


@user_blueprint.route('/customer', methods=['GET', 'POST'])
@login_required
def customer():
    user_id = g.user_id
    terrace = SqlData().search_user_field('terrace', user_id)
    if terrace != 'SMT':
        return "该帐号没有添加SMT客户权限!"
    if request.method == 'GET':
        return render_template('user/user_customer.html')
    elif request.method == "POST":
        data = json.loads(request.form.get('data'))
        add_cus = data.get('add_cus')
        account = data.get('account')
        password = data.get('password')
        discount = data.get('discount')
        ex_discount = data.get('ex_discount')
        note = data.get('note')
        try:
            label_list = SqlData().search_user_cus(user_id)
            if add_cus in label_list:
                if account:
                    SqlData().update_user_cus('account', account, user_id, add_cus)
                if password:
                    SqlData().update_user_cus('pass_word', password, user_id, add_cus)
                if discount:
                    SqlData().update_user_cus('discount', float(discount), user_id, add_cus)
                if ex_discount:
                    SqlData().update_user_cus('exchange_dis', float(ex_discount), user_id, add_cus)
                if note:
                    SqlData().update_user_cus('note', note, user_id, add_cus)
            if add_cus not in label_list:
                if not discount:
                    discount = '1.0'
                if not ex_discount:
                    ex_discount = '1.0'
                if not account:
                    account = ''
                if not password:
                    password = ''
                if not note:
                    note = ''
                SqlData().insert_user_cus(add_cus, account, password, note, user_id)
                SqlData().update_user_cus('exchange_dis', float(ex_discount), user_id, add_cus)
                SqlData().update_user_cus('discount', float(discount), user_id, add_cus)
            return jsonify({'code': RET.OK, 'msg': MSG.OK})

        except Exception as e:
            logging.error(str(e))
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


@user_blueprint.route('/conf', methods=['GET', "POST"])
@login_required
def user_conf():
    user_id = g.user_id
    if request.method == "GET":
        dollar_exchange = SqlData().search_user_field('dollar_exchange', user_id)
        context = {'dollar_exchange': dollar_exchange}
        return render_template('user/user_conf.html', **context)
    elif request.method == "POST":
        data = json.loads(request.form.get('data'))
        exchange = data.get('exchange')
        try:
            SqlData().update_user_field('dollar_exchange', float(exchange), user_id)
            return jsonify({'code': RET.OK, 'msg': MSG.OK})
        except Exception as e:
            logging.error(str(e))
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


@user_blueprint.route('/change_pass', methods=["POST"])
@login_required
def change_pass():
    data = json.loads(request.form.get('data'))
    old_pass = data.get('old_pass')
    new_pass_one = data.get('new_pass_one')
    new_pass_two = data.get('new_pass_two')
    results = {'code': RET.OK, 'msg': MSG.OK}
    if not (old_pass == g.pass_word):
        results['code'] = RET.SERVERERROR
        results['msg'] = MSG.PSWDERROR
        return jsonify(results)
    if not (new_pass_one == new_pass_two):
        results['code'] = RET.SERVERERROR
        results['msg'] = MSG.PSWDERROR
        return jsonify(results)
    if len(new_pass_one) < 6:
        results['code'] = RET.SERVERERROR
        results['msg'] = MSG.PSWDLEN
        return jsonify(results)
    try:
        SqlData().update_user_info(new_pass_one, g.user_id)
        return jsonify(results)
    except Exception as e:
        logging.error(e)
        results['code'] = RET.SERVERERROR
        results['msg'] = MSG.SERVERERROR
        return jsonify(results)


@user_blueprint.route('/user_info', methods=['GET'])
@login_required
def user_info():
    user_name = g.user_name
    us_time = g.us_time
    expire_time = g.expire_time
    context = {
        'user_name': user_name,
        'expire_time': expire_time,
        'us_time': us_time
    }
    return render_template('user/user_info.html', **context)


@user_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    session.pop('user_id')
    session.pop('user_name')
    session.pop('pass_word')
    session.pop('expire_time')
    session.pop('us_time')
    session.pop('terrace')
    return render_template('user/login.html')


@user_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')

    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        user_name = data.get('user_name')
        user_pass = data.get('pass_word')
        results = {'code': RET.OK, 'msg': MSG.OK}
        user_data = SqlData().search_user_info(user_name)
        try:
            user_id = user_data.get('user_id')
            pass_word = user_data.get('pass_word')
            expire_time = user_data.get('expire_time')
            us_time = user_data.get('us_time')
            terrace = user_data.get('terrace')
            time_str = expire_time.strftime("%Y-%m-%d %H:%M:%S")
            now_time = xianzai_time()
            if user_pass == pass_word and verify_login_time(time_str, now_time):
                session['user_id'] = user_id
                session['user_name'] = user_name
                session['pass_word'] = pass_word
                session['expire_time'] = time_str
                session['us_time'] = us_time
                session['terrace'] = terrace
                return jsonify(results)
            else:
                results['code'] = RET.SERVERERROR
                results['msg'] = MSG.DATAERROR
                return jsonify(results)

        except Exception as e:
            logging.error(str(e))
            results['code'] = RET.SERVERERROR
            results['msg'] = MSG.DATAERROR
            return jsonify(results)
