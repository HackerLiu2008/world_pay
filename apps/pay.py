import datetime
import logging
import uuid

from flask import render_template, request, json, jsonify

from tools_me.mysql_tools import SqlData
from tools_me.other_tools import time_str, xianzai_time
from tools_me.parameter import RET, MSG, DIR_PATH
from tools_me.send_email import send
from . import pay_blueprint


@pay_blueprint.route('/', methods=['GET'])
def index_pay():
    ex_change = SqlData().search_admin_field('ex_change')
    ex_range = SqlData().search_admin_field('ex_range')
    hand = SqlData().search_admin_field('hand')
    dollar_hand = SqlData().search_admin_field('dollar_hand')
    context = dict()
    context['ex_change'] = ex_change
    context['ex_range'] = ex_range
    context['hand'] = hand
    context['dollar_hand'] = dollar_hand
    return render_template('pay/index.html', **context)


@pay_blueprint.route('/acc_top_cn/', methods=['POST'])
def top_cn():
    if request.method == 'POST':
        '''
        1:校验前端数据是否正确
        2:查看实时汇率有没有变动
        3:核实客户是否存在
        '''
        data = json.loads(request.form.get('data'))
        sum_money = data.get('sum_money')
        top_money = data.get('top_money')
        cus_name = data.get('cus_name')
        cus_account = data.get('cus_account')
        res = SqlData().search_user_check(cus_name, cus_account)
        if not res:
            return jsonify({'code': RET.SERVERERROR, 'msg': '没有该用户!请核实后重试!'})
        ex_change = SqlData().search_admin_field('ex_change')
        ex_range = SqlData().search_admin_field('ex_range')
        hand = SqlData().search_admin_field('hand')
        _money_self = float(top_money) * (ex_change + ex_range) * (hand + 1)
        money_self = round(_money_self, 10)
        sum_money = round(float(sum_money), 10)
        if money_self == sum_money:
            return jsonify({'code': RET.OK, 'msg': MSG.OK})
        else:
            return jsonify({'code': RET.SERVERERROR, 'msg': '汇率已变动!请刷新界面后重试!'})


@pay_blueprint.route('/acc_top_dollar/', methods=['POST'])
def top_dollar():
    if request.method == 'POST':
        '''
        1:校验前端数据是否正确
        2:查看实时汇率有没有变动
        3:核实客户是否存在
        '''
        data = json.loads(request.form.get('data'))
        sum_money = data.get('sum_money')
        top_money = data.get('top_money')
        cus_name = data.get('cus_name')
        cus_account = data.get('cus_account')
        res = SqlData().search_user_check(cus_name, cus_account)
        if not res:
            return jsonify({'code': RET.SERVERERROR, 'msg': '没有该用户!请核实后重试!'})
        dollar = SqlData().search_admin_field('dollar_hand')
        _money_self = float(top_money) * (dollar + 1)
        money_self = round(_money_self, 10)
        sum_money = round(float(sum_money), 10)
        if money_self == sum_money:
            return jsonify({'code': RET.OK, 'msg': MSG.OK})
        else:
            return jsonify({'code': RET.SERVERERROR, 'msg': '手续费已变动!请刷新界面后重试!'})


@pay_blueprint.route('/pay_pic/', methods=['GET', 'POST'])
def pay_pic():
    if request.method == 'GET':
        sum_money = request.args.get('sum_money')
        top_money = request.args.get('top_money')
        cus_name = request.args.get('cus_name')
        cus_account = request.args.get('cus_account')
        context = dict()
        context['sum_money'] = sum_money
        context['top_money'] = top_money
        context['cus_name'] = cus_name
        context['cus_account'] = cus_account
        return render_template('pay/pay_pic.html', **context)
    if request.method == 'POST':
        '''
        获取充值金额, 保存付款截图. 发送邮件通知管理员
        '''
        try:

            data = json.loads(request.form.get('data'))
            top_money = data.get('top_money')
            sum_money = data.get('sum_money')
            cus_name = data.get('cus_name')
            cus_account = data.get('cus_account')
            results = {'code': RET.OK, 'msg': MSG.OK}
            file = request.files.get('file')
            now_time = time_str()
            file_name = cus_name + "_" + now_time + ".png"
            file_path = DIR_PATH.PHOTO_DIR + file_name
            file.save(file_path)
            n_time = xianzai_time()
            vir_code = str(uuid.uuid1())[:6]
            context = "客户:  " + cus_name + " , 于" + n_time + "在线申请充值: " + top_money + "美元, 折和人名币: " + sum_money + "元。 验证码为: " + vir_code

            cus_id = SqlData().search_user_check(cus_name, cus_account)
            sum_money = float(sum_money)
            top_money = float(top_money)
            SqlData().insert_pay_log(n_time, sum_money, top_money, vir_code, '待充值', cus_id)

            # 获取要推送邮件的邮箱
            top_push = SqlData().search_admin_field('top_push')
            top_dict = json.loads(top_push)
            email_list = list()
            for i in top_dict:
                email_list.append(top_dict.get(i))
            for p in email_list:
                send(context, file_name, p)

            return jsonify(results)
        except Exception as e:
            logging.error(str(e))
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})
