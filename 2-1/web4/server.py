import socket
import urllib.parse

from utils import log

from routes import route_static
from routes import route_dict


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
        User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36
        Cookie: height=169; user=gua
        :return:
        """
        # header = [
        #     'Host: 127.0.0.1:3000',
        #     'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
        #     # 'Cookie: height=169; user=gua'
        # ]
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.header[k] = v
        self.add_cookies()

    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f


# 创建一个全局的请求对象
request = Request()


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
        return path, query


def response_for_path(path):
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
        # '/': route_index,
        # '/login': route_login,
        # '/message': route_message,
    }
    r.update(route_dict)
    response = r.get(path, error)
    # log('response_for_path  response(request)****', response(request))
    # if b'image/' not in response(request):
    #     log(response(request).decode(encoding='utf-8'))
    return response(request)


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    log('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        # 无限循环来处理请求
        while True:
            # 监听 接受 读取请求数据 解码成字符串
            s.listen(5)
            connection, address = s.accept()
            r = connection.recv(1000)
            r = r.decode('utf-8')
            # log('ip and request, {}\n{}'.format(address, request))
            # 因为 chrome 会发送空请求导致 split 得到空的list
            # 所以在这里判断一下防止程序崩溃
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            # 设置 request 的 method
            request.method = r.split()[0]
            # 把 body 放入到 request 中
            request.body = r.split('\r\n\r\n', 1)[1]
            # 把 header 放入到 request 中
            request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
            log('request content',request.method, '\n', request.header, '\n', request.cookies, '\n', request.body, '\n')
            # 用 response_for_path 函数来得到 path 对应的相应内容
            response = response_for_path(path)
            # 把响应发送给客户端
            connection.sendall(response)
            # 处理完请求后，关闭连接
            connection.close()


if __name__ == '__main__':
    # 生成配置文件并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
