import socket
import urllib.parse
import _thread

from utils import (
    log,
    error,
)

from routes.routes_user import route_static
from routes.routes_todo import route_dict as todo_routes
from routes.routes_weibo import route_dict as weibo_routes
from routes.routes_user import route_dict as user_routes
from routes.api_todo import route_dict as api_todo
from routes.todo import route_dict as todo_new_routes


# 定义一个 class 用户保存请求的数据
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.header = {}
        self.cookies = {}

    def add_cookies(self):
        """
        Accept-Language: zh-CN,zh;q=0.8
        Cookie: height=169; user=gua
        :return:
        """
        cookies = self.header.get('Cookie', '')
        kvs = cookies.split('; ')
        log('cookie', kvs)
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v

    def add_headers(self, header):
        """
        Host: 127.0.0.1:3000
        User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)
            Chrome/65.0.3325.146 Safari/537.36
        Cookie: height=169; user=gua
        """
        # header = [
        #     'Host: 127.0.0.1:3000',
        #     'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)
        #       Chrome/65.0.3325.146 Safari/537.36',
        #     # 'Cookie: height=169; user=gua'
        # ]
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.header[k] = v
        self.add_cookies()

    def form(self):
        log('form self.form', self.body)
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f

    def json(self):
        """
        把body 中的 json 格式字符串解析成 dict 或者list 并返回
        :return:
        """
        import json
        print('json', self.body)
        print('json_dumps', json.dumps(self.body))
        return json.loads(self.body)


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有404
    """
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def parsed_path(path):
    """
    解析 path 获取 path 和 query
    如：
    message=hello&author=gua
    {
        'message': 'hello',
        'author': 'gua',
    }
    """
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split("=")
            query[k] = v
            print('path k, v',path, query)
        return path, query


def response_for_path(path, request):
    """
    根据请求的 path 返回相应的内容
    """
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and query', path, query)
    """
    根据 path 的值， 调用不同的处理函数
    没有处理函数的 path 会返回 404
    """
    r = {
        '/static': route_static,
    }
    r.update(todo_routes)
    r.update(weibo_routes)
    r.update(user_routes)
    r.update(api_todo)
    r.update(todo_new_routes)
    response = r.get(path, error)
    return response(request)


def process_request(connection):
    r = connection.recv(1100)
    r = r.decode('utf-8')
    log('完整请求')
    log('请求结束')
    # log('ip and request, {}\n{}'.format(address, r))
    # 因为 chrome 会发送空请求导致 split 得到空 list
    # 所以这里判断一下防止程序崩溃
    if len(r.split()) < 2:
        connection.close()
    path = r.split()[1]
    # 创建一个全局的请求对象
    request = Request()
    # 获取 request 的 method
    request.method = r.split()[0]
    # 把 body 放入到 request 中
    request.body = r.split('\r\n\r\n', 1)[1]
    # 把 header 放入到 request 中
    request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])

    # log('request content',request.method, '\n',
    #   request.header, '\n', request.cookies, '\n', request.body, '\n')
    # 用 response_for_path 函数来得到 path 对应的相应内容
    response = response_for_path(path, request)
    # print('response', response, type(response))
    # 把响应发送给客户端
    connection.sendall(response)
    print('完整响应')
    try:
        log(response.decode('utf-8').replace('\r\n', '\n'))
    except Exception as e:
        log('异常', e)
    print('响应结束', '*'*100)
    # 处理完请求后，关闭连接
    connection.close()


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    print('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        # 监听 接受 读取请求数据 解码成字符串
        s.listen(5)
        # 无限循环来处理请求
        while True:
            connection, address = s.accept()
            print('连接成功， 使用多线程处理请求', address)
            # 开一个新的线程来处理请求， 第二个参数 是传给新函数的参数列表， 必须为tutle
            # tuple 如果只有一个值，必须带逗号
            _thread.start_new_thread(process_request, (connection,))


if __name__ == '__main__':
    # 生成配置文件并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
