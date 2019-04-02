from models import Model


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    def __int__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    @classmethod
    def new(cls, form):
        """
        创建并保存一个 todo 并且返回它
        Todo.new({'title': '吃饭'})
        :param form: 一个字典 包含了 todo 的数据
        :return: 创建的 todo 实例
        """
        # 下面一行相当于 t = Todo(form)
        t = cls(form)
        t.save()
        return t

    def salted_password(self, password, salt='!@#AERQEWTDGVfasdfk;'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha3_256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        # 用 ascii 编码转换为 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_by(username=name):
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        u = User(form)
        user = User.find_by(username=u.name)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None