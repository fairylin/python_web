import json

from utils import log


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
        # print('load_s_content', path, s)
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
    def _new_from_dict(cls, d):
        # 因为子元素的 __init__ 需要一个 form 参数
        # 这个会给出一个 空字典
        # print('_new_from_dict', d)
        m = cls({})
        for k, v in d.items():
            # setattr 是一个特殊的函数
            # 假设k v 分别是 name 和 gua
            # 它相当于m.name = 'gua'
            setattr(m, k, v)
        return m

    @classmethod
    def all(cls):
        """
        得到类中所有存储的实例
        """
        path = cls.db_path()
        models = load(path)
        # 下面的列表推导式给出的是一个列表格式的数据，生成了包含所有实例的 list
        # 因为这是从 存储的数据文件 中加载数据
        # 所以用 _new_from_dict 这个特殊的函数来初始化数据
        ms = [cls._new_from_dict(m) for m in models]
        # print(ms, type(ms), type(ms[0]))
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
            obj = models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l, path)
            return obj

    def __repr__(self):
        """
        这是一个 魔法函数
        当程序调用 __str__方法时，
        如果不存在__str__方法，则会调用__repr__方法
        :return:
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def json(self):
        """
        返回当前 model 的字典表示
        :return:
        """
        d = self.__dict__.copy()
        return d

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        models = self.all()
        # log('models', models)
        # 如果没有 id，说明是新添加的元素
        # print('调用 save 函数后输出self 属性值， save_self.id', self)
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
