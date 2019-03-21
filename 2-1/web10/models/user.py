from models import Model
from models.todo import Todo
from utils import log


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

    def salted_password(self, password, salt='!@#$$#%$admin'):
        import hashlib

        def md5hex(ascii_str):
            return hashlib.md5(ascii_str.encode('ascii')).hexdigest()

        hash1 = md5hex(password)
        hash2 = md5hex(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        # 用 ascii 编码转换为 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.md5(p)
        return s.hexdigest()

    def is_admin(self):
        return self.role == 1

    def validate_register(self):
        log('validate_register', self)
        pwd = self.password
        self.password = self.salted_password(pwd)
        if User.find_by(username=self.username) is None:
            log('find_user', self.username)
            self.save()
            return self
        else:
            log('该用户名已存在, 请键入其他的用户名')
            return None
        # return len(self.username) > 2 and len(self.password) > 2

    def validate_login(self):
        # u = User.find_by(username=self.username)
        # return u is not None and u.password == self.password
        u = User.find_by(username=self.username)
        if u is not None:
            return u.password == self.salted_password(self.password)
        else:
            return None

    def todos(self):
        # 列表推到式 和过滤方式
        # return [t for t in Todo.all() if t.user_id == self.id]
        ts = []
        for t in Todo.all():
            if t.user_id == self.id:
                ts.append(t)
        return ts


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
