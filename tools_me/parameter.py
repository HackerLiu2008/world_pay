# coding:utf-8
# 以下是一些常用参数

# 保存excel文件的路径

ACCOUNT_DIR = '/order_flask/static/excel_account/'
TASK_DIR = '/order_flask/static/excel_task/'
PHOTO_DIR = 'G:/order_flask/static/photo'
DW_ACCOUNT = 'G:/order_flask/static/download/买家号导入模板.xlsx'
DW_TASK = 'G:/order_flask/static/download/AMZ任务导入模板.xlsx'
SMT_TASK = 'G:/order_flask/static/download/SMT任务导入模板.xlsx'


class RET:
    OK = 0
    SERVERERROR = 502


class MSG:
    OK = 'SUCCESSFUL'
    SERVERERROR = 'SERVER ERROR'
    NODATA = 'NODATA'
    DATAERROR = '参数错误!'
    PSWDERROR = 'PASS_WORD ERROR'
    PSWDLEN = '密码长度不得小于6位数!'


class CACHE:
    TIMEOUT = 15


class TASK:
    SUM_ORDER_CODE = ''


class ORDER:
    TASK_CODE = ''
    BUY_ACCOUNT = ''
    TERRACE = ''
    COUNTRY = ''
    LAST_BUY = ''
    STORE = ''
    ASIN = ''
    STORE_GROUP = ''
    ASIN_GROUP = ''
