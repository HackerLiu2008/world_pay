# 以下是自用零时接口,/dome

from flask import request
from . import dome_blueprint


# @dome_blueprint.route('/lum_change', methods=['GET'])
# def lum_change():
#     header = request.headers
#     print(header)