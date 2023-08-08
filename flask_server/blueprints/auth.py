import random
import string


from flask import Blueprint,request,jsonify,session
#邮件发送
from exts import mail,db
from flask_mail import Message
from werkzeug.security import generate_password_hash,check_password_hash #加密

from .forms import RegisterForm,LoginForm #从当前目录中导入刚才书写的规则

#验证码缓存
from models import EmailCaptchaModel,UserModel


bp = Blueprint("api",__name__,url_prefix="/api")

#登录页：http://127.0.0.1:5000/api/login
@bp.route("/login",methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        email = form.email.data
        password = form.password.data
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            print("该邮箱未注册")
            return jsonify({"code":201,"message":"邮箱未注册","data":None})
        if check_password_hash(user.password,password):
            session['user_id'] = user.id #将user的id加密后存入session
            return "登录成功"
        else:
            print("密码错误！")
            return jsonify({"code": 202, "message": "密码错误", "data": None})
    else:
        print(form.errors)
        return form.errors


@bp.route('/logout')
def logout():
    session.clear()
    return jsonify({"code": 200, "message": "logout success", "data": None})

@bp.route('/getUsername')
def getUsername():
    user_id = session.get('user_id')
    print(user_id)
    if user_id:
        user = UserModel.query.get(user_id)
        username = user.username
        return jsonify({"code": 200, "message": "got username success", "data": username})
    else:
        return jsonify({"code": 200, "message": "got username failed", "data": None})



@bp.route('/register', methods=['POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate():
        # 表单验证成功
        email = form.email.data
        captcha = form.captcha.data
        username = form.username.data
        password = form.password.data
        user = UserModel(username=username,email=email,password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print("注册成功！")
        return jsonify({"code":200,"message":"success","data":None})
    else:
        # 表单验证失败
        validation_errors = form.errors
        print(validation_errors)
        # 处理验证错误
        return jsonify({"code":406,"message":"表单验证失败","data":None})

#如果没有指定methods参数，默认get请求
@bp.route("/getCatpcha")
def get_email_captcha():
    email = request.args.get("email")#/captcha/email?email=xx@qq.com问号传参
    source = string.digits*4
    catpcha = random.sample(source,4)
    captcha = "".join(catpcha)
    message = Message(subject='catpcha',recipients=[email], body=f'your catpcha is:{captcha}')
    mail.send(message)
    #将验证码存入数据库，正常情况应该用redis等缓存的
    email_captcha = EmailCaptchaModel(email=email,captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    #使用jsonify返回一个restful风格的API
    return jsonify({"code":200,"message":"success","data":None})
