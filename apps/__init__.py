from flask import Blueprint


upload_blueprint = Blueprint('upload', __name__, url_prefix='/upload', template_folder='../templates')


user_blueprint = Blueprint('user', __name__, url_prefix='/user', template_folder='../templates')


middle_blueprint = Blueprint('middle', __name__, url_prefix='/middle',  template_folder='../templates')


admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin',  template_folder='../templates')


from . import upload, user,  middle, admin