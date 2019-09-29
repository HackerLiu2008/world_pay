import json
import logging
from tools_me.mysql_tools import SqlData
from flask import request, render_template, jsonify, session, g
from tools_me.other_tools import middle_required, get_nday_list, now_year
from tools_me.parameter import RET, MSG
from . import middle_blueprint


@middle_blueprint.route('/change_phone', methods=['GET'])
@middle_required
def change_phone():
    middle_id = g.middle_id
    phone_num = request.args.get('phone_num')
    results = dict()
    try:
        SqlData().update_middle_field('phone_num', phone_num, middle_id)
        results['code'] = RET.OK
        results['msg'] = MSG.OK
        return jsonify(results)
    except Exception as e:
        logging.error(str(e))
        results['code'] = RET.SERVERERROR
        results['msg'] = MSG.SERVERERROR
        return jsonify(results)


@middle_blueprint.route('/logout', methods=['GET'])
@middle_required
def logout():
    session.pop('middle_id')
    return render_template('middle/login_middle.html')


@middle_blueprint.route('/middle_info', methods=['GET'])
@middle_required
def user_info():
    middle_id = g.middle_id
    dict_info = SqlData().search_middle_detail(middle_id)
    account = dict_info.get('account')
    phone_num = dict_info.get('phone_num')
    card_price = dict_info.get('card_price')
    context = {
        'account': account,
        'card_price': card_price,
        'phone_num': phone_num,
    }
    return render_template('middle/middle_info.html', **context)


@middle_blueprint.route('/middle_money', methods=['GET'])
@middle_required
def middle_money():
    # 编写定时脚本:每周三统计上周三至本周二中介下的客户开卡数量插入到middle_money表
    # 1,所有中介;2,每一个中介下的所有客户,计算费用和数量

    # 根据id查寻middle_money表返回统计的开卡数量
    results = dict()
    results['code'] = RET.OK
    results['msg'] = MSG.OK
    results['data'] = [{'start_time': '2019-08-08', 'end_time': '2019-09-09'}]
    return jsonify(results)


# 根据缓存中介缓存id查询客户,在根据客户id查询用的卡数量
@middle_blueprint.route('/customer_info', methods=['GET'])
@middle_required
def task_list():
    if request.method == 'GET':
        try:
            user_id = g.middle_user_id
            middle_id = g.middle_id
            limit = request.args.get('limit')
            page = request.args.get('page')
            info_list = SqlData().search_task_on_middle(str(middle_id), user_id)
            if not info_list:
                return jsonify({'code': RET.OK, 'msg': MSG.NODATA})
            page_list = list()
            results = dict()
            results['code'] = RET.OK
            results['msg'] = MSG.OK
            info_list = list(reversed(info_list))
            for i in range(0, len(info_list), int(limit)):
                page_list.append(info_list[i:i + int(limit)])
            results['data'] = page_list[int(page) - 1]
            results['count'] = len(info_list)
            return jsonify(results)
        except Exception as e:
            logging.error(str(e))
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


# 查询折线图数据(today, week, month)
@middle_blueprint.route('/line_chart', methods=['GET'])
@middle_required
def test():
    l = []
    for i in range(30):
        l.append(i)
    s = []
    for i in range(25, 40):
        s.append(i)
    month = [{'name': 'liuxiao', 'data': l},{'name':'刘总', 'data': s}]
    results = dict()
    results['code'] = RET.OK
    results['msg'] = MSG.OK
    results['data'] = month
    return jsonify(results)


@middle_blueprint.route('/', methods=['GET', 'POST'])
@middle_required
def middle_index():
    if request.method == 'GET':
        middle_id = g.middle_id
        day_list = get_nday_list(30)
        year = now_year()
        context = dict()
        context['day_list'] = day_list
        context['year'] = year
        name = SqlData().search_middle_field('name', middle_id)
        context['name'] = name
        return render_template('middle/index.html', **context)


@middle_blueprint.route('/login', methods=['GET', 'POST'])
def middle_login():
    if request.method == 'GET':
        return render_template('middle/login_middle.html')
    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        account = data.get('account')
        pass_word = data.get('password')
        info = SqlData().search_middle_login(account)
        if not info:
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.PSWDERROR})
        middle_id = info[0][0]
        password = info[0][1]
        if pass_word != password:
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.PSWDERROR})
        else:
            session['middle_id'] = middle_id
            return jsonify({'code': RET.OK, 'msg': MSG.OK})
