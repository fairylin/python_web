from utils import log
from routes import current_user
from models import User
# 根据 Model 类 创建的 Todo 类
from todo import Todo

import time


def template(name):
    """
    根据名字读取 templates 文件夹中的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def change_time(timestamp):
    """
    进行时间戳 timeStamp 格式转换为 本地时间格式
    """
    time_array = time.localtime(timestamp)
    other_style_time = time.strftime("%m-%d %H:%M", time_array)
    return other_style_time


def response_with_headers(headers, code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def redirect(url):
    """
    浏览器在收到 302 相应的时候
    会自动在 HTTP headers 里面找到一个 Location 字段并获取一个url
    然后再次对获取到的 url 发送一次请求
    """
    headers = {
        'Location': url,
    }
    # 增加 Location 字段并生成 HTTP 响应返回
    # 注意， 没有 HTTP body 部分
    r = response_with_headers(headers, 302)
    return r.encode(encoding='utf-8')


def login_required(route_function):
    def f(request):
        uname = current_user(request)
        u = User.find_by(username=uname)
        if u is None:
            return redirect('/login')
        return route_function(request)

    return f


def index(request):
    """
    _todo 首页的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    # 找到当前登录用户，如果没有登录，就 redirect 到 /login
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_list = Todo.find_all(user_id=u.id)
    # 下面这一行 生成一个html字符串
    # todo_html = ''.join(['<h3>{}: {}</h3>'.format(t.id, t.title)
    #                      for t in todo_list])

    todos = []
    for t in todo_list:
        edit_link = '<a href="/todo/edit?id={}">编辑</a>'.format(t.id)
        delete_link = '<a href="/todo/delete?id={}">删除</a>'.format(t.id)
        create_time = '创建时间: {}\t'.format(t.create_time)
        update_time = '<br />更新时间: {}\t'.format(t.update_time)
        s = '<h3>{} : {} {} {}</h3><h5>{} {}</h5>'.format(t.id, t.title, edit_link, delete_link, create_time,
                                                          update_time)
        todos.append(s)
    todo_html = ''.join(todos)
    # 替换模板文件中的标记字符串
    body = template('todo_index.html')
    body = body.replace('{{todos}}', todo_html)
    # 下面这三行可以改写为一条函数， 还把 headers 也放进 函数中
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def edit(request):
    """
    _todo edit 的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    # 得到当前编辑的 _todo 的 id
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    # if todo_id < 1:
    #     return error(404)
    if u is None:
        return redirect('/login')
    if u.id != t.user_id:
        redirect('/todo')
    # 替换 模板文件中的标记字符串
    body = template('todo_edit.html')
    body = body.replace('{{todo_id}}', str(t.id))
    body = body.replace('{{todo_title}}', str(t.title))
    # 把下面 3 行可以修改为一个函数，还把 headers 放入到函数中
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def add(request):
    """
    用于增加 _todo 的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if request.method == 'POST':
        form = request.form()
        t = Todo.new(form)
        t.user_id = u.id
        t.create_time = change_time(int(time.time()))
        t.update_time = change_time(int(time.time()))
        t.save()
    # 浏览器发送过来的数据被处理后， 重定向到首页
    # 当浏览器请求首页的时候， 就可以看到新增的数据信息了
    return redirect('/todo')


def update(request):
    """
    用于增加新的 _todo 的路由函数
    """
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    if request.method == 'POST':
        # 修改并保存 todo_
        form = request.form()
        log('debug update ', form)
        todo_id = int(form.get('id', -1))
        t = Todo.find_by(id=todo_id)
        if u.id != t.user_id:
            redirect('/todo')
        t.title = form.get('title', t.title)
        t.update_time = form.get('update_time', change_time(time.time()))
        t.save()
    # 浏览器发送数据过来被处理后，重定向到首页
    # 浏览器在亲求新首页地址的时候，就能看到新增的数据了
    return redirect('/todo')


def delete_todo(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    # 得到当前编辑的 _todo 的 id
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    if t is not None:
        t.remove()
    return redirect('/todo')


def route_admin_users(request):
    """
    只有 id 为 1 的用户可以访问这个页面, 其他用户访问会定向到 /login
    这个页面显示了所有的用户 包括 id username password
    """
    headers = {
        'Content-Type': 'text/html',
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    if u.id != 1:
        return redirect('/todo')
    user_list = []
    for u in User.all():
        user = '<br> {} {} {}'.format(u.id, u.username, u.password)
        user_list.append(user)
    log('/admin/users', user_list, type(user_list))
    body = template('all_user.html')
    body = body.replace('{{users}}', ''.join(user_list))
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_admin_users_update(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    # 得到当前编辑的 _todo 的 id
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    if t is not None:
        t.remove()
    return redirect('/todo')


route_dict = {
    # GET 请求 显示数据
    '/todo': index,
    '/todo/edit': edit,
    # POST 请求, 处理数据
    '/todo/add': add,
    '/todo/update': update,
    '/todo/delete': delete_todo,
    '/admin/users': route_admin_users,
}
