import json
from routes.session import session
from utils import (
    log,
    redirect,
    http_response,
    json_response,
)
from models.todo import Todo


# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据信息
def all(request):
    """
    返回所有的 todo
    :param request:
    :return:
    """
    todo_list = Todo.all()
    # 要转换为 dict 格式
    # print('todo_list', todo_list)
    todos = [t.json() for t in todo_list]
    return json_response(todos)


def add(request):
    """
    接受浏览器发过来的添加 todo 的请求
    添加数据并返回给浏览器
    :param request:
    :return:
    """
    # 得到浏览器发送的表单，浏览器用ajax 发送json数据过来
    # 所以这里我们用新增加的 json 函数来获取 格式化之后的 json 数据
    form = request.json()
    print('add form', form)
    # 创建一个 todo
    t = Todo.new(form)
    # 把创建好的 todo 返回给浏览器
    return json_response(t.json())


def delete(request):
    """
    通过下面的链接来删除一个 todo
    /delete?id=1
    :param request:
    :return:
    """
    todo_id = int(request.query.get('id'))
    print('delete todo_id', todo_id)
    t = Todo.delete(todo_id)
    print('delete todo', type(t), t)
    return json_response(t.json())


def update(request):
    form = request.form()
    todo_id = request.query.get('id')
    t = Todo.update(todo_id, form)
    return json_response(t.json())


route_dict = {
    '/api/todo/all': all,
    '/api/todo/add': add,
    '/api/todo/delete': delete,
    '/api/todo/update': update,
}