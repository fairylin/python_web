from models import Model
from utils import log

import time


# 继承 Model 的 Todo 类
class Todo(Model):
    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.completed = False
        self.ct = int(time.time())
        self.ut = self.ct

    @classmethod
    def new(cls, form):
        """
        创建并保存一个 todo 并返回他
        Todo.new({'task': '吃饭'})
        :param form 一个字典，包含了todo的数据
        :return 创建的 todo 实例

        cls 就相当于指定类的初始化过程
        """
        # print("Model_new", form)
        # 下面这一行相当于 t = Todo(form)
        # t = cls(form)
        t = cls(form)
        t.save()
        return t

    @classmethod
    def update(cls, id, form):
        t = cls.find(id)
        valid_names = [
            'task',
            'completed'
        ]
        for key in form:
            # 这里只要更新我们想要更新的内容
            if key in valid_names:
                setattr(t, key, form[key])
        t.save()
        return t

    @classmethod
    def complete(cls, id, completed):
        """
        用法很简单
        Todo.complete(1, True)
        Todo.complete(2, True)
        """
        t = cls.find(id)
        t.completed = completed
        t.save()
        return t

    def is_owner(self, id):
        return self.user_id == id

    def ct(self):
        format = '%H:%M:%S'
        value = time.localtime(self.updated_time)
        dt = time.strftime(format, value)
        return dt


def test_todo_ct():
    form = {
        'id': 1,
        'task': 'asdsadfaasd',
        'completed': False,
        'user_id': -1,
        'created_time': 1551106417,
        'updated_time': '22:53:37'
    }
    t = Todo(form)
    update_time = t.ct()
    log('test_todo_ct', update_time)