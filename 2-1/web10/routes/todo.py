from routes.session import session
from utils import (
    log,
    redirect,
    template,
    http_response,
)


def main_index(request):
    log('routes-todo.py-main_index')
    return redirect('/todo/index')


def index(request):
    """
    主页处理函数，返回主页的响应
    :param request:
    :return:
    """
    body = template('todo_index.html')
    return http_response(body)


route_dict = {
    '/': main_index,
    '/todo/index': index,
}