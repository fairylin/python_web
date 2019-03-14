# -*- coding:utf-8 -*-
# datetime:2019/2/14 13:58
# software: PyCharm
import socket
import ssl

"""
2017/02/16
作业 1


资料:
在 Python3 中，bytes 和 str 的互相转换方式是
str.encode('utf-8')
bytes.decode('utf-8')

send 函数的参数和 recv 函数的返回值都是 bytes 类型
其他请参考上课内容, 不懂在群里发问, 不要憋着
"""


# 1
# 补全函数
def protocol_of_url(url):
    """
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表协议的字符串, 'http' 或者 'https'
    """
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        u = url

    return protocol, u
    # pass


# 2
# 补全函数
def host_of_url(url):
    """
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表主机的字符串, 比如 'g.cn'
    """
    # 检查默认的path
    i = url.find('/')
    if i == -1:
        host = url
        path = '/'
    else:
        host = url[:i]
        path = url[i:]

    return host, path


# 3
# 补全函数
def port_of_url(url):
    """
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表端口的字符串, 比如 '80' 或者 '3000'
    注意, 如上课资料所述, 80 是默认端口
    """
    protocol = 'http'
    port_dict = {
        'http': 80,
        'https': 443
    }
    port = port_dict[protocol]
    if ':' in url:
        h = url.split(':')
        port = int(h[1])

    return port


# 4
# 补全函数
def path_of_url(url):
    """
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表路径的字符串, 比如 '/' 或者 '/search'
    注意, 如上课资料所述, 当没有给出路径的时候, 默认路径是 '/'
    """
    i = url.find('/')
    if i == -1:
        path = '/'
    else:
        # path = url.split('/', 1)[1]
        path = url[i:]
    return path


# 4
# 补全函数
def parsed_url(url):
    """
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'
    返回一个 tuple, 内容如下 (protocol, host, port, path)
    """
    # 获取协议信息
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        u = url

    # 检查默认的path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # 获取端口信息
    port_dict = {
        'http': 80,
        'https': 443
    }

    port = port_dict[protocol]
    if ':' in host:
        h = host.split(':')
        host = h[0]
        port = int(h[1])
    print(url, protocol, host, port, path)
    return protocol, host, port, path


def socket_by_protocol(protocol):
    """
    根据协议返回 socket实例
    """
    if protocol == 'http':
        s = socket.socket()
    else:
        # HTTPS 协议需要使用ssl.wrap_socket 包装一下原始的socket
        # 除此之外无其他差别
        s = ssl.wrap_socket(socket.socket())
    return s


def response_by_socket(s):
    """
    参数是一个socket 实例
    返回这个socket 读取的所有数据
    """
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r
    return response


def parsed_response(r):
    """
    把response 解析出 状态码 headers body 并返回
    状态码 是 int
    headers 是 dict
    body 是 str
    """
    headers, body = r.split('\r\n\r\n', 1)
    h = headers.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        print(line)
        k, v = line.split(': ')
        headers[k] = v
    return status_code, headers, body


# 5
# 把向服务器发送 HTTP 请求并且获得数据这个过程封装成函数
# 定义如下
# 将复杂的逻辑全部封装为函数
def get(url):
    """
    用GET 请求 url 并返回响应
    本函数使用上课代码 client.py 中的方式使用 socket 连接服务器
    获取服务器返回的数据并返回
    注意, 返回的数据类型为 bytes
    """
    protocol, host, port, path = parsed_url(url)
    # 写 what 不写 how
    s = socket_by_protocol(protocol)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost:{}\r\nConnection:close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = response_by_socket(s)
    r = response.decode(encoding)

    status_code, headers, body = parsed_response(r)
    if status_code == 301:
        url = headers['Location']
        return get(url)

    return status_code, headers, body


# 使用
def main():
    url = 'http://movie.douban.com/top250'
    status_code, headers, body = get(url)
    print(status_code, headers, body)


# 以下 以test开头的函数是单元测试
def test_parsed_url():
    """
    parsed_url 函数很容易出错， 所以我们写测试函数来运行看检测是否正确运行
    """
    http = 'http'
    https = 'https'
    host = 'g.cn'
    path = '/'
    test_items = [
        ('http://g.cn', (http, host, 80, path)),
        ('http://g.cn/', (http, host, 80, path)),
        ('http://g.cn:90', (http, host, 90, path)),
        ('http://g.cn:90/', (http, host, 90, path)),
        #
        ('https://g.cn', (https, host, 443, path)),
        ('https://g.cn:233/', (https, host, 233, path)),
    ]
    for t in test_items:
        url, expected = t
        u = parsed_url(url)
        # assert 是一个语句 名字 叫 断言
        # 如果断言成功， 条件成立， 则通过测试
        # 否则测试失败， 中断程序， 报错
        e = "parsed_url ERROR, ({}) ({}), ({})".format(url, u, expected)
        assert u == expected, e


def test_parsed_response():
    """
        测试是否能正确解析响应
        """
    # NOTE, 行末的 \ 表示连接多行字符串
    response = 'HTTP/1.1 301 Moved Permanently\r\n' \
               'Content-Type: text/html\r\n' \
               'Location: https://movie.douban.com/top250\r\n' \
               'Content-Length: 178\r\n\r\n' \
               'test body'
    status_code, header, body = parsed_response(response)
    assert status_code == 301, '状态码错误'
    assert len(list(header.keys())) == 3, '头部信息不足3条'
    assert body == 'test body', 'body信息错误'
    pass


def test_get():
    """
        测试是否能正确处理 HTTP 和 HTTPS
        """
    urls = [
        'http://movie.douban.com/top250',
        'https://movie.douban.com/top250',
    ]
    # 这里就直接调用了 get 如果出错就会挂, 测试得比较简单
    for u in urls:
        get(u)
    pass


def test():
    """
    用于测试的主函数
    :return:
    """
    # test_parsed_url()
    # test_get()
    test_parsed_response()


if __name__ == '__main__':
    # main()
    test()
