import time
from models import Model


# 针对我们的数据 Blog
# 我们要做 4 件事情
"""
C create 创建数据
R read 读取数据
U update 更新数据
D delete 删除数据

Blog.new() 来创建一个 blog
"""


class Blog(Model):
    @classmethod
    def new(cls, form):
        """
        创建并保存一个 todo 并且返回它
        Todo.new({'title': '吃饭'})
        :param form: 一个字典 包含了 todo 的数据
        :return: 创建的 todo 实例
        """
        # 下面一行相当于 m = Todo(form)
        m = cls(form)
        m.save()
        return m

    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.author = form.get('author', '')
        self.ct =int(time.time())

    def time(self):
        format_time = '%y-%m-%d %H:%M:%S'
        value = self.ct
        dt = time.gmtime(value)
        return time.strftime(format_time, dt)


class BlogComment(Model):
    @classmethod
    def new(cls, form):
        """
        创建并保存一个 todo 并且返回它
        Todo.new({'title': '吃饭'})
        :param form: 一个字典 包含了 todo 的数据
        :return: 创建的 todo 实例
        """
        # 下面一行相当于 m = Todo(form)
        m = cls(form)
        m.save()
        return m

    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.author = form.get('author', '')
        self.blog_id = int(form.get('blog_id', 0))
        self.ct = int(time.time())

    def time(self):
        format_time = '%y-%m-%d %H:%M:%S'
        value = self.ct
        dt = time.gmtime(value)
        return time.strftime(format_time, dt)