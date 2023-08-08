#各种配置相关的信息，包括邮箱、加密。。。

SECRET_KEY = "asdfasfdasdf" #用作session加密解密，可以随便写，越长越安全但是性能也越差


# MySQL所在的主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# MySQL上创建的数据库名称
DATABASE = "wangQin_oa"
# 连接MySQL的用户名，读者用自己设置的
USERNAME = "root"
# 连接MySQL的密码，读者用自己的
PASSWORD = "root"

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "wang.qin_001@foxmail.com"
MAIL_PASSWORD = "ojybfhdddvqsfjfj"
MAIL_DEFAULT_SENDER = "wang.qin_001@foxmail.com"