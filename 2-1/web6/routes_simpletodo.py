from utils import log
from utils import template
from utils import redirect
from utils import http_response

# 根据 Model 类 创建的 _Todo 类
from models import Todo


def index(request):
    """
    _todo 首页的路由函数
    """
    todo_list = Todo.all()
    body = template('simple_todo_index.html', todos=todo_list)
    return http_response(body)


def edit(request):
    """
    _todo edit 的路由函数
    """
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    log('debug EDIT', t)
    body = template('simple_todo_edit.html', todo=t)
    return http_response(body)


def add(request):
    """
    用于增加 _todo 的路由函数
    """
    # 得到浏览器发送的表单
    form = request.form()
    # 创建一个 _todo
    Todo.new(form)
    # 让浏览器刷新页面到主页面去
    return redirect('/todo')


def update(request):
    """
    通过下面一种链接来更新一个 _todo
    /todo/update?id=1
    """
    form = request.form()
    todo_id = int(request.query.get('id'))
    Todo.update(todo_id, form)
    return redirect('/todo')


def delete(request):
    """
    通过下面这样的的链接来删除数据
    """
    todo_id = int(request.query.get('id'))
    Todo.delete(todo_id)
    return redirect('/todo')


route_dict = {
    # GET 请求 显示数据
    '/todo': index,
    '/todo/edit': edit,
    # POST 请求, 处理数据
    '/todo/add': add,
    '/todo/update': update,
    '/todo/delete': delete,
}
