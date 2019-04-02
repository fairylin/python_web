from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.blog_new import (
    Blog,
    BlogComment,
)
from utils import log

# 将路由定义在蓝图对象中，可以通过在主程序中引入蓝图对象获取路由函数
# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字, 以后会有用(add函数里面就用到了)
# 第二个参数是套路
main = Blueprint('blog_new', __name__)

"""
1.拆分有哪些问题，首先进行页面相关设计和编写。 view over
    1.1
        发博客 link 点进去以后呢 进入发博客的页面
    1.2
        具体的博客内容页面，博客的标题，可以被点击
    2.1
        博客正文页面， 作者, title, 时间, 内容 评论页面
    2.2
        发表评论的窗口， 发表的评论，都是针对这个博客的
    2.3
        显示所有评论的地方， 这个里面会有评论信息
    3.1
        创建blog 的页面

2.组织哪些数据，把数据的操作实现； over
Blog 的数据
1. id int
2. author
3. content
4. create_time

Blog 的方法有哪些
1. new 出来一个blog
2. 根据blog id 拿到一个blog

BlogComment
1. id
2. author
3. comment
4. create_time
5. blog_id 也应该被索引，增加检索速度

BlogComment 操作
1. new
2. blog_id find

3.逻辑。
    3.1
4.开始代码实现，部分实现，部分todo
5.剩下的一点点补全
6.美化页面（css）
"""


@main.route('/')
def index():
    all_blog = Blog.all()
    return render_template('test_blog_index.html', blogs=all_blog)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    Blog.new(form)
    return redirect(url_for('.index'))


@main.route('/new', methods=['GET'])
def new():
    return render_template('test_blog_new.html')


@main.route('/<int:blog_id>', methods=['GET'])
def view(blog_id):
    comments = BlogComment.find_all(blog_id=blog_id)
    blog = Blog.find(blog_id)
    return render_template('test_blog_view.html', blog=blog, comments=comments)


@main.route('/comment/new', methods=['POST'])
def comment():
    form = request.form
    BlogComment.new(form)
    return redirect(url_for('.view', blog_id=form.get('blog_id')))

# 传统  ： 传递回来一个页面
# 现代的方法呢： 是做成服务 访问一个网址，返回了json
# 1. 不同服务，可以用不用的语言
# 2. 拆分服务 业务里面 有一些部分很耗费性能，有一些部分不怎么耗费性能
# 在传统做法里面 n个app 对应不同的用户，让他访问不同的app
# 每个服务独立，复制的单位，是以服务为基础的 微服务，SOA,面向服务的架构
