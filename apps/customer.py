import datetime
import json
import logging
import os
import xlrd
from tools_me.other_tools import customer_required, save_file, excel_to_data, asin_num, sum_code, xianzai_time, \
    date_to_week, transferContent
from tools_me.parameter import RET, MSG, TASK_DIR, PHOTO_DIR
from tools_me.up_pic import up_photo
from . import customer_blueprint
from flask import render_template, request, jsonify, session, g
from tools_me.mysql_tools import SqlData


@customer_blueprint.route('/up_review_pic', methods=['POST'])
@customer_required
def up_review_pic():
    user_id = g.cus_user_id
    results = {'code': RET.OK, 'msg': MSG.OK}
    file = request.files.get('file')
    task_code = request.args.get('task_code')
    image_state = SqlData().search_order_one('review_info', task_code)
    if not image_state:
        return jsonify({'code': RET.SERVERERROR, 'msg': '此订单不支持上传图片'})
    bucket_name = 'pay_pic'
    file_name = str(user_id) + "-" + sum_code() + ".PNG"
    file_path = PHOTO_DIR + "/" + file_name
    file.save(file_path)
    status_code, filename = up_photo(file_name, file_path, bucket_name)
    if status_code == 200:
        os.remove(file_path)
        if image_state == 'T':
            phone_link = dict()
            phone_link[filename] = 1
            link_json = json.dumps(phone_link, ensure_ascii=False)
            SqlData().update_review_one('review_info', link_json, task_code)
        else:
            phone_link = json.loads(image_state)
            if len(phone_link) == 4:
                return jsonify({'code': RET.SERVERERROR, 'msg': '最多可上传四张图片'})
            phone_link[filename] = 1
            link_json = json.dumps(phone_link, ensure_ascii=False)
            SqlData().update_review_one('review_info', link_json, task_code)
        return jsonify(results)
    else:
        return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


@customer_blueprint.route('/edit_smt', methods=['GET', 'POST'])
@customer_required
def edit_smt():
    if request.method == 'GET':
        task_code = request.args.get('task_code')
        context = {'task_code': task_code}
        return render_template('customer/smt_review.html', **context)
    if request.method == 'POST':
        try:
            data = json.loads(request.form.get('data'))
            task_code = request.args.get('task_code')
            review_title = data.get('review_title')
            title_state = SqlData().search_order_one('review_title', task_code)
            if title_state != "T":
                return jsonify({'code': RET.SERVERERROR, 'msg': '此订单不可添加文字留评'})
            if review_title:
                SqlData().update_review_one('review_title', review_title, task_code)
            results = {'code': RET.OK, 'msg': MSG.OK}
            return jsonify(results)
        except Exception as e:
            logging.error(str(e))
            results = {'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR}
            return jsonify(results)


@customer_blueprint.route('/edit_review', methods=['GET', 'POST'])
@customer_required
def edit_review():
    if request.method == 'GET':
        return render_template('customer/edit_review.html')
    if request.method == 'POST':
        try:
            data = json.loads(request.form.get('data'))
            task_code = data.get('task_code')
            review_title = data.get('review_title')
            review_info = data.get('review_info')
            feedback_info = data.get('feedback_info')
            serve = SqlData().search_order_one('serve_class', task_code)
            if review_title:
                if 'REVIEW' in serve.upper():
                    SqlData().update_review_one('review_title', review_title, task_code)
                else:
                    results = {'code': RET.SERVERERROR, 'msg': '次订单没有编辑评论信息权限!'}
                    return jsonify(results)
            if review_info:
                if 'REVIEW' in serve.upper():
                    SqlData().update_review_one('review_info', review_info, task_code)
                else:
                    results = {'code': RET.SERVERERROR, 'msg': '次订单没有编辑评论信息权限!'}
                    return jsonify(results)
            if feedback_info:
                if 'FEEDBACK' in serve.upper():
                    SqlData().update_review_one('feedback_info', feedback_info, task_code)
                else:
                    results = {'code': RET.SERVERERROR, 'msg': '次订单没有编辑Feedback信息权限!'}
                    return jsonify(results)
            results = {'code': RET.OK, 'msg': MSG.OK}
            return jsonify(results)
        except Exception as e:
            logging.error(str(e))
            results = {'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR}
            return jsonify(results)


@customer_blueprint.route('/edit_sum', methods=['GET', 'POST'])
@customer_required
def edit_sum():
    if request.method == 'GET':
        sum_order_code = request.args.get('sum_order_code')
        context = {'sum_order_code': sum_order_code}
        return render_template('customer/sub_pay.html', **context)
    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        sum_order_code = data.get('sum_order_code')
        note = data.get('note')
        if note:
            SqlData().update_task_one('note', note, sum_order_code)
        results = {'code': RET.OK, 'msg': MSG.OK}
        return jsonify(results)


@customer_blueprint.route('/up_pay_pic', methods=['POST'])
@customer_required
def up_pay_pic():
    user_id = g.cus_user_id
    results = {'code': RET.OK, 'msg': MSG.OK}
    file = request.files.get('file')
    sum_order_code = request.args.get('sum_order_code')
    bucket_name = 'pay_pic'
    file_name = str(user_id) + "-" + sum_order_code + ".PNG"
    file_path = PHOTO_DIR + "/" + file_name
    file.save(file_path)
    status_code, filename = up_photo(file_name, file_path, bucket_name)
    if status_code == 200:
        os.remove(file_path)
        SqlData().update_task_one('deal_num', filename, sum_order_code)
        return jsonify(results)
    else:
        return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


@customer_blueprint.route('/task_choose', methods=['GET', 'POST'])
@customer_required
def task_choose():
    user_id = g.cus_user_id
    label = g.cus_label
    cus_id = g.cus_id
    if request.method == 'GET':
        SqlData().update_user_cus('task_json', '', user_id, label)
        return jsonify({'code': RET.OK, 'msg': MSG.OK})

    if request.method == 'POST':
        task_json = SqlData().search_cus_field('task_json', cus_id)
        task_dict = json.loads(task_json)

        task_list = task_dict.get('task_info')
        serve_money = task_dict.get('serve_money')
        good_sum_money = task_dict.get('good_sum_money')
        terrace = task_dict.get('terrace')
        sum_num = task_dict.get('sum_num')
        discount = SqlData().search_cus_field('discount', cus_id)
        serve_dis = "%.2f" % (serve_money * float(discount))
        exchange = SqlData().search_user_field('dollar_exchange', user_id)
        good_dis = "%.2f" % (good_sum_money * float(exchange))
        sum_money = float(serve_dis) + float(good_dis)

        sum_order_code = sum_code()
        parent_id = SqlData().insert_task_parent(user_id, sum_order_code)

        SqlData().update_task_one('terrace', terrace, sum_order_code)
        SqlData().update_task_one('sum_num', sum_num, sum_order_code)
        SqlData().update_task_one('serve_money', float(serve_dis), sum_order_code)
        SqlData().update_task_one('good_money', float(good_dis), sum_order_code)
        SqlData().update_task_one('sum_money', sum_money, sum_order_code)
        now_time = xianzai_time()
        SqlData().update_task_one('sum_time', now_time, sum_order_code)
        label = g.cus_label
        SqlData().update_task_one('customer_label', label, sum_order_code)

        index = 1
        for i in task_list:
            task_code = sum_order_code + '-' + str(index)
            country = i[0]
            task_run_time = i[1]
            asin = i[2]
            key_word = i[3]
            kw_location = i[4]
            store_name = i[5]
            good_name = i[6]
            good_money = i[7]
            good_link = i[8]
            pay_method = i[9]
            serve_class = i[10]
            mail_method = i[11]
            note = i[12]
            review_title = i[13]
            review_info = i[14]
            feedback_info = i[15]
            try:
                SqlData().insert_task_detail(parent_id, task_code, country, asin, key_word, kw_location, store_name,
                                             good_name, good_money, good_link, pay_method, task_run_time, serve_class,
                                             mail_method, note, review_title, review_info, feedback_info)
                index += 1
            except Exception as e:
                logging.error(str(e))
                return jsonify({'code': RET.SERVERERROR, 'msg': '上传失败!'})
        SqlData().update_user_cus('task_json', '', user_id, label)
        return jsonify({'code': RET.OK, 'msg': MSG.OK})


@customer_blueprint.route('/preview_index', methods=['GET'])
@customer_required
def preview_index():
    cus_id = g.cus_id
    user_id = g.cus_user_id
    task_json = SqlData().search_cus_field('task_json', cus_id)
    if not task_json:
        return '请先导入表格文件!'
    task_dict = json.loads(task_json)
    serve_money = task_dict.get('serve_money')
    good_sum_money = task_dict.get('good_sum_money')
    terrace = task_dict.get('terrace')
    sum_num = task_dict.get('sum_num')
    discount = SqlData().search_cus_field('discount', cus_id)
    serve_dis = "%.2f" % (serve_money * float(discount))
    exchange = SqlData().search_user_field('dollar_exchange', user_id)
    good_dis = "%.2f" % (good_sum_money * float(exchange))
    sum_money = float(serve_dis) + float(good_dis)
    context = dict()
    context['serve_money'] = str(serve_dis) + " = " + str(serve_money) + "(服务费总额)" + "*" + str(float(discount)) + "(折扣)"
    context['good_money'] = str(good_dis) + " = " + str(good_sum_money) + "(商品金额总额)" + "*" + str(float(exchange)) + "(汇率)"
    context['sum_money'] = str(sum_money)
    context['terrace'] = terrace
    context['sum_num'] = sum_num
    return render_template('customer/preview_task.html', **context)


@customer_blueprint.route('/smt_choose', methods=['GET', 'POST'])
@customer_required
def smt_choose():
    user_id = g.cus_user_id
    label = g.cus_label
    cus_id = g.cus_id
    if request.method == 'GET':
        SqlData().update_user_cus('task_json', '', user_id, label)
        return jsonify({'code': RET.OK, 'msg': MSG.OK})

    if request.method == 'POST':
        task_json = SqlData().search_cus_field('task_json', cus_id)
        task_dict = json.loads(task_json)

        task_list = task_dict.get('task_info')
        serve_money = float(task_dict.get('serve_money')) + float(task_dict.get('other_money'))
        good_sum_money = task_dict.get('good_money')
        terrace = task_dict.get('terrace')
        sum_num = task_dict.get('sum_num')
        sum_money = float(task_dict.get('sum_money'))

        sum_order_code = sum_code()
        parent_id = SqlData().insert_task_parent(user_id, sum_order_code)

        SqlData().update_task_one('terrace', terrace, sum_order_code)
        SqlData().update_task_one('sum_num', sum_num, sum_order_code)
        SqlData().update_task_one('serve_money', serve_money, sum_order_code)
        SqlData().update_task_one('good_money', good_sum_money, sum_order_code)
        SqlData().update_task_one('sum_money', sum_money, sum_order_code)
        now_time = xianzai_time()
        SqlData().update_task_one('sum_time', now_time, sum_order_code)
        label = g.cus_label
        SqlData().update_task_one('customer_label', label, sum_order_code)

        index = 1
        for i in task_list:
            task_code = sum_order_code + '-' + str(index)
            country = i[1]
            task_run_time = i[0]
            store_name = i[2]
            key_word = i[3]
            asin = i[4]
            good_search_money = i[5]
            good_link = i[6]
            mail_method = i[7]
            sku = i[8]
            good_money = i[9]
            mail_money = i[10]
            text_review = i[11]
            image_review = i[12]
            if len(i) == 14:
                default_review = i[13]
            else:
                default_review = ''
            kw_location = ""
            note = ""
            # good_search_money=AMZ.good_name, sku=AMZ.pay_method, mail_money=AMZ.serve_class, text_review=AMZ.review_t
            # itle, image_review=AMZ.review_info, default_review=AMZ.feedback_info
            try:
                SqlData().insert_task_detail(parent_id, task_code, country, asin, key_word, kw_location, store_name,
                                             good_search_money, good_money, good_link, sku, task_run_time, mail_money,
                                             mail_method, note, text_review, image_review, default_review)
                index += 1
            except Exception as e:
                logging.error(str(e))
                return jsonify({'code': RET.SERVERERROR, 'msg': '上传失败!'})
        SqlData().update_user_cus('task_json', '', user_id, label)
        return jsonify({'code': RET.OK, 'msg': MSG.OK})


@customer_blueprint.route('/smt_preview', methods=['GET'])
@customer_required
def smt_preview():
    if request.method == 'GET':
        try:
            cus_id = g.cus_id
            user_id = g.cus_user_id
            label = g.cus_label
            method = request.args.get('method')
            task_json = SqlData().search_cus_field('task_json', cus_id)
            if not task_json:
                return '请先导入表格文件!'
            task_dict = json.loads(task_json)
            task_info = task_dict.get('task_info')
            sum_num = task_dict.get('sum_num')
            terrace = task_dict.get('terrace')
            good_sum_money = task_dict.get('good_sum_money')
            mail_sum_money = task_dict.get('mail_sum_money')
            text_num = task_dict.get('text_num')
            image_num = task_dict.get('image_num')
            sunday_num = task_dict.get('sunday_num')

            discount = SqlData().search_cus_field('discount', cus_id)

            exchange_dis = SqlData().search_cus_field('exchange_dis', cus_id)

            exchange = SqlData().search_user_field('dollar_exchange', user_id)

            smt_serve = SqlData().search_user_field('amz_serve', user_id)

            smt_dict = json.loads(smt_serve)
            bili = smt_dict.get('bili')
            bili = bili / 100
            default = round(sum_num * bili)
            for i in task_info[:default]:
                i.append('T')
            task_dict['task_info'] = task_info
            SqlData().update_user_cus('task_json', task_info, user_id, label)
            pc_money = smt_dict.get('pc_money')
            app_money = smt_dict.get('app_money')
            text_money = smt_dict.get('text_money')
            image_money = smt_dict.get('image_money')
            sunday_money = smt_dict.get('sunday_money')
            if not all([pc_money, app_money, text_money, image_money, sunday_money]):
                return '请联系服务商完善收费标准!'
            good_sum_money = float("%.3f" %(good_sum_money))
            mail_sum_money = float("%.3f" %(mail_sum_money))
            s = (good_sum_money + mail_sum_money) * exchange * exchange_dis
            if method == 'PC':
                money = float(pc_money)
                q = sum_num * float(pc_money) * discount
            else:
                # APP
                money = float(pc_money)
                q = sum_num * float(app_money) * discount
            text = text_num * float(text_money)
            image = image_num * float(image_money)
            sunday = sunday_num * float(sunday_money)
            other_money = text + image + sunday
            context = dict()
            context['serve_money'] = str(q) + " = " + str(sum_num * float(money)) + "(服务费总额)" + "*" + str(float(discount)) + "(折扣)"
            context['good_money'] = str(s) + " = (" + str(good_sum_money) + "(商品金额总额)+" + str(mail_sum_money) + '(邮费总额)) ' + "*" + str(float(exchange)) + "(汇率) *" + str(float(exchange_dis)) + '折扣'
            context['other_money'] = str(other_money) + "=" + str(text)+"(文字留评) +" + str(image) + "(图片留评) +" + str(sunday) + "(周日留评)"
            context['sum_money'] = "%.2f" % (q + s + other_money)
            context['sum_num'] = sum_num
            context['terrace'] = terrace
            task_dict['sum_money'] = "%.2f" % (q + s + other_money)
            task_dict['serve_money'] = str(q)
            task_dict['good_money'] = str(s)
            task_dict['other_money'] = str(other_money)
            task_json = json.dumps(task_dict, ensure_ascii=False)
            SqlData().update_user_cus('task_json', task_json, user_id, label)
            return render_template('customer/smt_preview_task.html', **context)
        except Exception as e:
            logging.error(str(e))
            return jsonify({'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR})


@customer_blueprint.route('/smt_up_preview', methods=['GET', 'POST'])
@customer_required
def smt_up_preview():
    cus_id = g.cus_id
    results = {'code': RET.OK, 'msg': MSG.OK}
    if request.method == 'GET':
        limit = request.args.get('limit')
        page = request.args.get('page')
        task_json = SqlData().search_cus_field('task_json', cus_id)
        task_dict = json.loads(task_json)
        task_list = task_dict.get('task_info')
        data = list()
        for i in task_list:
            one_dict = dict()
            one_dict['task_run_time'] = i[1]
            one_dict['country'] = i[0]
            one_dict['store_name'] = i[2]
            one_dict['key_word'] = i[3]
            one_dict['asin'] = i[4]
            one_dict['good_search_money'] = i[5]
            one_dict['good_link'] = i[6]
            one_dict['mail_method'] = i[7]
            one_dict['sku'] = i[8]
            one_dict['good_money'] = i[9]
            one_dict['mail_money'] = i[10]
            one_dict['text_review'] = i[11]
            one_dict['image_review'] = i[12]
            if len(i) == 14:
                one_dict['default_review'] = i[13]
            else:
                one_dict['default_review'] = ''
            data.append(one_dict)
        page_list = list()
        for i in range(0, len(data), int(limit)):
            page_list.append(data[i:i + int(limit)])
        results['data'] = page_list[int(page) - 1]
        results['count'] = len(data)
        return results


@customer_blueprint.route('/smt_task', methods=['GET', 'POST'])
@customer_required
def smt_task():
    if request.method == 'GET':
        return render_template('customer/cus_smt_task.html')

    # 预存表格数据到task_json字段中
    if request.method == 'POST':
        file = request.files.get('file')
        filename = file.filename
        file_path = save_file(file, filename, TASK_DIR)
        results = {'code': RET.OK, 'data': MSG.OK}
        user_id = g.cus_user_id
        try:
            if 'static' in file_path:
                data = xlrd.open_workbook(file_path, encoding_override='utf-8')
                table = data.sheets()[0]
                nrows = table.nrows  # 行数
                ncols = table.ncols  # 列数
                row_list = [table.row_values(i) for i in range(0, nrows)]  # 所有行的数据
                col_list = [table.col_values(i) for i in range(0, ncols)]  # 所有列的数
                # 验证参数是否空缺
                index = 1
                err_list = list()
                for i in row_list[1:]:
                    index += 1
                    if not all([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]]):
                        err_list.append(str(index))
                if len(err_list) != 0:
                    results['code'] = RET.SERVERERROR
                    m = ""
                    for i in err_list:
                        m = m + i + ','
                    results['msg'] = "第" + m + "行缺少必填参数!"
                    return jsonify(results)

                # 以下是计算服务费
                good_money = col_list[9][1:]
                mail_money_list = col_list[10][1:]
                # 计算全部商品本金
                good_sum_money = 0
                for i in good_money:
                    good_sum_money += float(i)
                #  计算邮费
                mail_sum_money = 0
                for n in mail_money_list:
                    mail_sum_money += float(n)

                # 计算文字留评数量
                text_review = col_list[11][1:]
                text_num = 0
                for t in text_review:
                    if t.upper() == 'T':
                        text_num += 1

                # 计算图片留评数量
                image_review = col_list[12][1:]
                image_num = 0
                for i in image_review:
                    if i == 'T':
                        image_num += 1

                time_list = col_list[0][1:]
                sunday_num = 0
                for t in time_list:
                    time_str = excel_to_data(t)
                    if date_to_week(time_str) == 6:
                        sunday_num += 1

                # 计算下单数量
                sum_num = len(time_list)

                task_info_list = list()
                for one in row_list[1:]:
                    one_task_list = list()
                    if not one[0]:
                        task_run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        task_run_time = excel_to_data(one[0])
                    country = one[1].strip()
                    store_name = one[2].strip()
                    key_word = one[3].strip()
                    asin = one[4].strip()
                    good_search_money = float(one[5])
                    good_link = one[6].strip()
                    mail_method = one[7].strip()
                    sku = one[8]
                    good_money = one[9]
                    mail_money = one[10]
                    review_text = one[11]
                    review_image = one[12]
                    one_task_list.append(task_run_time)
                    one_task_list.append(country)
                    one_task_list.append(store_name)
                    one_task_list.append(key_word)
                    one_task_list.append(asin)
                    one_task_list.append(good_search_money)
                    one_task_list.append(good_link)
                    one_task_list.append(mail_method)
                    one_task_list.append(sku)
                    one_task_list.append(good_money)
                    one_task_list.append(mail_money)
                    one_task_list.append(review_text)
                    one_task_list.append(review_image)
                    task_info_list.append(one_task_list)
                task_info_dict = dict()
                task_info_dict['task_info'] = task_info_list

                task_info_dict['sum_num'] = sum_num

                task_info_dict['terrace'] = 'SMT'

                task_info_dict['good_sum_money'] = good_sum_money

                task_info_dict['mail_sum_money'] = mail_sum_money

                task_info_dict['text_num'] = text_num

                task_info_dict['image_num'] = image_num

                task_info_dict['sunday_num'] = sunday_num
                # print(task_info_dict)
                task_info_json = json.dumps(task_info_dict, ensure_ascii=False)

                label = g.cus_label
                SqlData().update_user_cus('task_json', task_info_json, user_id, label)

                return jsonify(results)
        except Exception as e:
            logging.error(str(e))
            return '请联系服务商拟定收费规则!'

    else:
        results = {'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR}
        return jsonify(results)


@customer_blueprint.route('/preview', methods=['GET', 'POST'])
@customer_required
def preview_task():
    cus_id = g.cus_id
    results = {'code': RET.OK, 'msg': MSG.OK}
    if request.method == 'GET':
        limit = request.args.get('limit')
        page = request.args.get('page')
        task_json = SqlData().search_cus_field('task_json', cus_id)
        task_dict = json.loads(task_json)
        task_list = task_dict.get('task_info')
        data = list()
        for i in task_list:
            one_dict = dict()
            one_dict['country'] = i[0]
            one_dict['task_run_time'] = i[1]
            one_dict['asin'] = i[2]
            one_dict['key_word'] = i[3]
            one_dict['kw_location'] = i[4]
            one_dict['store_name'] = i[5]
            one_dict['good_name'] = i[6]
            one_dict['good_money'] = i[7]
            one_dict['good_link'] = i[8]
            one_dict['pay_method'] = i[9]
            one_dict['serve_class'] = i[10]
            one_dict['mail_method'] = i[11]
            one_dict['note'] = i[12]
            data.append(one_dict)
        page_list = list()
        for i in range(0, len(data), int(limit)):
            page_list.append(data[i:i + int(limit)])
        results['data'] = page_list[int(page) - 1]
        results['count'] = len(data)
        return results


@customer_blueprint.route('/up_task', methods=['GET', 'POST'])
@customer_required
def up_task():
    if request.method == 'GET':
        return render_template('customer/cus_up_task.html')

    # 预存表格数据到task_json字段中
    if request.method == 'POST':
        file = request.files.get('file')
        filename = file.filename
        file_path = save_file(file, filename, TASK_DIR)
        results = {'code': RET.OK, 'data': MSG.OK}
        user_id = g.cus_user_id
        try:
            if 'static' in file_path:
                data = xlrd.open_workbook(file_path, encoding_override='utf-8')
                table = data.sheets()[0]
                nrows = table.nrows  # 行数
                ncols = table.ncols  # 列数
                row_list = [table.row_values(i) for i in range(0, nrows)]  # 所有行的数据
                col_list = [table.col_values(i) for i in range(0, ncols)]  # 所有列的数
                # 验证参数是否空缺
                index = 1
                err_list = list()
                for i in row_list[1:]:
                    index += 1
                    if not all([i[0], i[1], i[2], i[3], i[4], i[6], i[7], i[8], i[11]]):
                        err_list.append(str(index))
                if len(err_list) != 0:
                    results['code'] = RET.SERVERERROR
                    m = ""
                    for i in err_list:
                        m = m + i + ','
                    results['msg'] = "第" + m + "行缺少必填参数!"
                    return jsonify(results)

                # 以下是计算服务费
                asin_list = col_list[2][1:]
                serve_class_list = col_list[10][1:]
                # 计算全部商品本金
                good_money_list = col_list[7][1:]
                good_sum_money = 0
                for i in good_money_list:
                    good_sum_money += float(i)

                # 计算下单数量
                sum_num = len(asin_list)

                # 获取每个asin对饮的数量(字典)
                asin_num_dict = asin_num(asin_list)
                # 去重后的asin列表
                one_asin_list = list(asin_num_dict.keys())
                # 将asin和serve_class组合为列表,数据结构:[['1AJFOAFJA', 'Review/FeedBack'], ['AB', 'FeedBack']]
                asin_group = list()
                index = 0
                for i in asin_list:
                    one_asin = [asin_list[index], serve_class_list[index]]
                    asin_group.append(one_asin)
                    index += 1

                # 计算review的数量和feedback数量
                asin_detail_list = list()
                for asin in one_asin_list:
                    asin_detail = dict()
                    review_num = 0
                    feedback_num = 0
                    for i in asin_group:
                        if i[0] == asin and i[1] == "Review":
                            review_num += 1
                        if i[0] == asin and i[1] == "FeedBack":
                            feedback_num += 1
                        if i[0] == asin and i[1] == "Review/FeedBack":
                            review_num += 1
                            feedback_num += 1
                    asin_detail['asin'] = asin
                    num = asin_num_dict.get(asin)
                    asin_detail['num'] = num
                    asin_detail['review_num'] = review_num
                    asin_detail['feedback'] = feedback_num
                    asin_detail['bili'] = review_num / num
                    asin_detail_list.append(asin_detail)

                # 查询服务商的收费标准
                serve_json = SqlData().search_user_field('amz_serve', user_id)
                if not serve_json:
                    return jsonify({'code': RET.SERVERERROR, 'msg': "请联系服务商设置收费标准!"})
                else:
                    serve_dict = json.loads(serve_json)
                    FeedBack = serve_dict.get('FeedBack')
                    if not FeedBack:
                        return jsonify({'code': RET.SERVERERROR, 'msg': "请联系服务商设置FeedBack收费标准!"})

                # 判断留评比例是否符合要求
                pass_asin = list()
                for i in asin_detail_list:
                    bili = i.get('bili')
                    bili_baifen = str(int(bili * 100))
                    if bili_baifen in serve_dict:
                        i['review_price'] = serve_dict.get(str(bili_baifen))
                    else:
                        pass_asin.append(i)

                if len(pass_asin) > 0:
                    s = "以下ASIN的留评比例不符合服务商的收费标准: "
                    for i in pass_asin:
                        asin = i.get('asin')
                        bili = str(int(i.get('bili') * 100)) + '%'
                        s1 = asin + ": " + bili + "。 "
                        s += s1
                    s + '更多收费标准请咨询服务商!'
                    return jsonify({'code': RET.SERVERERROR, 'msg': s})

                for i in asin_detail_list:
                    asin_n = i.get('num')
                    price = i.get('review_price')
                    review_money = asin_n * price
                    feedback_num = i.get('feedback')
                    feedback_money = feedback_num * FeedBack
                    i['sum_money'] = review_money + feedback_money

                task_info_list = list()
                for one in row_list[1:]:
                    one_task_list = list()
                    country = one[0].strip()
                    if not one[1]:
                        task_run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        task_run_time = excel_to_data(one[1])
                    asin = one[2].strip()
                    key_word = one[3].strip()
                    kw_location = one[4].strip()
                    store_name = one[5].strip()
                    good_name = one[6].strip()
                    good_money = one[7]
                    good_link = one[8].strip()
                    pay_method = one[9].strip()
                    serve_class = one[10].strip()
                    mail_method = one[11].strip()
                    note = one[12].strip()
                    review_title = one[13].strip()
                    review_info = one[14].strip()
                    feedback_info = one[15].strip()
                    one_task_list.append(country)
                    one_task_list.append(task_run_time)
                    one_task_list.append(asin)
                    one_task_list.append(key_word)
                    one_task_list.append(kw_location)
                    one_task_list.append(store_name)
                    one_task_list.append(good_name)
                    one_task_list.append(good_money)
                    one_task_list.append(good_link)
                    one_task_list.append(pay_method)
                    one_task_list.append(serve_class)
                    one_task_list.append(mail_method)
                    one_task_list.append(note)
                    one_task_list.append(review_title)
                    one_task_list.append(review_info)
                    one_task_list.append(feedback_info)
                    task_info_list.append(one_task_list)
                task_info_dict = dict()
                task_info_dict['task_info'] = task_info_list
                serve_money = 0
                for i in asin_detail_list:
                    money = i.get('sum_money')
                    serve_money += money
                task_info_dict['serve_money'] = serve_money

                task_info_dict['good_sum_money'] = good_sum_money

                task_info_dict['terrace'] = 'AMZ'

                task_info_dict['sum_num'] = sum_num
                # print(task_info_dict)
                task_info_json = json.dumps(task_info_dict, ensure_ascii=False)
                string = ""
                for i in task_info_json:
                    if i == "'":
                        i = "\\'"
                        string += i
                    else:
                        string += i
                label = g.cus_label
                SqlData().update_user_cus('task_json', string, user_id, label)

                return jsonify(results)
        except Exception as e:
            logging.error(str(e))
            results = {'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR}
            return jsonify(results)

    else:
        results = {'code': RET.SERVERERROR, 'msg': MSG.SERVERERROR}
        return jsonify(results)


@customer_blueprint.route('/one_detail/', methods=['GET'])
@customer_required
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
        one_detail['task_run_time'] = str(data[16])
        one_detail['task_state'] = data[17]
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
        return render_template('customer/cus_order_detail.html', **one_detail)

    except Exception as e:
        logging.error(str(e))
        return jsonify(results)


@customer_blueprint.route('/task_detail/', methods=['GET'])
@customer_required
def task_detail():
    sum_order_code = request.args.get('sum_order_code')
    page = request.args.get('page')
    limit = request.args.get('limit')
    task_state = request.args.get('task_state')
    results = {"code": RET.OK, "msg": MSG.OK, "count": 0, "data": ""}
    page_list = list()
    try:
        if task_state:
            state_sql = "AND task_state='" + task_state + "'"
        else:
            state_sql = "AND task_detail_info.task_state!='已完成' AND task_detail_info.task_state!='待留评'"
        task_info = SqlData().search_task_detail(sum_order_code, state_sql=state_sql)
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


@customer_blueprint.route('/task_list/', methods=['GET'])
@customer_required
def task_list():
    sum_order_code = request.args.get('sum_order_code')
    terrace = request.args.get('terrace')
    context = dict()
    if terrace == "AMZ":
        context['good_name'] = '产品名称'
        context['pay_method'] = '支付方式'
        context['serve_class'] = '服务类型'
        context['review_title'] = '评论标题'
        context['review_info'] = '评论内容'
        context['feedback_info'] = 'FeedBack'
    if terrace == "SMT":
        context['good_name'] = '搜索价格'
        context['pay_method'] = 'SKU'
        context['serve_class'] = '邮费'
        context['review_title'] = '文字留评'
        context['review_info'] = '图片留评'
        context['feedback_info'] = '默认留评'

    context['sum_code'] = sum_order_code
    context['terrace'] = terrace
    return render_template('customer/customer_task_list.html', **context)


@customer_blueprint.route('/task', methods=['GET'])
@customer_required
def customer_task():
    user_id = g.cus_user_id
    cus_label = g.cus_label
    page = request.args.get('page')
    limit = request.args.get('limit')
    results = {'code': RET.OK, 'msg': MSG.OK}
    task_info = SqlData().search_task_on_code('customer_label', cus_label, user_id)
    task_info = list(reversed(task_info))
    page_list = list()
    for i in range(0, len(task_info), int(limit)):
        page_list.append(task_info[i:i + int(limit)])
    results['data'] = page_list[int(page) - 1]
    results['count'] = len(task_info)
    return jsonify(results)


@customer_blueprint.route('/index', methods=['GET'])
@customer_required
def customer_index():
    context = {'account': g.cus_account}
    return render_template('customer/customer_index.html', **context)


@customer_blueprint.route('/logout', methods=['GET'])
@customer_required
def logout():
    session.pop('cus_id')
    session.pop('customer_label')
    session.pop('customer_account')
    session.pop('customer_discount')
    session.pop('customer_user_id')
    return render_template('customer/login_customer.html')


@customer_blueprint.route('/login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'GET':
        return render_template('customer/login_customer.html')
    if request.method == 'POST':
        results_er = {'code': RET.SERVERERROR, 'msg': MSG.DATAERROR}
        results_ok = {'code': RET.OK, 'msg': MSG.OK}
        data = json.loads(request.form.get('data'))
        main_user = data.get('main_user')
        account = data.get('account')
        password = data.get('password')
        res = SqlData().search_customer_login(main_user, account, password)
        if not res:
            return jsonify(results_er)
        if res:
            one_info = res[0]
            session['cus_id'] = one_info[0]
            session['customer_account'] = one_info[3]
            session['customer_label'] = one_info[2]
            session['customer_discount'] = one_info[5]
            session['customer_user_id'] = one_info[1]
            return jsonify(results_ok)
