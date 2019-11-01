import json
import logging
from flask import render_template, request, jsonify
from tools_me.mysql_tools import SqlData
from tools_me.other_tools import sum_code, xianzai_time
from tools_me.parameter import RET, MSG
from tools_me.send_sms.send_sms import CCP
from . import verify_pay_blueprint


@verify_pay_blueprint.route('/')
def verify_index():
    return render_template('verify_pay/index.html')


@verify_pay_blueprint.route('/pay_log/', methods=['GET'])
def pay_log():
    results = dict()
    results['code'] = RET.OK
    results['msg'] = MSG.OK
    limit = request.args.get('limit')
    page = request.args.get('page')
    status = request.args.get('status')
    data = SqlData().search_pay_log(status)
    if not data:
        results['msg'] = MSG.NODATA
        return jsonify(results)
    info = list(reversed(data))
    page_list = list()
    for i in range(0, len(info), int(limit)):
        page_list.append(info[i:i + int(limit)])
    data = page_list[int(page) - 1]
    results['data'] = data
    results['count'] = len(data)
    return jsonify(results)


@verify_pay_blueprint.route('/top_up/', methods=['GET', 'POST'])
def top_up():
    if request.method == 'GET':
        pay_time = request.args.get('pay_time')
        cus_name = request.args.get('cus_name')
        context = dict()
        context['pay_time'] = pay_time
        context['cus_name'] = cus_name
        return render_template('verify_pay/check.html', **context)
    if request.method == 'POST':
        try:
            results = dict()
            data = json.loads(request.form.get('data'))
            pay_time = data.get('pay_time')
            cus_name = data.get('cus_name')
            check = data.get('check')
            ver_code = data.get('ver_code')
            # 校验参数验证激活码
            if check != 'yes':
                results['code'] = RET.SERVERERROR
                results['msg'] = '请确认已收款!'
                return jsonify(results)
            pass_wd = SqlData().search_pay_code('ver_code', cus_name, pay_time)
            if pass_wd != ver_code:
                results['code'] = RET.SERVERERROR
                results['msg'] = '验证码错误!'
                return jsonify(results)

            # 验证成功后,做客户账户充值
            money = SqlData().search_pay_code('top_money', cus_name, pay_time)
            pay_num = sum_code()
            t = xianzai_time()
            before = SqlData().search_user_field_name('balance', cus_name)
            balance = before + money
            user_id = SqlData().search_user_field_name('id', cus_name)
            # 更新账户余额
            SqlData().update_user_balance(money, user_id)
            # 更新客户充值记录
            SqlData().insert_top_up(pay_num, t, money, before, balance, user_id, '系统')

            # 更新pay_log的订单的充值状态
            cus_id = SqlData().search_user_field_name('id', cus_name)
            SqlData().update_pay_status('已充值', t, cus_id, pay_time)

            phone = SqlData().search_user_field_name('phone_num', cus_name)

            if phone:
                CCP().send_Template_sms(phone, [cus_name, t, money], 478898)
            results['code'] = RET.OK
            results['msg'] = MSG.OK
            return jsonify(results)
        except Exception as e:
            logging.error(str(e))
            results = dict()
            results['code'] = RET.SERVERERROR
            results['msg'] = MSG.SERVERERROR
            return jsonify(results)


@verify_pay_blueprint.route('/del_pay/', methods=['POST'])
def del_pay():
    try:
        data = json.loads(request.form.get('data'))
        user_name = data.get('user_name')
        pay_time = data.get('pay_time')
        user_id = SqlData().search_user_field_name('id', user_name)
        SqlData().del_pay_log(user_id, pay_time)
        results = dict()
        results['code'] = RET.OK
        results['msg'] = MSG.OK
        return jsonify(results)
    except Exception as e:
        logging.error(str(e))
        results = dict()
        results['code'] = RET.SERVERERROR
        results['msg'] = MSG.SERVERERROR
        return jsonify(results)
