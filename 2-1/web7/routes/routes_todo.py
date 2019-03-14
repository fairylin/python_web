from utils import log
from utils import template

# 根据 Model 类 创建的 _Todo 类
from models import Todo
from routes.session import session


def current_user(request):
    session_id = request.cookies.get('user', '')
    user_id = session.get(session_id, -1)
    return user_id


def response_with_headers(headers, status_code=200):
    header = 'HTTP/1.1 {} OK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def redirect(location, headers=None):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 中找到一个 Location 字段，并获取其中的一个 url 值
    然后自动请求新的 url
    """
    h = {
        'Content-Type': 'text/html',
    }
    if headers is not None:
        h.update(headers)
    h['Location'] = location
    # 增加 Location 字段并生成 HTTP 响应返回
    # 注意， 没有 HTTP body 部分
    header = response_with_headers(h, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')


# 直接写函数名字不写 route 了
def index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    session_id = request.cookies.get('user', '')
    user_id = session.get(session_id)
    todo_list = Todo.find_all(user_id=user_id)
    # 判断如果 user_id 为1 ，即用户为管理员用户账号，则展示所有的用户信息，否则展示其他用户对应信息
    # 如果未登录状态，则为空
    # if user_id == 1:
    #     todo_list = Todo.all()
    log('index debug', todo_list)
    body = template('simple_todo_index.html', todos=todo_list)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# def index(request):
#     """
#     _todo 首页的路由函数
#     """
#     header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
#     session_id = request.cookies.get('user', '')
#     user_id = session.get(session_id)
#     todo_list = Todo.find_all(user_id=user_id)
#     # todo_list = Todo.all()
#     body = template('simple_todo_index.html', todos=todo_list)
#     r = header + '\r\n' + body
#     return r.encode(encoding='utf-8')


def add(request):
    """
    用于增加 _todo 的路由函数
    """
    # 得到浏览器发送的表单
    form = request.form()
    session_id = request.cookies.get('user', '')
    user_id = session.get(session_id, 1)
    print('todo_add_info', form, session_id, user_id)
    # 创建一个 _todo
    Todo.new(form, user_id)
    # 让浏览器刷新页面到主页面去
    return redirect('/todo/index')


def edit(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    todo_id = int(request.query.get('id'))
    t = Todo.find(todo_id)
    body = template('simple_todo_edit.html', todo=t)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def update(request):
    """
    通过下面一种链接来更新一个 _todo
    /update?id=1
    """
    todo_id = int(request.query.get('id'))
    form = request.form()
    Todo.update(todo_id, form)
    return redirect('/todo/index')


def delete(request):
    """
    通过下面这样的链接来删除一个 todo
    /delete?id=1
    """
    todo_id = int(request.query.get('id'))
    session_id = request.cookies.get('user', '')
    user_id = session.get(session_id)
    t = Todo.find(todo_id)
    print('routes_todo_todo_id', t, user_id)
    if t.user_id == user_id:
        Todo.delete(todo_id)
    return redirect('/todo/index')


# 定义一个函数统一检测是否登录
def login_required(route_function):
    def func(request):
        uid = current_user(request)
        log('登录鉴定, user_id ', uid)
        if uid == -1:
            # 没登录 不让看 重定向到 /login
            return redirect('/login')
        else:
            # 登录了, 正常返回路由函数响应
            return route_function(request)
    return func


route_dict = {
    # GET 请求 显示数据
    '/todo/index': login_required(index),
    '/todo/edit': login_required(edit),
    # POST 请求, 处理数据
    '/todo/add': login_required(add),
    '/todo/update': login_required(update),
    '/todo/delete': login_required(delete),
}
