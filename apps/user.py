import json
import logging
import operator
from tools_me.other_tools import xianzai_time, login_required, check_float, make_name, choke_required, sum_code
from tools_me.parameter import RET, MSG, TRANS_STATUS, TRANS_TYPE, DO_TYPE
from tools_me.RSA_NAME.helen import QuanQiuFu
from tools_me.remain import get_card_remain
from . import user_blueprint
from flask import render_template, request, jsonify, session, g
from tools_me.mysql_tools import SqlData


@user_blueprint.route('/card_lock/', methods=['POST'])
@login_required
def card_lock():
    try:
        card_no = request.args.get('card_no')
        resp = QuanQiuFu().card_status_query(card_no)
        resp_code = resp.get('resp_code')
        if resp_code != "0000":
            return jsonify({'code': RET.SERVERERROR, 'msg': '服务器繁忙请稍后在试!'})
        resp_detail = resp.get('response_detail')
        card_status = resp_detail.get('card_status')
        pay_passwd = SqlData().search_card_field('pay_passwd', card_no)
        if card_status == "00":
            # 挂失
            do_type = DO_TYPE.CARD_LOCK
            card_status_field = '11'
        elif card_status == '11':
            # 解挂
            do_type = DO_TYPE.CARD_OPEN
            card_status_field = '0'
        else:
            return jsonify({'code': RET.SERVERERROR, 'msg': '服务器繁忙请稍后在试!'})
        resp = QuanQiuFu().card_loss(card_no, pay_passwd, do_type)
        resp_code = resp.get('resp_code')
        if resp_code == '0000':
            SqlData().update_card_info_card_no('card_status', card_status_field, card_no)
            return jsonify({'code': RET.OK, 'msg': MSG.OK})
        else:
            return jsonify({'code': RET.SERVERERROR, 'msg': '服务器繁忙请稍后在试!'})
    except Exception as e:
        logging.error(str(e))
        return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


@user_blueprint.route('/refund/', methods=['POST'])
@login_required
def refund_balance():
    try:
        data = json.loads(request.form.get('data'))
        card_no = json.loads(request.form.get('card_no'))
        pay_passwd = SqlData().search_card_field('pay_passwd', card_no)
        if "-" in str(data):
            return jsonify({'code': RET.SERVERERROR, 'msg': '请输入正确金额!'})
        refund_money = str(round(float(data) * 100))
        resp = QuanQiuFu().trans_account_cinsume(card_no, pay_passwd, refund_money)
        resp_code = resp.get('resp_code')
        resp_msg = resp.get('resp_msg')
        results = {"code": RET.OK, "msg": MSG.OK}
        if resp_code == "0000":
            user_id = g.user_id
            refund = SqlData().search_user_field('refund', user_id)
            hand_money = round(refund * float(data), 2)
            do_money = round(float(data) - hand_money, 2)
            before_balance = SqlData().search_user_field('balance', user_id)
            balance = round(before_balance + do_money, 2)
            # 更新账户余额
            SqlData().update_user_balance(do_money, user_id)

            n_time = xianzai_time()
            SqlData().insert_account_trans(n_time, TRANS_TYPE.IN, DO_TYPE.REFUND, 1, card_no, do_money, hand_money,
                                           before_balance,
                                           balance, user_id)

            # 更新客户充值记录
            pay_num = sum_code()
            t = xianzai_time()
            SqlData().insert_top_up(pay_num, t, do_money, before_balance, balance, user_id)

            results['msg'] = resp_msg
        else:
            resp_msg = resp.get('resp_msg')
            s = '卡余额领回失败,状态码: ' + resp_code + ',信息: ' + resp_msg
            logging.error(s)
            results['code'] = RET.SERVERERROR
            results['msg'] = resp_msg
        return jsonify(results)
    except Exception as e:
        print(e)
        logging.error(str(e))
        results = {"code": RET.SERVERERROR, "msg": MSG.SERVERERROR}
        return jsonify(results)


@user_blueprint.route('/account_trans/', methods=['GET'])
@login_required
def account_trans():
    page = request.args.get('page')
    limit = request.args.get('limit')

    time_range = request.args.get('time_range')
    card_num = request.args.get('card_num')
    time_sql = ""
    card_sql = ""
    if time_range:
        min_time = time_range.split(' - ')[0]
        max_time = time_range.split(' - ')[1] + ' 23:59:59'
        time_sql = "AND date BETWEEN " + "'" + min_time + "'" + " and " + "'" + max_time + "'"
    if card_num:
        card_sql = "AND card_no LIKE '%" + card_num + "%'"

    user_id = g.user_id
    task_info = SqlData().search_account_trans(user_id, card_sql, time_sql)
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


@user_blueprint.route('/top_up/', methods=['POST'])
@login_required
def top_up():
    data = json.loads(request.form.get('data'))
    user_id = g.user_id
    card_no = data.get('card_no')
    top_money = data.get('top_money')
    if not check_float(top_money):
        results = {"code": RET.SERVERERROR, "msg": "充值金额不能为小数!"}
        return jsonify(results)
    money = str(int(top_money) * 100)
    resp = QuanQiuFu().trans_account_recharge(card_no, money)
    resp_code = resp.get('resp_code')
    if resp_code == '0000':
        before_balance = SqlData().search_user_field('balance', user_id)
        balance = round(before_balance - int(top_money), 2)
        SqlData().update_user_field_int('balance', balance, user_id)
        n_time = xianzai_time()
        SqlData().insert_account_trans(n_time, TRANS_TYPE.OUT, DO_TYPE.TOP_UP, 1, card_no, float(top_money), 0, before_balance,
                                       balance, user_id)
        return jsonify({"code": RET.OK, "msg": "充值成功!请刷新界面!"})
    else:
        resp_msg = resp.get('resp_msg')
        s = '充值卡余额失败,状态码: ' + resp_code + ',信息: ' + resp_msg
        logging.error(s)
        return jsonify({"code": RET.SERVERERROR, "msg": "充值失败!请联系服务商解决!"})


@user_blueprint.route('/create_some/', methods=['POST'])
@login_required
@choke_required
def create_some():

    # print(session.get('create'))
    data = json.loads(request.form.get('data'))
    card_num = data.get('card_num')
    name_status = data.get('n')
    content = data.get('content')
    limit = data.get('limit')
    label = data.get('label')
    user_id = g.user_id
    user_data = SqlData().search_user_index(user_id)
    create_price = user_data.get('create_card')
    min_top = user_data.get('min_top')
    max_top = user_data.get('max_top')
    balance = user_data.get('balance')

    card_num = int(card_num)
    if card_num > 20:
        results = {"code": RET.SERVERERROR, "msg": "批量开卡数量不得超过20张!"}
        return jsonify(results)

    if name_status == "write":
        name_list = content.split("|")
        if len(name_list) < card_num:
            results = {"code": RET.SERVERERROR, "msg": "名字数量小于建卡数量!"}
            return jsonify(results)
    else:
        name_list = make_name(card_num)

    if not check_float(limit):
        results = {"code": RET.SERVERERROR, "msg": "充值金额不能为小数!"}
        return jsonify(results)
    sum_money = card_num * int(limit) + card_num * create_price

    # 本次开卡需要的费用,计算余额是否充足
    if sum_money > balance:
        results = {"code": RET.SERVERERROR, "msg": "本次消费金额:" + str(sum_money) + ",账号余额不足!"}
        return jsonify(results)

    # 计算充值金额是否在允许范围
    if not min_top <= int(limit) <= max_top:
        results = {"code": RET.SERVERERROR, "msg": "充值金额不在允许范围内!"}
        return jsonify(results)

    act_count = SqlData().search_activation_count()

    if act_count < card_num:
        results = {"code": RET.SERVERERROR, "msg": "请联系服务商添加库存!"}
        return jsonify(results)

    try:
        for i in range(card_num):
            activation = SqlData().search_activation()
            if not activation:
                return jsonify({"code": RET.SERVERERROR, "msg": "请联系服务商添加库存!"})
            pay_passwd = "04A5E788"
            resp = QuanQiuFu().create_card(activation, pay_passwd)
            # print(resp)
            resp_code = resp.get('resp_code')
            # print(resp_code)
            if resp_code != '0000' or resp_code != '0079':
                resp_msg = resp.get('resp_msg')
                s = '激活卡失败,状态码: ' + resp_code + ',信息: ' + resp_msg + ',激活码为:' + activation
                logging.error(s)
                return jsonify({"code": RET.SERVERERROR, "msg": resp_msg})
            SqlData().update_card_info_field('account_id', user_id, activation)
            try:
                card_no = resp.get('response_detail').get('card_no')
            except Exception as e:
                logging.error('获取卡号失败!以下是返回的resp: ' + resp)
                resp = QuanQiuFu().create_card(activation, pay_passwd)
                card_no = resp.get('response_detail').get('card_no')
            before_balance = SqlData().search_user_field('balance', user_id)
            balance = before_balance - create_price
            n_time = xianzai_time()
            SqlData().insert_account_trans(n_time, TRANS_TYPE.OUT, DO_TYPE.CREATE_CARD, 1, card_no, create_price, 0, before_balance,
                                           balance, user_id)
            SqlData().update_user_field_int('balance', balance, user_id)

            resp_card_info = QuanQiuFu().query_card_info(card_no)
            # print(resp_card_info)
            if resp_card_info.get('resp_code') != '0000' or resp_code != '0079':
                expire_date = ''
                card_verify_code = ''
            else:
                re_de = resp_card_info.get('response_detail')
                expire_date = re_de.get('expire_date')
                card_verify_code = re_de.get('card_verify_code')
            act_time = xianzai_time()
            card_name = name_list.pop()
            SqlData().update_card_info(card_no, pay_passwd, act_time, card_name, label, expire_date, card_verify_code, user_id, activation)

            before_balance = SqlData().search_user_field('balance', user_id)
            money = str(int(limit) * 100)
            resp = QuanQiuFu().trans_account_recharge(card_no, money)
            resp_code = resp.get('resp_code')
            # print(resp)
            if resp_code == '0000':
                top_money = int(limit)
                balance = round(before_balance - top_money, 2)
                SqlData().update_user_field_int('balance', balance, user_id)
                n_time = xianzai_time()
                SqlData().insert_account_trans(n_time, TRANS_TYPE.OUT, DO_TYPE.TOP_UP, 1, card_no, top_money, 0, before_balance, balance, user_id)
            else:
                resp_msg = resp.get('resp_msg')
                s = '充值卡余额失败,状态码: ' + resp_code + ',信息: ' + resp_msg
                logging.error(s)
                card_num = str(i+1)
                s = "成功开卡"+card_num+"张,充值第"+card_num+"失败!请单独充值卡号:"+card_no+"!"
                return jsonify({"code": RET.SERVERERROR, "msg": s})
        return jsonify({"code": RET.OK, "msg": "成功开卡"+str(card_num)+"张!请刷新界面!"})
    except Exception as e:
        logging.error(e)
        results = {"code": RET.SERVERERROR, "msg": MSG.SERVERERROR}
        return jsonify(results)


@user_blueprint.route('/create_card/', methods=['POST'])
@login_required
@choke_required
def create_card():
    data = json.loads(request.form.get('data'))
    card_name = data.get('card_name')
    top_money = data.get('top_money')
    label = data.get('label')
    user_id = g.user_id
    user_data = SqlData().search_user_index(user_id)
    create_price = user_data.get('create_card')
    min_top = user_data.get('min_top')
    max_top = user_data.get('max_top')
    balance = user_data.get('balance')

    if not check_float(top_money):
        results = {"code": RET.SERVERERROR, "msg": "充值金额不能为小数!"}
        return jsonify(results)

    # 本次开卡需要的费用,计算余额是否充足
    money_all = int(top_money) + create_price
    if money_all > balance:
        results = {"code": RET.SERVERERROR, "msg": "本次消费金额:" + str(money_all) + ",账号余额不足!"}
        return jsonify(results)

    # 计算充值金额是否在允许范围
    if not min_top <= int(top_money) <= max_top:
        results = {"code": RET.SERVERERROR, "msg": "充值金额不在允许范围内!"}
        return jsonify(results)


    try:
        activation = SqlData().search_activation()
        if not activation:
            return jsonify({"code": RET.SERVERERROR, "msg": "请联系服务商添加库存!"})
        pay_passwd = "04A5E788"
        resp = QuanQiuFu().create_card(activation, pay_passwd)
        # print(resp)
        resp_code = resp.get('resp_code')
        # print(resp_code)
        if resp_code != '0000' or resp_code != '0079':
            resp_msg = resp.get('resp_msg')
            s = '卡激活失败! 状态码: ' + resp_code + ',信息: ' + resp_msg + '激活码为: ' + activation
            logging.error(s)
            return jsonify({"code": RET.SERVERERROR, "msg": resp_msg})

        SqlData().update_card_info_field('account_id', user_id, activation)
        try:
            card_no = resp.get('response_detail').get('card_no')
        except Exception as e:
            logging.error('获取卡号失败!以下是返回的resp: ' + resp)
            resp = QuanQiuFu().create_card(activation, pay_passwd)
            card_no = resp.get('response_detail').get('card_no')

        before_balance = SqlData().search_user_field('balance', user_id)
        balance = before_balance - create_price
        n_time = xianzai_time()
        SqlData().insert_account_trans(n_time, TRANS_TYPE.OUT, DO_TYPE.CREATE_CARD, 1, card_no, create_price, 0, before_balance,
                                       balance, user_id)
        SqlData().update_user_field_int('balance', balance, user_id)

        resp_card_info = QuanQiuFu().query_card_info(card_no)
        # print(resp_card_info)
        if resp_card_info.get('resp_code') != '0000':
            expire_date = ''
            card_verify_code = ''
        else:
            re_de = resp_card_info.get('response_detail')
            expire_date = re_de.get('expire_date')
            card_verify_code = re_de.get('card_verify_code')
        act_time = xianzai_time()
        SqlData().update_card_info(card_no, pay_passwd, act_time, card_name, label, expire_date, card_verify_code, user_id, activation)

        before_balance = SqlData().search_user_field('balance', user_id)
        money = str(int(float(top_money) * 100))
        resp = QuanQiuFu().trans_account_recharge(card_no, money)
        resp_code = resp.get('resp_code')

        if resp_code == '0000':
            top_money = float(top_money)
            balance = round(before_balance - top_money, 2)
            SqlData().update_user_field_int('balance', balance, user_id)
            n_time = xianzai_time()
            SqlData().insert_account_trans(n_time, TRANS_TYPE.OUT, DO_TYPE.TOP_UP, 1, card_no, top_money, 0, before_balance, balance, user_id)

            return jsonify({"code": RET.OK, "msg": "开卡成功!请刷新界面!"})
        else:
            resp_msg = resp.get('resp_msg')
            s = '充值卡余额失败,状态码: ' + resp_code + ',信息: ' + resp_msg
            logging.error(s)
            return jsonify({"code": RET.SERVERERROR, "msg": "开卡成功,充值失败!"})

    except Exception as e:
        logging.error(e)
        results = {"code": RET.SERVERERROR, "msg": MSG.SERVERERROR}
        return jsonify(results)


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
    sum_balance = dict_info.get('sum_balance')
    out_money = SqlData().search_trans_sum(user_id)
    context = dict()
    context['user_name'] = user_name
    context['balance'] = balance
    context['refund'] = refund
    context['create_card'] = create_card
    context['min_top'] = min_top
    context['max_top'] = max_top
    context['sum_balance'] = sum_balance
    context['out_money'] = out_money
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
# @login_required
def one_detail():
    try:
        context = dict()
        card_no = request.args.get('card_no')
        resp = QuanQiuFu().query_card_info(card_no)
        if resp.get('resp_code') == '0000':
            detail = resp.get('response_detail')
            freeze_fee_all = detail.get('freeze_fee_all')
            balance = detail.get('balance')
            f_freeze = int(freeze_fee_all)/100
            f_balance = int(balance)/100
            remain = round(f_balance - f_freeze, 2)
            context['balance'] = f_balance
            context['freeze_fee_all'] = f_freeze
            context['remain'] = remain

        resp = QuanQiuFu().auth_trade_query(card_no)
        if resp.get('resp_code') == '0000':
            result_set = resp.get('response_detail').get('result_set')
            info_list = list()
            for i in result_set:
                info_dict = dict()
                info_dict['trade_no'] = i.get('trade_no')
                if i.get('merchant_name') == "香港龙日实业有限公司":
                    info_dict['merchant_name'] = "全球付"
                else:
                    info_dict['merchant_name'] = i.get('merchant_name')
                trans_type = i.get('trans_type')[0:2]
                if trans_type == '01':
                    info_dict['trans_type'] = '充值'
                elif trans_type == '02':
                    info_dict['trans_type'] = '消费'
                else:
                    info_dict['trans_type'] = '暂未定义消费类型'
                status_code = i.get('trans_status')
                info_dict['trans_status'] = TRANS_STATUS.get(status_code)

                info_dict['trans_amount'] = i.get('trans_amount')
                info_dict['trans_currency_type'] = i.get('trans_currency_type')
                # info_dict['trans_local_time'] = i.get('trans_local_time')
                info_dict['trans_local_time'] = i.get('app_time')
                info_dict['auth_settle_amount'] = i.get('auth_settle_amount')
                info_dict['settle_amount'] = i.get('settle_amount')
                info_dict['settle_currency_type'] = i.get('settle_currency_type')
                info_list.append(info_dict)
            context['pay_list'] = info_list
        return render_template('user/card_detail.html', **context)
    except Exception as e:
        logging.error((str(e)))
        return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


@user_blueprint.route('/change_detail', methods=['GET'])
@login_required
def change_detail():
    return render_template('user/edit_account.html')


@user_blueprint.route('/change_card_name', methods=['GET', 'POST'])
@login_required
def change_card_name():
    if request.method == 'GET':
        return render_template('user/card_name.html')
    if request.method == 'POST':
        try:
            data = json.loads(request.form.get('data'))
            card_no = data.get('card_no')
            card_name = data.get('card_name')
            card_label = data.get('card_label')
            card_no = card_no.strip()
            if card_name:
                SqlData().update_card_info_card_no('card_name', card_name, card_no)
            if card_label:
                SqlData().update_card_info_card_no('label', card_label, card_no)
            return jsonify({'code': RET.OK, 'msg': MSG.OK})
        except Exception as e:
            logging.error(str(e))
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


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
    user_id = g.user_id

    if not card_name and not card_num and not label and not range_time:
        data = SqlData().search_card_info(user_id, '', '', '', '')
        if len(data) == 0:
            results['code'] = RET.SERVERERROR
            results['msg'] = MSG.NODATA
            return results
        data = sorted(data, key=operator.itemgetter('act_time'))
    else:
        name_sql = ''
        if card_name:
            name_sql = "AND card_name LIKE '%" + card_name + "%'"
        card_sql = ''
        if card_num:
            card_sql = "AND card_no LIKE '%" + card_num + "%'"
        label_sql = ''
        if label:
            label_sql = "AND label LIKE '%" + label + "%'"
        time_sql = ''
        if range_time:
            min_time = range_time.split(' - ')[0]
            max_time = range_time.split(' - ')[1] + ' 23:59:59'
            time_sql = "AND act_time BETWEEN " + "'" + min_time + "'" + " and " + "'" + max_time + "'"
        data = SqlData().search_card_info(user_id, name_sql, card_sql, label_sql, time_sql)
        if len(data) == 0:
            results['code'] = RET.SERVERERROR
            results['msg'] = MSG.NODATA
            return results
    page_list = list()
    info = list(reversed(data))
    for i in range(0, len(info), int(limit)):
        page_list.append(info[i:i + int(limit)])
    data = page_list[int(page) - 1]
    data = get_card_remain(data)
    results['data'] = data
    results['count'] = len(info)
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
