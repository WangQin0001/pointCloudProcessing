from flask import Flask,session,g       #g代表全局变量
#1.创建config.py并导入和绑定
import config
#2.创建extension文件并导入db(解决循环引用的问题)
from exts import db,mail
#3.创建ORM模型modules并导入
from models import UserModel
from flask_migrate import Migrate
#4.导入并注册蓝图
from blueprints.pcd import bp as pcd_bp
from blueprints.auth import bp as auth_bp
from blueprints.controller import bp as controller_bp

app = Flask(__name__)
#1.绑定配置文件
app.config.from_object(config)
#2.在app中绑定db
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app,db)
#4.注册蓝图
app.register_blueprint(pcd_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(controller_bp)

if __name__ == '__main__':
    app.logger.debug('This is a debug message')
    app.run(debug=True,use_reloder=True)
