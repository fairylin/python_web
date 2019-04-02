from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    session,
)

main = Blueprint('session', __name__)

"""
在进行项目开发过程中基本顺序应该是；
1.拆分问题，首先进行页面相关设计和编写。 view over
2.组织数据，把数据的操作实现； over
3.逻辑。
    1、未登录 展示登录 session_index2 页面，需要用户登录 服务器记录 session 会话信息
    2、登录成功，展示问好信息，并提供退出登录按钮
    3、逻辑设置完成
4.开始代码实现，部分实现，部分todo
5.剩下的一点点补全
6.美化页面（css）
"""


# @main.route('/')
# def index():
#     username = session.get("user_name", None)
#     if username is None:
#         return render_template("login.html")
#     else:
#         return render_template('session_index.html', username=username)


# @main.route("/login", methods=['POST'])
# def login():
#     user_name = request.form.get("user_name", "")
#     session["user_name"] = user_name
#     return redirect(url_for(".index"))


# @main.route("/logout", methods=['get'])
# def log_out():
#     session.pop("user_name")
#     return redirect(url_for(".index"))

@main.route('/')
def index():
    username = session.get("username", None)
    if username is None:
        return render_template("session_login.html")
    else:
        return render_template('session_logout.html', username=username)


@main.route("/login", methods=['POST'])
def login():
    username = request.form.get("username", "")
    session["username"] = username
    return redirect(url_for(".index"))


@main.route("/logout", methods=['GET'])
def log_out():
    session.pop("username")
    return redirect(url_for(".index"))
