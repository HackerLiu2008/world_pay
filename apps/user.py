import json
import logging
import operator
from tools_me.other_tools import verify_login_time, xianzai_time, login_required
from tools_me.parameter import RET, MSG
from . import user_blueprint
from flask import render_template, request, jsonify, session, g
from tools_me.mysql_tools import SqlData


@user_blueprint.route('/top_history/', methods=['GET'])
@login_required
def top_history():
    page = request.args.get('page')
    limit = request.args.get('limit')
    user_id = g.user_id
    task_info = SqlData().search_top_history_acc(user_id)
    task_info = sorted(task_info, key=operator.itemgetter('time'))
    results = {"code": RET.OK, "msg": MSG.OK, "count": 0, "data": ""}
    if len(task_info) == 0:
        results['MSG'] = MSG.NODATA
        return results
    page_list = list()
    task_info = list(reversed(task_info))
    for i in range(0, len(task_info), int(limit)):
        page_list.append(task_info[i:i + int(limit)])
    results['data'] = page_list[int(page) - 1]
    results['count'] = len(task_info)
    return results


@user_blueprint.route('/', methods=['GET'])
@login_required
def account_html():
    user_name = g.user_name
    user_id = g.user_id
    dict_info = SqlData().search_user_index(user_id)
    create_card = dict_info.get('create_card')
    refund = dict_info.get('refund') * 100
    min_top = dict_info.get('min_top')
    max_top = dict_info.get('max_top')
    balance = dict_info.get('balance')
    context = dict()
    context['user_name'] = user_name
    context['balance'] = balance
    context['refund'] = refund
    context['create_card'] = create_card
    context['min_top'] = min_top
    context['max_top'] = max_top
    return render_template('user/index.html', **context)


@user_blueprint.route('/change_phone', methods=['GET'])
@login_required
def change_phone():
    user_id = g.user_id
    phone_num = request.args.get('phone_num')
    results = dict()
    try:
        SqlData().update_user_field('phone_num', phone_num, user_id)
        results['code'] = RET.OK
        results['msg'] = MSG.OK
        return jsonify(results)
    except Exception as e:
        logging.error(str(e))
        results['code'] = RET.SERVERERROR
        results['msg'] = MSG.SERVERERROR
        return jsonify(results)


@user_blueprint.route('/one_card_detail', methods=['GET'])
@login_required
def one_detail():
    try:
        return render_template('account/account_detail.html')
    except Exception as e:
        logging.error((str(e)))


@user_blueprint.route('/change_detail', methods=['GET'])
@login_required
def change_detail():
    return render_template('user/edit_account.html')


@user_blueprint.route('/card_info', methods=['GET'])
@login_required
def card_info():
    limit = request.args.get('limit')
    page = request.args.get('page')
    card_name = request.args.get('card_name')
    card_num = request.args.get('card_num')
    label = request.args.get('label')
    range_time = request.args.get('range_time')
    results = dict()
    results['code'] = RET.OK
    results['msg'] = MSG.OK

    if not card_name and not card_num and not label and not range_time:
        data = [{'card_name': '刘晓', 'card_num': 12121212, 'card_exp': '2019-9-9', 'cvv': '7996', 'amount': 499, 'balance':342, 'label':'测试', 'close_date':'222-22-22', 'status': '正常', 'create_date':'2222-09-99'}]
        page_list = list()
        data = list(reversed(data))
        for i in range(0, len(data), int(limit)):
            page_list.append(data[i:i + int(limit)])
        results['data'] = page_list[int(page) - 1]
        results['count'] = len(data)
        return jsonify(results)
    else:
        print(card_name, card_num, label, range_time)
        return jsonify(results)


@user_blueprint.route('/edit_user', methods=['GET'])
@login_required
def ch_pass_html():
    return render_template('user/edit_user.html')


@user_blueprint.route('/change_pass', methods=["POST"])
@login_required
def change_pass():
    data = json.loads(request.form.get('data'))
    old_pass = data.get('old_pass')
    new_pass_one = data.get('new_pass_one')
    new_pass_two = data.get('new_pass_two')
    user_id = g.user_id
    pass_word = SqlData().search_user_field('password', user_id)
    results = {'code': RET.OK, 'msg': MSG.OK}
    if not (old_pass == pass_word):
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
        SqlData().update_user_field('password', new_pass_one, g.user_id)
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
    user_id = g.user_id
    dict_info = SqlData().search_user_detail(user_id)
    account = dict_info.get('account')
    phone_num = dict_info.get('phone_num')
    balance = dict_info.get('balance')
    context = {
        'user_name': user_name,
        'account': account,
        'balance': balance,
        'phone_num': phone_num,
    }
    return render_template('user/user_info.html', **context)


@user_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    session.pop('user_id')
    session.pop('name')
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
            pass_word = user_data.get('password')
            name = user_data.get('name')
            if user_pass == pass_word:
                session['user_id'] = user_id
                session['name'] = name
                return jsonify(results)
            else:
                results['code'] = RET.SERVERERROR
                results['msg'] = MSG.PSWDERROR
                return jsonify(results)

        except Exception as e:
            logging.error(str(e))
            results['code'] = RET.SERVERERROR
            results['msg'] = MSG.DATAERROR
            return jsonify(results)
