from jinja2 import Environment, FileSystemLoader
import os.path
import time


def log(*arg, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式
    # 实现将 log 内容写入到文件中
    time_style = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_style, value)
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        print(dt, *arg, file=f, **kwargs)


# __file__ 就是本文件的名字
# 得到用户加载模板文件的目录
path = '{}/templates/'.format(os.path.dirname(__file__))
# 创建一个加载器 jinja2 会从这个目录中加载模板
loader = FileSystemLoader(path)
# 用加载器创建一个环境， 有了它才能读取模板文件
env = Environment(loader=loader)


def template(path, **kwargs):
    log('template', path, kwargs)
    """
    本函数接受一个路径和一系列参数
    读取模板并渲染返回
    """
    t = env.get_template(path)
    return t.render(**kwargs)


def response_with_headers(headers, status_code=200):
    """
    根据传递进来的 字典格式的 headers 信息和状态码信息，返回标准格式的响应头信息
    """
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


def http_response(body, headers=None):
    """
    headers 是可选的字典格式的 HTTP 头
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    log('http_response', headers)
    if headers is not None:
        header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    log('http_response', header)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')
