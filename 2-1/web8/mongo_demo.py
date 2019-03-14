"""
注意需要首先安装pymongo 这个库

pip install pymongo

安装后可以通过 pymongo 来链接使用mongodb
"""
import pymongo

# 链接 mongo 数据库， 主机是本机， 端口是默认端口
client = pymongo.MongoClient("mongodb://localhost:27017")
print('连接数据库成功', client)

# 设置要使用的数据库（名称）
mongodb_name = 'web8'
# 直接这样就可以创建（如果不存在）并使用这个数据库了
db = client[mongodb_name]


# 插入数据
# ===
# mongo 中的 document 相当于 sqlite 中的 table
# 不需要定义， 直接使用
# 不限定每条数据的字段
# 直接插入新数据， 数据以字典形式提供和操作
# 下面的例子中， user 是文档名（表名）， 不存在的文档会自动创建
# 每条数据有一个自动创建的字段 _id, 可以认为是 mongo 自动创建的主键
import random


def insert():
    u = {
        'name': 'gua',
        'note': '瓜',
        # 放一个随机值来方便区分不同的数据，以便下面的代码使用条件查询
        '随机值': random.randint(0,3),
    }
    db.user.insert_one(u)
# 相当于 db['user'].insert


insert()
insert()
insert()
insert()
insert()
insert()
insert()
print('插入多条数据成功！！！')


# 查找数据
# ====
# find 返回一个可迭代对象， 使用 list 函数转换为数组
def find():
    user_list = list(db.user.find())
    print('所有用户', len(user_list))


find()


# find 可以传入参数作为条件进行查询
# 具体可以很复杂，我们只简单演示
#
# 查询 随机值为 1 的所有数据
def find2():
    query = {
        '随机值': 2,
    }
    print('random 1', list(db.user.find(query)))


# find2()


#
# 查询 随机值 大于1 的所有数据
def find_cond():
    query = {
        '随机值': {
            '$gt': 1
        },
    }
    print('random > 1', list(db.user.find(query)))

#
# find_cond()


#
# 此外还有 $lt $let $get $ne $or 等条件
#
#
# 部分查询， 相当于 select xx, yy from 表名 语句
def find_cond2():
    query = {}
    field = {
        # 字段： 1，表示提取这个字段
        # 不传的 默认为0 表示不提取这个字段
        '_id': 0,
        'name': 1
    }
    print('部分查询， 只查询', list(db.user.find(query, field)))


# find_cond2()


# 更新数据
# ===
# 默认更新第一条查询到的数据
def update():
    query = {
        '随机值': 2,
    }
    form = {
        '$set': {
            'name': 'GUA',
        }
    }
    db.user.update_one(query, form)


# update()
# 如果想要更新所有查询到的数据
# 需要加入下面的参数 {'multi': True}
# db.user.update(query, form, {'multi': True})


# 删除
# ===
# 删除和find是一样的