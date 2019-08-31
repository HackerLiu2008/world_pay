from flask import Blueprint


task_blueprint = Blueprint("task", __name__, url_prefix="/task", template_folder='../templates')


account_blueprint = Blueprint("account", __name__, url_prefix="/account", template_folder='../templates')


upload_blueprint = Blueprint('upload', __name__, url_prefix='/upload', template_folder='../templates')


user_blueprint = Blueprint('user', __name__, url_prefix='/user', template_folder='../templates')


order_blueprint = Blueprint('order', __name__, url_prefix='/order', template_folder='../templates')


customer_blueprint = Blueprint('customer', __name__, url_prefix='/customer', template_folder='../templates')


dome_blueprint = Blueprint('dome', __name__, url_prefix='/dome', template_folder='../templates')


middle_blueprint = Blueprint('middle', __name__, url_prefix='/middle',  template_folder='../templates')


from . import task, account, upload, user, order, customer, middle