import json
import logging
from . import account_blueprint
from flask import render_template, jsonify, request, session, g
from tools_me.mysql_tools import SqlData
from tools_me.other_tools import login_required
from tools_me.parameter import RET, MSG


@account_blueprint.route('/', methods=['GET'])
@login_required
def account_html():
    user_id = g.user_id
    label_list = SqlData().search_account_label(user_id)
    context = {'user_name': g.user_name}
    if len(label_list) == 0:
        context['label'] = []
    else:
        # 去重
        new_list = list(set(label_list))
        new_list.sort(key=label_list.index)
        # 去空
        new_list = [x for x in new_list if x != '']
        context['label'] = new_list
    return render_template('account/account.html', **context)


@account_blueprint.route('/add_account', methods=["GET"])
@login_required
def add_account():
    return render_template('account/add_account.html')


@account_blueprint.route('/change_detail', methods=['GET'])
@login_required
def change_detail():
    return render_template('account/edit_account.html')


@account_blueprint.route('/batch_change', methods=['GET', 'POST'])
@login_required
def batch_change():
    if request.method == 'GET':
        return render_template('account/batch_account.html')
    elif request.method == 'POST':
        user_id = g.user_id
        data = json.loads(request.form.get('data'))
        batch_list = json.loads(data.get('batch_data'))
        label = data.get('label')
        member_state = data.get('member_state')
        try:
            if not label and not member_state:
                return jsonify({'code': RET.SERVERERROR, 'msg': '请填写参数!'})
            if label:
                for i in batch_list:
                    account = i.get('account')
                    SqlData().update_account_one('label', label, account, user_id)
            if member_state:
                for i in batch_list:
                    account = i.get('account')
                    SqlData().update_account_one('member_state', member_state, account, user_id)

            return jsonify({'code': RET.OK, 'msg': MSG.OK})
        except Exception as e:
            logging.error(str(e))
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


@account_blueprint.route('/del_account', methods=['GET', 'POST'])
@login_required
def del_account():
    user_name = g.user_name
    user_id = g.user_id
    results = {'code': RET.OK, 'msg': MSG.OK}
    if request.method == "GET":
        account = request.args.get('account')
        try:
            SqlData().del_account(account, user_id)
            logging.warning(user_name + '删除' + account)
            return jsonify(results)
        except Exception as e:
            logging.error(str(e))
            results['code'] = RET.SERVERERROR
            results['msg'] = MSG.DATAERROR
            return jsonify(results)
    elif request.method == 'POST':
        data = json.loads(request.form.get('data'))
        try:
            for i in data:
                account = i.get('account')
                SqlData().del_account(account, user_id)
                logging.warning(user_name + '删除' + account)
            return jsonify(results)
        except Exception as e:
            logging.error(str(e))
            results['code'] = RET.SERVERERROR
            results['msg'] = MSG.DATAERROR
            return jsonify(results)


@account_blueprint.route('/one_detail', methods=['GET'])
@login_required
def one_detail():
    account = request.args.get('account')
    user_id = g.user_id
    try:
        context = SqlData().search_account_detail(account, user_id)
        return render_template('account/account_detail.html', **context)
    except Exception as e:
        logging.error((str(e)))


@account_blueprint.route('/detail/', methods=['GET'])
@login_required
def account_detail():
    user_id = g.user_id
    page = request.args.get('page')
    limit = request.args.get('limit')
    buy_state = request.args.get('buy_state')
    account = request.args.get('account')
    label = request.args.get('label')
    terrace = request.args.get('terrace')
    # print(page, limit, account, label, terrace)
    results = {"code": RET.OK, "msg": MSG.OK, "count": 0, "data": ""}
    page_list = list()
    if not account and not label and not terrace:
        try:
            if buy_state == "使用中":
                data = SqlData().search_account_ing("buy_state", buy_state, user_id)
                data = list(reversed(data))
                for i in range(0, len(data), int(limit)):
                    page_list.append(data[i:i + int(limit)])
                results['data'] = page_list[int(page) - 1]
                results['count'] = len(data)
            elif buy_state == '未分配':
                buy_state = ""
                data = SqlData().search_account_ing("buy_state", buy_state, user_id)
                data = list(reversed(data))
                for i in range(0, len(data), int(limit)):
                    page_list.append(data[i:i + int(limit)])
                results['data'] = page_list[int(page) - 1]
                results['count'] = len(data)
            else:
                data = SqlData().search_account(user_id)
                data = list(reversed(data))
                for i in range(0, len(data), int(limit)):
                    page_list.append(data[i:i + int(limit)])
                results['data'] = page_list[int(page) - 1]
                results['count'] = len(data)
        except Exception as e:
            logging.error(str(e))
            results['code'] = RET.SERVERERROR
            results['msg'] = MSG.NODATA
    else:
        sql_label = ''
        sql_account = ''
        sql_terrace = ''
        if label:
            sql_label = "AND label='" + label + "'"
        if account:
            sql_account = "AND account LIKE '%" + account + "%'"
        if terrace:
            sql_terrace = "AND terrace='" + terrace + "'"
        sql = sql_label + sql_account + sql_terrace
        data = SqlData().search_account_sql(sql, user_id)
        results['count'] = len(data)
        results['data'] = data
    return results


@account_blueprint.route('/add_acc_info/', methods=['POST'])
@login_required
def add_acc_info():
    data = json.loads(request.form.get('data'))
    account = data.get('account')
    password = data.get('password')
    email = data.get('email')
    email_pw = data.get('email_pw')
    pay_money = data.get('pay_money')
    reg_time = data.get('reg_time')
    label = data.get('label')
    terrace = data.get('terrace').upper()
    country = data.get('country')
    member_state = data.get('member_state')
    full_name = data.get('full_name')
    phone_num = data.get('phone')
    coun = data.get('coun')
    province = data.get('province')
    city = data.get('city')
    zip_num = data.get('zip')
    detail_address = data.get('detail_address')
    card_num = data.get('card_num')
    sizeof = data.get('sizeof')
    security_code = data.get('security_code')

    user_id = g.user_id

    try:
        SqlData().insert_account_detail(user_id, account, password, email, email_pw, pay_money, reg_time, label, terrace
                                        , country, member_state, full_name, phone_num, coun, province, city, zip_num,
                                        detail_address, card_num, sizeof, security_code)
        results = {'code': RET.OK, 'msg': MSG.OK}
        return jsonify(results)

    except Exception as e:
        logging.error(str(e))
        results = {"code": RET.SERVERERROR, 'msg': MSG.SERVERERROR}
        return jsonify(results)


@account_blueprint.route('/put_account/', methods=['POST'])
@login_required
def put_account():
    data = json.loads(request.form.get('data'))
    account = data.get('account')
    password = data.get('password')
    label = data.get('label')
    terrace = data.get('terrace')
    country = data.get('country')
    member_state = data.get('member_state')
    note = data.get('note')
    # print(account, password, label, terrace, country, member_state, note)
    try:
        SqlData().update_account(password, label, terrace, country, member_state, note, account)
        results = {'code': RET.OK, 'msg': MSG.OK}
        return jsonify(results)

    except Exception as e:
        logging.error(str(e))
        results = {"code": RET.SERVERERROR, 'msg': MSG.SERVERERROR}
        return jsonify(results)

