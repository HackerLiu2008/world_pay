import json
import logging

from tools_me.mysql_tools import SqlData
from flask import request, render_template, jsonify, session, g
from tools_me.other_tools import middle_required
from tools_me.parameter import RET, MSG
from . import middle_blueprint


@middle_blueprint.route('/task_detail/', methods=['GET'])
@middle_required
def task_detail():
    sum_order_code = request.args.get('sum_order_code')
    page = request.args.get('page')
    limit = request.args.get('limit')
    results = {"code": RET.OK, "msg": MSG.OK, "count": 0, "data": ""}
    page_list = list()
    try:
        task_info = SqlData().search_task_detail(sum_order_code)
        # task_info = list(reversed(task_info))
        for i in range(0, len(task_info), int(limit)):
            page_list.append(task_info[i:i + int(limit)])
        results['data'] = page_list[int(page) - 1]
        results['count'] = len(task_info)
    except Exception as e:
        logging.warning('没有符合条件的数据' + str(e))
        results['code'] = RET.SERVERERROR
        results['msg'] = MSG.NODATA
    return results


@middle_blueprint.route('/order_html/', methods=['GET'])
@middle_required
def task_html():
    sum_order_code = request.args.get('sum_order_code')
    terrace = request.args.get('terrace')
    context = dict()
    context['sum_code'] = sum_order_code
    if terrace == "AMZ":
        return render_template('middle/amz_order_list.html', **context)
    if terrace == "SMT":
        return render_template('middle/smt_task_list.html', **context)


@middle_blueprint.route('/task_list', methods=['GET'])
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


@middle_blueprint.route('/', methods=['GET', 'POST'])
@middle_required
def middle_index():
    if request.method == 'GET':
        return render_template('middle/index.html')


@middle_blueprint.route('login', methods=['GET', 'POST'])
def middle_login():
    if request.method == 'GET':
        return render_template('middle/login.html')
    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        main_user = data.get('mainName')
        account = data.get('userName')
        pass_word = data.get('nuse')
        data_info = SqlData().search_middle_login(main_user, account, pass_word)
        if not data_info:
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.PSWDERROR})
        else:
            info = data_info[0]
            session['middle_id'] = info[0]
            session['middle_user_id'] = info[1]
            session['middle_name'] = info[2]
            return jsonify({'code': RET.OK, 'msg': MSG.OK})
