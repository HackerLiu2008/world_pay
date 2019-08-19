from datetime import timedelta

from flask import Flask
import logging

# from flask_wtf.csrf import CSRFProtect
# from apps.task import task_blueprint

app = Flask(__name__)
# 使用缓存,缓存大量查出来的信息
# cache = Cache(app, config={'CACHE_TYPE': 'simple'})

app.config['SECRET_KEY'] = 'Gute9878934'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

app.app_context().push()
# CSRFProtect(app)


LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "  # 配置输出日志格式
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '  # 配置输出时间的格式，注意月份和天数不要搞乱了
logging.basicConfig(level=logging.WARNING,
                    format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,
                    filename=r"G:/order_flask/static/log/test.log"  # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                    )

# 注册路由,以url_prefix区分功能(蓝图)

from apps.task import task_blueprint

app.register_blueprint(task_blueprint)

from apps.account import account_blueprint

app.register_blueprint(account_blueprint)

from apps.upload import upload_blueprint

app.register_blueprint(upload_blueprint)

from apps.user import user_blueprint

app.register_blueprint(user_blueprint)

from apps.order import order_blueprint

app.register_blueprint(order_blueprint)

from apps.customer import customer_blueprint

app.register_blueprint(customer_blueprint)
