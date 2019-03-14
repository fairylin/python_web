from utils import log
from utils import template
from utils import redirect
from utils import http_response

# 根据 Model 类 创建的 _Todo 类
from models import Todo
from routes.session import session
# from routes_static import current_user


def index(request):
    """
    _todo 首页的路由函数
    """
    session_id = request.cookies.get('user', '')
    user_id = session.get(session_id)
    todo_list = Todo.find_all(user_id=user_id)
    # todo_list = Todo.all()
    body = template('simple_todo_index.html', todos=todo_list)
    return http_response(body)


def add(request):
    """
    用于增加 _todo 的路由函数
    """
    # 得到浏览器发送的表单
    form = request.form()
    session_id = request.cookies.get('user', '')
    user_id = session.get(session_id, 1)
    log('todo_add_info', form, session_id, user_id)
    # 创建一个 _todo
    Todo.new(form, user_id)
    # 让浏览器刷新页面到主页面去
    return redirect('/todo/index')


def edit(request):
    """
    _todo edit 的路由函数
    """
    todo_id = int(request.query.get('id'))
    t = Todo.find_by(id=todo_id)
    body = template('simple_todo_edit.html', todo=t)
    return http_response(body)


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
    通过下面这样的的链接来删除数据
    """
    todo_id = int(request.query.get('id'))
    Todo.delete(todo_id)
    return redirect('/todo/index')


route_dict = {
    # GET 请求 显示数据
    '/index': index,
    '/edit': edit,
    # POST 请求, 处理数据
    '/add': add,
    '/update': update,
    '/delete': delete,
}
