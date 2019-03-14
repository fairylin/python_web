from models import Model
import time


# 继承 Model 的 Todo 类
# class Todo(Model):
#     def __init__(self, form):
#         self.id = form.get('id', None)
#         if self.id is not None:
#             self.id = int(self.id)
#         self.title = form.get('title', '')
class Todo(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.title = form.get('title', '')
        self.user_id = int(form.get('user_id', -1))
        self.create_time = form.get('create_time', int(time.time()))
        self.update_time = form.get('update_time', int(time.time()))
