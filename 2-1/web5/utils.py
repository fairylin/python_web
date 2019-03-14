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
    # print(dt, *arg, **kwargs)