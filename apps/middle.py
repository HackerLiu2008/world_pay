import json
from tools_me.mysql_tools import SqlData
from flask import request, render_template, jsonify, session
from tools_me.other_tools import middle_required
from tools_me.parameter import RET, MSG
from . import middle_blueprint


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
