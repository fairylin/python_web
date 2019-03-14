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
    def find_all(cls, **kwargs):
        """
        us = User.find_all(password='123')
        上面这句可以以 list 的形式返回所有 password 属性为 '123' 的 User 实例
        如果没这样的数据, 返回 []

        注意, 这里参数的名字是可以变化的, 所以应该使用 **kwargs 功能
        :param kwargs:
        :return:
        """
        k, v = '', ''
        kv_list = []
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                kv_list.append(m)
        return kv_list

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

    def __repr__(self):
        """
        这是一个 魔法函数
        :return:
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)

    def save(self):
        """
        save函数用户把一个 Model 的实例保存到文件中
        :return:
        """
        log('debug save')
        models = self.all()
        # log('models', models)
        first_index = 0
        if self.__dict__.get('id') is None:
            # 加上 id  此处的 0 表示，需要当 models 的长度为多少时，开始进行 id 的增加
            if len(models) > 0:
                log('用log可以查看代码执行的走向')
                # 并不是第一个数据
                self.id = models[-1].id + 1
            else:
                # 是第一个数据
                log('first index', first_index)
                self.id = first_index
            models.append(self)
        else:
            # 有 id 说明已经是存在于数据文件中的数据
            # 那么就找到这条数据并替换
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            # 看看是否找到下标
            # 如果找到， 就替换掉这条数据
            if index > -1:
                models[index] = self
        # __dict__ 是包含了对象所有属性和值的字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)


# 以下两个类用户实际的数据处理
# 因为继承了Model
# 所以可以直接save load
class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')

    def validate_login(self):
        u = User.find_by(username=self.username)
        return u is not None and u.password == self.password

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


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
    users = User.find_all()
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


if __name__ == '__main__':
    test()
