import json
import logging
import os
from tools_me.other_tools import login_required, now_day, check_param, filter_by_time, filter_by_store, \
    filter_by_asin, xianzai_time, sum_code
from tools_me.up_pic import sm_photo
from . import order_blueprint
from flask import render_template, jsonify, request, g
from tools_me.mysql_tools import SqlData
from tools_me.parameter import RET, MSG, ORDER, PHOTO_DIR


@order_blueprint.route('/', methods=['GET'])
@login_required
def account():
    terrace = g.terrace
    context = {'user_name': g.user_name, 'terrace': terrace}
    return render_template("order/order.html", **context)


@order_blueprint.route('/repair', methods=['GET'])
@login_required
def repair():
    if request.method == 'GET':
        task_code = request.args.get('task_code')
        now_time = xianzai_time()
        SqlData().update_order_repair(now_time, task_code)
        return jsonify({'code': RET.OK, 'msg': MSG.OK})


@order_blueprint.route('/sub_review', methods=['GET', 'POST'])
@login_required
def sub_review():
    if request.method == 'GET':
        task_code = request.args.get('task_code')
        account = request.args.get('account')
        context = {'task_code': task_code, 'account': account}
        return render_template('order/sub_review.html', **context)
    if request.method == 'POST':
        # 注意更新账号的待留评状态
        user_id = g.user_id
        results = {'code': RET.OK, 'msg': MSG.OK}
        data = json.loads(request.form.get('data'))
        note = data.get('note')
        task_code = data.get('task_code')
        account = data.get('account')
        SqlData().update_review_one('task_state', '已完成', task_code)
        SqlData().update_review_one('urgent', '', task_code)
        SqlData().update_account_one('account_state', '', account, user_id)
        if note:
            SqlData().update_review_one('review_note', note, task_code)
        return jsonify(results)


@order_blueprint.route('/up_review_pic', methods=['POST'])
@login_required
def up_review_pic():
    user_id = g.user_id
    results = {'code': RET.OK, 'msg': MSG.OK}
    file = request.files.get('file')
    task_code = request.args.get('task_code')
    file_name = str(user_id) + "-" + sum_code() + ".PNG"
    file_path = PHOTO_DIR + "/" + file_name
    file.save(file_path)
    filename = sm_photo(file_path)
    if filename == 'F':
        return jsonify({'code': RET.SERVERERROR, 'msg': '不可上传相同图片,请重新上传!'})
    if filename:
        os.remove(file_path)
        phone_link = filename
        phone_info = SqlData().search_review_pic(task_code)
        if not phone_info:
            link_dict = dict()
            link_dict[phone_link] = 'one'
            link_json = json.dumps(link_dict)
            SqlData().update_review_one('pic_link', link_json, task_code)
        if phone_info:
            link_dict = json.loads(phone_info)
            link_dict[phone_link] = 'two'
            link_json = json.dumps(link_dict)
            SqlData().update_review_one('pic_link', link_json, task_code)
        return jsonify(results)
    else:
        return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


@order_blueprint.route('/one_detail/', methods=['GET'])
@login_required
def one_detail():
    task_code = request.args.get('task_code')
    results = {'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR}
    try:
        data = SqlData().search_order_task_code(task_code)
        one_detail = dict()
        one_detail['big_code'] = data[2].split('-')[0]
        one_detail['task_code'] = data[2]
        one_detail['country'] = data[3]
        one_detail['asin'] = data[4]
        one_detail['key_word'] = data[5]
        one_detail['kw_location'] = data[6]
        one_detail['store_name'] = data[7]
        one_detail['good_name'] = data[8]
        one_detail['good_money'] = data[9]
        one_detail['good_link'] = data[10]
        one_detail['mail_method'] = data[11]
        one_detail['pay_method'] = data[12]
        one_detail['serve_class'] = data[13]
        one_detail['buy_account'] = data[14]
        one_detail['account_ps'] = data[15]
        one_detail['task_run_time'] = str(data[16])
        one_detail['task_state'] = data[17]
        one_detail['brush_hand'] = data[18]
        one_detail['order_num'] = data[19]
        one_detail['good_money_real'] = data[20]
        one_detail['mail_money'] = data[21]
        one_detail['taxes_money'] = data[22]
        one_detail['sum_money'] = data[23]
        one_detail['note'] = data[24]
        one_detail['review_title'] = data[25]
        one_detail['review_info'] = data[26]
        one_detail['feedback_info'] = data[27]
        if data[28]:
            link_dict = json.loads(data[28])
            link_list = list(link_dict.keys())
            one_detail['pic_link'] = link_list
        else:
            one_detail['pic_link'] = []
        one_detail['review_note'] = data[29]
        return render_template('order/order_detail.html', **one_detail)

    except Exception as e:
        logging.error(str(e))
        return jsonify(results)


@order_blueprint.route('/del_order', methods=['GET'])
@login_required
def del_order():
    data_info = request.args.get('order_info')
    try:
        data_list = json.loads(data_info)
        try:
            for i in data_list:
                task_code = i.get('task_code')
                SqlData().update_order_state(task_code)
        except Exception as e:
            logging.error(str(e))
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})
        results = {'code': RET.OK, 'msg': MSG.OK}
        return jsonify(results)
    except Exception as e:
        logging.info("单行删除订单" + str(e))
        SqlData().update_order_state(data_info)
        results = {'code': RET.OK, 'msg': MSG.OK}
        return jsonify(results)


@order_blueprint.route('/change_time', methods=['GET', 'POST'])
@login_required
def change_time():
    if request.method == "GET":
        return render_template('order/edit_order_time.html')
    if request.method == 'POST':
        results = {'code': RET.OK, 'msg': MSG.OK}
        data = request.form.get('data')
        data = json.loads(data)
        run_time = data.get('run_time')
        data = json.loads(data.get('task_data'))
        if not data:
            results['code'] = RET.SERVERERROR
            results['msg'] = '请勾选订单修改!'
            return jsonify(results)
        task_code_list = list()
        for i in data:
            if i.get('task_state') == '已完成':
                results['code'] = RET.SERVERERROR
                results['msg'] = '已完成订单不可更改!'
                return jsonify(results)
            else:
                task_code_list.append(i.get('task_code'))
        try:
            for i in task_code_list:
                SqlData().update_order_time(run_time, i)
        except Exception as e:
            logging.error(str(e))
            results['code'] = RET.SERVERERROR
            results['msg'] = MSG.SERVERERROR
            return jsonify(results)
        return jsonify(results)


@order_blueprint.route('/sub_order', methods=['GET', 'POST'])
@login_required
def sub_order():
    if request.method == 'GET':
        return render_template('order/sub_order.html')
    elif request.method == 'POST':
        terrace = g.terrace
        results_ok = {'code': RET.OK, 'msg': MSG.OK}
        results_er = {'code': RET.SERVERERROR, 'msg': MSG.NODATA}
        data = json.loads(request.form.get('data'))
        task_code = data.get('task_code')
        account = data.get('account')
        asin = data.get('asin')
        store = data.get('store')
        serve_class = data.get('serve_class')
        order_num = data.get('order_num')
        good_money_real = data.get('good_money_real')
        mail_money = data.get('mail_money')
        taxes_money = data.get('taxes_money')
        note = data.get('note')
        SqlData().update_review_one('urgent', '', task_code)
        good_money_real = round(float(good_money_real), 3)
        if mail_money:
            mail_money = round(float(mail_money), 3)
        else:
            mail_money = 0

        if taxes_money:
            taxes_money = round(float(taxes_money), 3)
        else:
            taxes_money = 0
        sum_money = good_money_real + mail_money + taxes_money
        try:
            task_state = ''
            account_state = ''
            if terrace == 'AMZ':
                if serve_class:
                    task_state = '待留评'
                    account_state = ", account_state='待留评'"
                else:
                    task_state = '已完成'
                    account_state = ""
            if terrace == 'SMT':
                text_review = SqlData().search_order_one('review_title', task_code)
                image_review = SqlData().search_order_one('review_info', task_code)
                defalut_review = SqlData().search_order_one('feedback_info', task_code)
                if text_review or image_review or defalut_review:
                    task_state = '待留评'
                    account_state = ", account_state='待留评'"
                else:
                    task_state = '已完成'
                    account_state = ""

            SqlData().update_payed(order_num, good_money_real, mail_money, taxes_money, note, sum_money,  task_code, task_state)
            now_time = xianzai_time()
            SqlData().update_order_time(now_time, task_code)
            goods, stores, first_buy_time = SqlData().search_asin_store(account)
            if goods:
                goods_dict = json.loads(goods)
                goods_dict[asin] = xianzai_time()
                goods_json = json.dumps(goods_dict)
            else:
                goods_dict = dict()
                goods_dict[asin] = xianzai_time()
                goods_json = json.dumps(goods_dict)
            if stores:
                store_dict = json.loads(stores)
                store_dict[store] = xianzai_time()
                store_json = json.dumps(store_dict)
            else:
                store_dict = dict()
                store_dict[store] = xianzai_time()
                store_json = json.dumps(store_dict)
            if first_buy_time:
                now_time = xianzai_time()
                SqlData().update_account_have_time(sum_money, goods_json, store_json, now_time, account_state, account)
            else:
                now_time = xianzai_time()
                SqlData().update_account_no_time(sum_money, goods_json, store_json, now_time, now_time, account_state, account)
            return jsonify(results_ok)
        except Exception as e:
            logging.error(str(e))
            return jsonify(results_er)


@order_blueprint.route('/bind_account/', methods=['GET'])
@login_required
def bind_account():
    account = request.args.get('account')
    task_code = request.args.get('task_code')
    buy_account = request.args.get('buy_account')
    results_ok = {'code': RET.OK, 'msg': MSG.OK}
    results_er = {'code': RET.SERVERERROR, 'msg': MSG.NODATA}
    if buy_account:
        SqlData().update_account_state_one('', buy_account)
    try:
        password = SqlData().search_account_ps(account)
        SqlData().update_order_account(account, password, '已分配', task_code)
        SqlData().update_account_state_one('使用中', account)
        return jsonify(results_ok)
    except Exception as e:
        logging.error(str(e))
        return jsonify(results_er)


@order_blueprint.route('/filter_order/', methods=['GET'])
@login_required
def filter_order():
    user_id = g.user_id
    limit = request.args.get('limit')
    page = request.args.get('page')
    results_ok = {'code': RET.OK, 'msg': MSG.OK}
    results_er = {'code': RET.SERVERERROR, 'msg': MSG.NODATA}
    task_code = ORDER.TASK_CODE
    terrace = ORDER.TERRACE
    country = ORDER.COUNTRY
    last_buy = ORDER.LAST_BUY
    store = ORDER.STORE
    store_group = ORDER.STORE_GROUP
    asin = ORDER.ASIN
    asin_group = ORDER.ASIN_GROUP
    try:
        asin_name, store_name = SqlData().search_one_task(task_code)
    except Exception as e:
        logging.error(str(e))
        return jsonify(results_er)

    try:
        filter_of_terrace = SqlData().search_account_action('', terrace, country, user_id)
        if len(filter_of_terrace) == 0:
            return jsonify(results_er)

        match_of_time = filter_by_time(filter_of_terrace, int(last_buy))
        if len(match_of_time) == 0:
            return jsonify(results_er)

        match_of_store = filter_by_store(match_of_time, store_name, store, store_group)
        if len(match_of_store) == 0:
            return jsonify(results_er)

        match_of_asin = filter_by_asin(match_of_store, asin_name, asin, asin_group)
        if len(match_of_asin) == 0:
            return jsonify(results_er)

        data_list = list()
        try:
            label = request.args.get('label')
            account = request.args.get('account')
            price_min = request.args.get('price_min')
            price_max = request.args.get('price_max')
            if account or label or price_min or price_max:
                account_sql = ''
                label_sql = ''
                price_sql = ''
                if account:
                    account_sql = "AND account LIKE '%" + account.strip() + "%'"
                if label:
                    label_sql = "AND label='" + label.strip() + "'"
                if price_max and price_min:
                    price_min = round(float(price_min), 3)
                    price_max = round(float(price_max), 3)
                    price_sql = 'AND pay_money BETWEEN ' + str(price_min) + 'AND ' + str(price_max)
                for account_id in match_of_asin:
                    data = SqlData().search_detail_order(account_id, account=account_sql, label=label_sql, pay_money=price_sql)
                    if data != 'F':
                        data_list.append(data)
            else:
                for account_id in match_of_asin:
                    data = SqlData().search_detail_order(account_id)
                    if data != 'F':
                        data_list.append(data)
            page_list = list()
            for i in range(0, len(data_list), int(limit)):
                page_list.append(data_list[i:i + int(limit)])
            results_ok['data'] = page_list[int(page) - 1]
            results_ok['count'] = len(data_list)
            return jsonify(results_ok)

        except Exception as e:
            logging.error(str(e))
            return jsonify(results_er)

    except Exception as e:
        logging.error('分配账号失败:' + str(e))
        return jsonify(results_er)


@order_blueprint.route('/filter_html', methods=['GET'])
@login_required
def filter_html():
    user_id = g.user_id
    task_code = request.args.get('task_code')
    buy_account = request.args.get('buy_account')
    terrace = request.args.get('terrace')
    country = request.args.get('country')
    last_buy = request.args.get('last_buy')
    store = request.args.get('store')
    asin = request.args.get('asin')
    store_group = request.args.get('store_group')
    asin_group = request.args.get('asin_group')
    terrace, country, store, asin, store_group, asin_group = check_param(terrace, country, store, asin, store_group, asin_group)
    ORDER.TASK_CODE = task_code
    ORDER.TERRACE = terrace
    ORDER.COUNTRY = country
    ORDER.LAST_BUY = last_buy
    ORDER.STORE = store
    ORDER.ASIN = asin
    ORDER.STORE_GROUP = store_group
    ORDER.ASIN_GROUP = asin_group
    context = dict()
    try:
        label_list = SqlData().search_account_label(user_id)

        if len(label_list) == 0:
            context['label'] = []
        else:
            # 去重
            new_list = list(set(label_list))
            new_list.sort(key=label_list.index)
            # 去空
            new_list = [x for x in new_list if x != '']
            context['label'] = new_list

    except Exception as e:
        logging.error(str(e))
        return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})

    context['task_code'] = task_code
    context['buy_account'] = buy_account
    return render_template('order/allot_order.html', **context)


@order_blueprint.route('/order_detail', methods=['GET'])
@login_required
def order_detail():
    user_id = g.user_id
    t1 = now_day() + ' 00:00:00'
    t2 = now_day() + ' 23:59:59'
    page = request.args.get('page')
    limit = request.args.get('limit')
    buy_state = request.args.get('buy_state')
    task_code = request.args.get('task_code')
    asin = request.args.get('asin')
    order_num = request.args.get('order_num')
    results = {"code": RET.OK, "msg": MSG.OK, "count": 0, "data": ""}
    page_list = list()
    try:
        if not task_code and not asin and not order_num:
            task_info = ''
            if not buy_state:
                task_info = SqlData().search_now_order(t1, t2, user_id)
            elif buy_state == '已分配' or buy_state == '已完成' or buy_state == '待留评':
                task_info = SqlData().search_order_of_state(buy_state, user_id)
            elif buy_state == '已逾期':
                task_info = SqlData().search_order_of_overdue(t1, user_id)
            task_info = list(reversed(task_info))
            for i in range(0, len(task_info), int(limit)):
                page_list.append(task_info[i:i + int(limit)])
            results['data'] = page_list[int(page) - 1]
            results['count'] = len(task_info)
            return results
        else:
            task_sql = ''
            asin_sql = ''
            order_sql = ''
            if task_code:
                task_sql = "AND task_code='" + task_code + "'"
            if asin:
                asin_sql = "AND asin='" + asin + "'"
            if order_num:
                order_sql = "AND order_num='" + task_code + "'"
            task_info = SqlData().search_all_order(user_id, task_sql, asin_sql, order_sql)
            if len(task_info) == 0:
                results['code'] = RET.SERVERERROR
                results['msg'] = MSG.NODATA
                return results
            for i in range(0, len(task_info), int(limit)):
                page_list.append(task_info[i:i + int(limit)])
            results['data'] = page_list[int(page) - 1]
            results['count'] = len(task_info)
            return results

    except Exception as e:
        logging.warning('没有符合条件的数据' + str(e))
        results['code'] = RET.SERVERERROR
        results['msg'] = MSG.NODATA
        return results
