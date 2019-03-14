import json
from utils import log


def save(data, path):
    """
    本函数把一个 dict 或者 list 写入文件
    date 是 dict 或者 list
    path 是文件保存的路径
    :param data:
    :param path:
    :return:
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
    :param path:
    :return:
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
        classname = cls.__name__
        path = '{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        # 下面一句相当于 User(form) 或者 Message(form)
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        """
        得到类中所有存储的实例
        :return:
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    def save(self):
        """
        save函数用户把一个 Model 的实例保存到文件中
        :return:
        """
        models = self.all()
        log('models', models)
        models.append(self)
        log('models after append', models)
        # __dict__ 是包含了对象所有属性和值的字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        """
        这是一个 魔法函数
        :return:
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)


# 以下两个类用户实际的数据处理
# 因为继承了Model
# 所以可以直接save load
class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        # users = User.all()
        # for user in users:
        #     if user.__getattribute__('username') == self.username and user.__getattribute__('password') == self.password:
        #         return True
        return self.username == 'gua' and self.password == '123'

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


# 定义一个 class 用户保存 message
class Message(Model):
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')