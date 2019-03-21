from models import Model
from models.user import User
from utils import log


# 微博类
class Weibo(Model):
    def __init__(self, form, user_id=-1):
        log('weibo_init')
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        # self.c
        # 和别的数据关联的方式，用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)

    def comments(self):
        # return [c for c in Comment.all() if c.weibo_id == self.id]
        return Comment.find_all(weibo_id=self.id)


class Comment(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.content = form.get('content', )

        # 和别的数据关联的方式， 用 user_id 表明拥有它的实例
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = int(form.get('weibo_id', -1))

    def user(self):
        u = User.find_by(id=self.user_id)
        return u


def test_tweet():
    # 用户 1 发微博
    form = {
        'content': 'hello tweet'
    }
    t = Weibo(form, 1)
    t.save()
    # 用户 2 评论微博
    form = {
        'content': '楼主说得对'
    }
    c = Comment(form, 2)
    c.tweet_id = 1
    c.save()
    # 取出微博 1 的所有评论
    t = Weibo.find(1)
    print('comments, ', t.comments())
    pass


def test():
    cs = Comment.find_all(user_id=2)
    print(cs, '评论数', len(cs))
    # test_tweet()
    # 测试数据关联
    # form = {
    #     'task': 'gua 的 todo'
    # }
    # Todo.new(form, 1)
    # 得到 user 的所有 todos
    # u1 = User.find(1)
    # u2 = User.find(2)
    # ts1 = u1.todos()
    # ts2 = u2.todos()
    # log('gua de todos', ts1)
    # log('xiao de todos', ts2)
    # assert len(ts1) > 0
    # assert len(ts2) == 0
    #
    # test_create()
    # test_read()
    # test_update()
    # test_delete()
    # Todo.complete(1, True)
    pass