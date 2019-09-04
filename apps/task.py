import json
import logging
from tools_me.other_tools import sum_code, login_required
from . import task_blueprint
from flask import render_template, jsonify, request, g
from tools_me.mysql_tools import SqlData
from tools_me.parameter import RET, MSG


@task_blueprint.route('/', methods=['GET'])
@login_required
def account():
    user_id = g.user_id
    label_list = SqlData().search_task_all_label(user_id)
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

    return render_template("task/task.html", **context)


@task_blueprint.route('/form_input/', methods=['GET'])
@login_required
def up_task():
    user_id = g.user_id
    cus_list = SqlData().search_user_cus(user_id)
    context = {'cus_list': cus_list}
    return render_template('task/edit_task.html', **context)


@task_blueprint.route('/task_list/', methods=['GET'])
@login_required
def task_list():
    sum_order_code = request.args.get('sum_order_code')
    terrace = request.args.get('terrace')
    context = dict()
    context['sum_code'] = sum_order_code
    if terrace == "AMZ":
        return render_template('task/task_list.html', **context)
    if terrace == "SMT":
        return render_template('task/smt_task_list.html', **context)


@task_blueprint.route('/add_task/', methods=['GET'])
@login_required
def add_task():
    return render_template('task/add_task.html')


@task_blueprint.route('/finish_task', methods=['GET'])
@login_required
def finish_task():
    sum_order_code = request.args.get('sum_order_code')
    try:
        SqlData().update_task_one('sum_state', '已完成', sum_order_code)
        return jsonify({'code': RET.OK, 'msg': MSG.OK})
    except Exception as e:
        logging.error(str(e))
        return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


@task_blueprint.route('/edit_run_time', methods=['GET', 'POST'])
@login_required
def edit_run_time():
    if request.method == 'GET':
        return render_template('task/edit_run_time.html')
    elif request.method == 'POST':
        data = json.loads(request.form.get('data'))
        task_code = data.get('task_code')
        run_time = data.get('run_time')
        serve_class = data.get('serve_class')
        serve_info = ''
        if serve_class == "0":
            serve_info = ''
        elif serve_class == '1':
            serve_info = 'Review'
        elif serve_class == '2':
            serve_info = 'FeedBack'
        elif serve_class == '3':
            serve_info = 'Review/FeedBack'
        brush_hand = data.get('brush_hand')
        note = data.get('note')
        results = {'code': RET.OK, 'msg': MSG.OK}
        try:
            SqlData().update_task_detail(run_time, serve_info, brush_hand, note, task_code)
            return jsonify(results)
        except Exception as e:
            logging.error(str(e))
            results['code'] = RET.SERVERERROR
            results['msg'] = MSG.DATAERROR
            return jsonify(results)


@task_blueprint.route('/del_task', methods=['GET'])
@login_required
def del_task():
    sum_order_code = request.args.get('sum_order_code')
    task_code = request.args.get('task_code')
    user_id = g.user_id
    results = {'code': RET.OK, 'msg': MSG.OK}
    if sum_order_code:
        try:
            SqlData().del_task(sum_order_code, user_id)
            return jsonify(results)
        except Exception as e:
            logging.error(str(e))
            results['code'] = RET.SERVERERROR
            results['msg'] = MSG.DATAERROR
            return jsonify(results)
    if task_code:
        try:
            SqlData().update_order_state(task_code)
            return jsonify(results)
        except Exception as e:
            logging.error(str(e))
            results['code'] = RET.SERVERERROR
            results['msg'] = MSG.DATAERROR
            return jsonify(results)


@task_blueprint.route('/sum_info/', methods=['GET'])
@login_required
def get_task_info():
    user_id = g.user_id
    page = request.args.get('page')
    limit = request.args.get('limit')
    task_code = request.args.get('sum_order_code')
    label = request.args.get('label')
    asin = request.args.get('asin')
    sum_state = request.args.get('sum_state')
    results = {"code": RET.OK, "msg": MSG.OK, "count": 0, "data": ""}
    page_list = list()
    if not task_code and not label and not asin:
        try:
            if sum_state == "未完成":
                # task_info = cache.get('task_ed')
                # if not task_info:
                task_info = SqlData().search_task_on_code('sum_state', '', user_id)
                # cache.set('task_ed', task_info, timeout=CACHE.TIMEOUT)
            elif sum_state == "已完成":

                task_info = SqlData().search_task_on_code('sum_state', sum_state, user_id)

            elif sum_state == '':
                task_info = SqlData().search_task_parent(user_id)
                # 设置缓存查出来的订单信息缓存,60S后过期
            else:
                task_info = SqlData().search_task_parent(user_id)
                # 设置缓存查出来的订单信息缓存,60S后过期
            if len(task_info) == 0:
                return jsonify({'code': RET.SERVERERROR, 'msg': MSG.NODATA})
            task_info = list(reversed(task_info))
            for i in range(0, len(task_info), int(limit)):
                page_list.append(task_info[i:i + int(limit)])
            results['data'] = page_list[int(page) - 1]
            results['count'] = len(task_info)
        except Exception as e:
            logging.error(str(e))
            results = {"code": RET.SERVERERROR, "msg": MSG.NODATA}
        return jsonify(results)
    else:
        task_code_sql = ""
        label_sql = ""
        asin_sql = ""
        try:
            if task_code:
                task_code_sql = "AND sum_order_code LIKE '%" + task_code + "%'"
            if label:
                label_sql = "AND customer_label='" + label + "'"
            if asin:
                asin_sql = "AND asin='" + asin + "'"
            task_info = SqlData().search_task_on_asin(user_id, task_code_sql, label_sql, asin_sql)
            if len(task_info) == 0:
                return jsonify({'code': RET.SERVERERROR, 'msg': MSG.NODATA})
            task_info = list(reversed(task_info))
            for i in range(0, len(task_info), int(limit)):
                page_list.append(task_info[i:i + int(limit)])
            results['data'] = page_list[int(page) - 1]
            results['count'] = len(task_info)
            return jsonify(results)
        except Exception as e:
            logging.error(str(e))
            results = {"code": RET.SERVERERROR, "msg": MSG.NODATA}
            return jsonify(results)


@task_blueprint.route('/up_task_info/', methods=['POST'])
@login_required
def up_task_info():
    data = json.loads(request.form.get('data'))
    sum_order_code = data.get('sum_order_code')
    terrace = data.get('terrace')
    sum_num = data.get('sum_num')
    sum_money = data.get('sum_money')
    good_money = data.get('good_money')
    serve_money = data.get('serve_money')
    pay_cus = data.get('pay_cus')
    customer_label = data.get('customer_label')
    sum_time = data.get('sum_time')
    note = data.get('note')
    try:
        if terrace == '1':
            SqlData().update_task_one('terrace', 'AMZ', sum_order_code)
        if terrace == '2':
            SqlData().update_task_one('terrace', 'SMT', sum_order_code)
        if sum_num:
            SqlData().update_task_one('sum_num', int(sum_num), sum_order_code)
        if serve_money:
            SqlData().update_task_one('serve_money', float(serve_money), sum_order_code)
            label = SqlData().search_task_one_field('customer_label', sum_order_code)
            user_id = g.user_id
            middle_id = SqlData().search_cus_one_field('middle_id', user_id, label)
            if middle_id:
                discount = SqlData().search_of_middle_id('discount', int(middle_id))
                serve_money = SqlData().search_task_one_field('serve_money', sum_order_code)
                middle_money = round(serve_money * discount, 2)
                SqlData().update_task_one('middle_money', middle_money, sum_order_code)
        if good_money:
            SqlData().update_task_one('good_money', float(good_money), sum_order_code)
        if sum_money:
            SqlData().update_task_one('sum_money', float(sum_money), sum_order_code)
        if pay_cus:
            SqlData().update_task_one('pay_cus', pay_cus, sum_order_code)
            label = SqlData().search_task_one_field('customer_label', sum_order_code)
            user_id = g.user_id
            middle_id = SqlData().search_cus_one_field('middle_id', user_id, label)
            if middle_id:
                discount = SqlData().search_of_middle_id('discount', int(middle_id))
                serve_money = SqlData().search_task_one_field('serve_money', sum_order_code)
                middle_money = round(serve_money * discount, 2)
                SqlData().update_task_one('middle_money', middle_money, sum_order_code)
        if customer_label:
            SqlData().update_task_one('customer_label', customer_label, sum_order_code)
        if sum_time:
            SqlData().update_task_one('sum_time', str(sum_time), sum_order_code)
        if note:
            SqlData().update_task_one('note', note, sum_order_code)
        results = {"code": RET.OK, "msg": MSG.OK}
        return jsonify(results)
    except Exception as e:
        logging.error(str(e))
        results = {"code": RET.SERVERERROR, "msg": MSG.DATAERROR}
        return jsonify(results)


@task_blueprint.route('/task_detail/', methods=['GET'])
@login_required
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


@task_blueprint.route('/insert_task', methods=['POST'])
@login_required
def insert_task():
    user_id = g.user_id
    data = json.loads(request.form.get('data'))
    country = data.get('country')
    sum_time = data.get('sum_time')
    asin = data.get('asin')
    store_name = data.get('store_name')
    key_word = data.get('key_word')
    kw_location = data.get('kw_location')
    good_name = data.get('good_name')
    good_money = data.get('good_money')
    good_link = data.get('good_link')
    pay_method = data.get('pay_method')
    serve_class = data.get('serve_class')
    mail_method = data.get('mail_method')
    note = data.get('note')
    review_title = data.get('review_title')
    review_info = data.get('review_info')
    feedback_info = data.get('feedback_info')
    try:
        sum_order_code = sum_code()
        parent_id = SqlData().insert_task_parent(user_id, sum_order_code)
        task_code = sum_order_code + '-' + '1'
        SqlData().insert_task_detail(parent_id, task_code, country, asin, key_word, kw_location, store_name, good_name,
                                     good_money, good_link, pay_method, sum_time, serve_class, mail_method, note,
                                     review_title, review_info, feedback_info)
        return jsonify({'code': RET.OK, 'msg': RET.OK})
    except Exception as e:
        logging.error(str(e))
        return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})
