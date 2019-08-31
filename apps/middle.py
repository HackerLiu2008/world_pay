import json

from flask import request, render_template

from . import middle_blueprint


@middle_blueprint.route('login', methods=['GET', 'POST'])
def middle_login():
    if request.method == 'GET':
        return render_template('middle/login.html')
    if request.method == 'POST':
        data = json.loads(request.form.get('data'))
        main_user = data.get('mainName')
        account = data.get('userName')
        pass_word = data.get('nuse')
        pass