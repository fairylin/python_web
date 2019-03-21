from utils import log
from models.user import User
from models.message import Message

import random

# message_list 存储了所有的 message
message_list = []
# session 可以在服务器端实现过期功能
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


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    """
    主页的请求函数， 处理主页的响应
    """
    header = 'HTTP/1.1 200 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# def current_user(request):
#     session_id = request.cookies.get('user', '')
#     username = session.get(session_id, '【游客】')
#     return username


def current_user(request):
    """
    获取到登录的用户信息
    """
    log('session', session)
    session_id = request.cookies.get('user', '')
    user_id = int(session.get(session_id, '-1'))
    log('user_id', user_id)
    u = User.find_by(id=user_id)
    if u:
        log('current_user', user_id, u)
        return u
    else:
        return None


def response_with_header(headers, code=200):
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def redirect(url):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 中找到一个 Location 字段，并获取其中的一个 url 值
    然后自动请求新的 url
    """
    headers = {
        'Location': url,
    }
    # 增加 Location 字段并生成 HTTP 响应返回
    # 注意， 没有 HTTP body 部分
    r = response_with_header(headers, 302) + '\r\n'
    return r.encode(encoding='utf-8')


"""
HTTP/1.1 302 xxx
Location: /
"""


def route_login(request):
    """
    登录的请求函数， 处理登录请求的响应
    """
    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': 'height=169; gua=1; pwd=2; Path=/',
    }
    log('login, cookies', request.cookies, current_user(request))
    username = current_user(request)
    # log('login, username', username)
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            # headers['Set-Cookie'] = {}
            # headers['Set-Cookie'] = 'user={}'.format(u.username)
            # 可以通过设置一个令牌（随机字符串）进行使用
            session_id = random_str()
            session[session_id] = u.username
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            result = '登录成功'
        else:
            result = '用户名或密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{username}}', username)
    body = body.replace('{{result}}', result)
    header = response_with_header(headers)
    r = header + '\r\n' + body
    # log('login 的响应', r)
    return r.encode(encoding='utf-8')


def route_register(request):
    """
    注册的请求函数， 处理注册请求的响应
    """
    header = 'HTTP/1.1 200 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        log('register form', form)
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名和密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_message(request):
    username = current_user(request)
    # 如果是 未登录的用户 重定向到 '/'
    if username == '【游客】':
        log('**debug, route msg 未登录')
        return redirect('/')
    log('本次请求的method', request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        message_list.append(msg)
        # 可以考虑（应该）在这里保存一下message
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('html_basic.html')
    # '#'.join(['a', 'b', 'c']) 的结果是 ’a#b#c'
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{messages}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_profile(request):
    if request.cookies.get('user', ''):
        session_id = request.cookies.get('user', '')
        user = session[session_id]
        body = '<pre> {} </pre>'.format(User.all())
    else:
        user = ''
        body = '<h1>Hello World</h1>'
    log('profile *****', user)
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    """
    静态资源处理函数， 读取图片并产生响应进行返回
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\n'
        img = header + b'\r\n' + f.read()
        return img


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    # '/messages': route_message,
    '/profile': route_profile,
}
