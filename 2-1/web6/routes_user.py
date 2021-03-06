from utils import log
from utils import redirect
from utils import template
from utils import http_response

from models import User

import random
import time

session = {}


def random_str():
    """
    生成一个随机字符串
    """
    seed = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    s = ''
    for i in range(16):
        # 这里 len(seed) - 2 并没有特殊含义
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def current_user(request):
    """
    获取到登录的用户信息
    """
    log('session', session)
    session_id = request.cookies.get('user', '')
    user_id = int(session.get(session_id, '-1'))
    log('user_id', user_id)
    u = User.find_by(id=user_id)
    log('current_user', user_id, u)
    return u


def response_with_header(headers, code=200):
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


# def template(name):
#     """
#     实现 routes_user 中需要用到的 template 函数 加载模板文件
#     """
#     path = 'templates/' + name
#     with open(path, 'r', encoding='utf-8') as f:
#         return f.read()


def route_index(request):
    """
    主页的请求函数， 处理主页的响应
    """
    header = 'HTTP/1.1 200 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_login(request):
    """
    登录的请求函数， 处理登录请求的响应
    headers 的格式如下
    # 'Set-Cookie': 'height=169; gua=1; pwd=2; Path=/',
    """
    headers = {
        'Content-Type': 'text/html',
    }
    log('login, cookies', request.cookies, current_user(request))
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        # username = u.username
        if u.validate_login():
            user = User.find_by(username=u.username)
            # 可以通过设置一个令牌（随机字符串）进行使用
            session_id = random_str()
            log('session_id', session_id)
            session[session_id] = user.id
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            result = '登录成功'
            # body = template('login.html', username=username, result=result)
            # return http_response(body, headers)
            # time.sleep(5)
            return redirect('/login', headers)
        # else:
        #     result = '用户名或密码错误'
    # else:
    #     result = ''
    body = template('login.html')
    # body = body.replace('{{username}}', username)
    # body = body.replace('{{result}}', result)
    # header = response_with_header(headers)
    # r = header + '\r\n' + body
    # return r.encode(encoding='utf-8')
    return http_response(body, headers)


def route_register(request):
    """
    注册的请求函数， 处理注册请求的响应
    """
    # headers = 'HTTP/1.1 200 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        log('register form', form)
        u = User(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名和密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    return http_response(body)
    # body = body.replace('{{result}}', result)
    # r = headers + '\r\n' + body
    # return r.encode(encoding='utf-8')


# def route_admin_users(request):
#     """
#     只有 id 为 1 的用户可以访问这个页面, 其他用户访问会定向到 /login
#     这个页面显示了所有的用户 包括 id username password
#     """
#     headers = {
#         'Content-Type': 'text/html',
#     }
#     uname = current_user(request)
#     u = User.find_by(username=uname)
#     if u is None:
#         return redirect('/login')
#     if u.id != 1:
#         return redirect('/todo')
#     user_list = []
#     for u in User.all():
#         user = '<br> {} {} {}'.format(u.id, u.username, u.password)
#         user_list.append(user)
#     log('/admin/users', user_list, type(user_list))
#     body = template('admin_users.html')
#     body = body.replace('{{users}}', ''.join(user_list))
#     header = response_with_header(headers)
#     r = header + '\r\n' + body
#     return r.encode(encoding='utf-8')


def route_admin_users(request):
    u = current_user(request)
    log('u', u)
    log('admin users', u)
    if u is not None and u.is_admin():
        log(type(u))
        us = User.all()
        body = template('admin_users.html', users=us)
        return http_response(body)
    else:
        return redirect('/login')


def route_admin_user_update(request):
    """
    管理员账号登录修改其他用户的个人信息
    """
    form = request.form()
    log('route_admin_user_update', form)
    user_id = int(form.get('id', -1))
    new_password = form.get('password', '')
    u = User.find_by(id=user_id)
    if u is not None:
        u.password = new_password
        u.save()
    return redirect('/admin/users')


def route_static(request):
    """
    静态资源处理函数， 读取图片并产生响应进行返回
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/admin/users': route_admin_users,
    '/admin/user/update': route_admin_user_update,
}
