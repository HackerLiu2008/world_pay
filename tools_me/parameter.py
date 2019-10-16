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


TRANS_STATUS = {
    'WAIT': '待付款',
    'PROCESS': '处理中',
    'PAID': '已付款',
    'SUBBANK': '已提交银行卡',
    'SUCC': '交易成功',
    'FINISH': '交易成功',
    'AUTH': '已授权',
    'FAIL': '交易失败',
    'CLOSED': '交易关闭'
}


class TRANS_TYPE:
    IN = "收入"
    OUT = "支出"


class DO_TYPE:
    CREATE_CARD = "开卡"
    TOP_UP = "充值"
    REFUND = "退款"

