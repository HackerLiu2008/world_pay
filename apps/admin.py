import json
import logging

from flask import request, render_template, jsonify, session, g

from tools_me.mysql_tools import SqlData
from tools_me.other_tools import admin_required
from tools_me.parameter import RET, MSG
from . import admin_blueprint


@admin_blueprint.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin/admin_login.html')

    if request.method == 'POST':
        results = dict()
        results['code'] = RET.OK
        results['msg'] = MSG.OK
        try:
            data = json.loads(request.form.get('data'))
            account = data.get('account')
            password = data.get('password')
            admin_id, name = SqlData().search_admin_login(account, password)
            session['admin_id'] = admin_id
            session['admin_name'] = name
            return jsonify(results)

        except Exception as e:
            logging.error(str(e))
            results['code'] = RET.SERVERERROR
            results['msg'] = MSG.PSWDERROR
            return jsonify(results)


@admin_blueprint.route('/', methods=['GET'])
@admin_required
def index():
    admin_name = g.admin_name
    context = dict()
    context['admin_name'] = admin_name
    return render_template('admin/index.html', **context)
