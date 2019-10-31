from flask import render_template

from . import verify_pay_blueprint


@verify_pay_blueprint.route('/')
def verify_index():
    return render_template('verify_pay/index.html')
