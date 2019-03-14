import json

from utils import log
import time


def save(data, path):
    """
    本函数把一个 dict 或者 list 写入文件
    date 是 dict 或者 list
    path 是文件保存的路径
    """
    # json 是一个序列化/反序列化 list/dict 的库
    # indent 是缩进
    # ensure_ascii=False 用户保存中文（不进行ascii编码）
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并转化为 dict 或者是 list
    path 是文件的保存路径
    因为其中需要读取加载数据，所以应该先放数据到文件中
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)


# Model 是用户存储数据的类
class Model(object):
    # @classmethod 说明这是一个类方法
    # 类方法的调用方式为： 类名.类方法（）
    @classmethod
    def db_path(cls):
        # classmethod 有一个参数是class
        # 所以我们可以得到 class 的名字
        class_name = cls.__name__
        path = 'data/{}.txt'.format(class_name)
        return path

    @classmethod
    def all(cls):
        log("Model all")
        """
        得到类中所有存储的实例
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls(m) for m in models]
        # log('all ', ms)
        return ms

    # @classmethod
    # def new(cls, form):
    #     # 下面一句相当于 User(form) 或者 Message(form)
    #     m = cls(form)
    #     return m

    @classmethod
    def find_all(cls, **kwargs):
        """
        us = User.find_all(password='123')
        上面这句可以以 list 的形式返回所有 password 属性为 '123' 的 User 实例
        如果没这样的数据, 返回 []

        注意, 这里参数的名字是可以变化的, 所以应该使用 **kwargs 功能
        :param kwargs:
        :return:
        """
        kv_list = []
        log('kwargs', kwargs, type(kwargs))
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                kv_list.append(m)
        return kv_list

    @classmethod
    def find_by(cls, **kwargs):
        """
        用法如下， kwargs 是只有一个元素的dict
        u = User.find_by(username='gua')
        :param kwargs:
        :return:
        """
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def delete(cls, id):
        log('delete', id)
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
        # 判断是否占到了这个 id 的数据
        if index == -1:
            # 没找到
            pass
        else:
            models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l, path)

    def __repr__(self):
        """
        这是一个 魔法函数
        :return:
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        # log('debug save')
        models = self.all()
        # log('models', models)
        # 如果没有 id，说明是新添加的元素
        if self.id is None:
            # 设置 self.id
            # 先看看是否是空 list
            if len(models) == 0:
                # 我们让第一个元素的 id 为 1（当然也可以为 0）
                self.id = 1
            else:
                m = models[-1]
                # log('m', m)
                self.id = m.id + 1
            models.append(self)
        else:
            # index = self.find(self.id)
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            log('debug', index)
            models[index] = self
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    # def remove(self):
    #     models = self.all()
    #     if self.__dict__.get('id') is not None:
    #         # 有 id 证明已经是存在于数据文件中的数据
    #         # 那么就找到这条数据并替换之
    #         index = -1
    #         for i, m in enumerate(models):
    #             if m.id == self.id:
    #                 index = i
    #                 break
    #         # 看看是否找到下标
    #         # 如果找到，就替换
    #         if index > -1:
    #             del models[index]
    #     # 保存
    #     l = [m.__dict__ for m in models]
    #     path = self.db_path()
    #     save(l, path)


# 以下两个类用户实际的数据处理
# 因为继承了Model
# 所以可以直接save load
class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')
        self.role = form.get('role', 10)

    def is_admin(self):
        return self.role == 1

    def validate_login(self):
        u = User.find_by(username=self.username)
        return u is not None and u.password == self.password

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


# 继承 Model 的 Todo 类
class Todo(Model):
    def __init__(self, form, user_id=-1):
        log('Todo __init__', form)
        self.id = form.get('id', None)
        self.task = form.get('task', '')
        self.completed = False
        # 和别的数据关联的方式， 用 user_id 表明拥有它的 user 实例
        self.user_id = int(form.get('user_id', user_id))
        # 添加创建和修改时间
        self.created_time = form.get('created_time', None)
        self.updated_time = form.get('updated_time', None)
        if self.created_time is None:
            self.created_time = int(time.time())
            self.updated_time = self.created_time

    @classmethod
    def new(cls, form, user_id=-1):
        """
        创建并保存一个 todo 并返回他
        Todo.new({'task': '吃饭'})
        :param form 一个字典，包含了todo的数据
        :return 创建的 todo 实例
        """
        log("Model new")
        t = cls(form, user_id)
        t.save()
        return t

    @classmethod
    def update(cls, id, form):
        t = cls.find(id)
        log('classmethod update-model', t)
        t.updated_time = int(time.time())
        valid_names = [
            'task',
            'completed'
        ]
        log('update******', form)
        for key in form:
            # 这里只要更新我们想要更新的内容
            if key in valid_names:
                setattr(t, key, form[key])
        log('Todo update', cls)
        t.save()

    @classmethod
    def completed(cls, id, completed):
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


# 定义一个 class 用户保存 message
class Message(Model):
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')


def test_find_by():
    u = User.find_by(id=1)
    u.username = 'test_find_by 瓜'
    u.save()


def test_find_all():
    users = User.find_all(username='root')
    log('test_find_all users', users)


def test_find_all_property():
    u2 = User.find_all(username='admin')
    log('find_all username="admin"', u2)


def test_save():
    form = dict(
        username='gua',
        password='gua',
    )
    u = User(form)
    u.save()
    u.save()
    u.save()
    u.save()
    u.save()


def test():
    test_find_by()
    test_find_all()
    test_find_all_property()
    test_save()


# if __name__ == '__main__':
#     test_find_all()
