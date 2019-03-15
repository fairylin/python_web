/* 1, 给 add button 绑定事件
// 2，在事件处理函数中，获取 input 的值
// 3，用获取的值 组装一个 todo-cell HTML 字符串
// 4，插入到 todo-list 中
*/

// 定义一个 log函数，输出我们的日志文件
var log = function() {
    console.log.apply(console, arguments);
}

// 传入一个值，在 HTML 文本中找到对应的 HTML 内容
var e = function(sel) {
    log('进入函数e 获取需要输出的值， 此处需要获取的元素节点为：', sel)
    return document.querySelector(sel);
}

// 定义函数，根据输入的参数值，生成 todo 模板
var todoTemplate = function(todo) {
    log('进入函数 todoTemplate 获取需要输出的值， 此处需要获取的元素节点为：', todo)
    var t = `
        <div class="todo-cell">
            <button class="todo-delete">删除</button>
            <span>${todo}</span>
        </div>
    `
    return t
    /*
    上面的写法在python 中是这样的
    t = """
    <div class='todo-cell'>
        <button class='todo-delete'>删除</button>
        <span>{}</span>
    </div>
    """.format(todo)
    */
    log('todoTemplate, t', t)
}

// 创建一个插入 todo 列表项到 HTML 页面的 HTML 文本
var insertTodo = function(todo) {
    log('进入insertTodo函数，', todo)
    var todoCell = todoTemplate(todo)
    // 插入 todo-list
    var todoList = e('.todo-list')
    log('insertTodo, todoList', todoList)
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

var clear_input = function(input) {
    input.value = ''
}


// 给新增按钮 绑定监听事件
var b = e('#id-button-add')
// 注意， 第二个参数可以直接给出定义函数
b.addEventListener('click', function() {
    log('click')
    // 在页面下方添加 一个检查结果标识
    var msg = e('#id-msg')
    var input = e('#id-input-todo')
    var body = e('body')
    var todo = input.value
    // 匹配以字母开头的字符串信息
    var reg= /^[A-Za-z]/;
    // 匹配以字符串或者数字结尾的字符串
    var reg2 = /[A-Za-z0-9]$/;
    // var reg3 = /[^A-Z_a-z0-9]/;
    if (todo.length > 2 && reg.test(todo) && todo.length < 10 && reg2.test(todo)) {
        log('if')
        console.log('todo.length', todo.length)
        // 逐个检查字符串中的各个字符值，如果不在 字母 数字 下划线范围内，则报错退出
        for (var i = 0; i < todo.length; i++) {
            console.log(i)
            // todo.indexOf 判断一个字符是否在一个字符串中，如果在，返回下标，如果不在返回-1
            if(todo.indexOf(i) != -1) {
                continue;
            }
        }
        // log('todo', todo)
        insertTodo(todo)
        msg.innerHTML = '检查通过,插入数据成功!'
        log('检查通过')
    } else {
        // alert('输入的字符串长度应该大于2个长度 且 第一个字符必须为字母')
        msg.innerHTML = '用户名错误!'
        log('用户名错误')
    }
    // 提交内容后，将输入框置为空
    clear_input(input)
})

/*
给 删除 按钮 绑定删除的事件
1，绑定事件
2，删除整个 todo-cell 元素
*/

var todoList = e('.todo-list')
// 事件响应函数 会被传入一个参数，就是事件本身
todoList.addEventListener('click', function(event) {
    // log('click todoList', evnet)
    // 我们可以通过event.target 来得到被点击的 元素
    var self = event.target
    // log('被点击的元素', self)
    // 通过比较被点击元素的 class 来判断元素是否是我们想要的
    // classList 属性保存了元素的所有class
    // 在HTML 中 一个元素可以有多个class 用空格分开
    // log(self.classList)
    // 判断是否拥有某个 class 的方法如下
    if (self.classList.contains('todo-delete')) {
        log('点到了 删除按钮')
        // 删除 self 的父节点
        // parentElement 可以访问到元素的父节点
        log('self.parentElement', self.parentElement)
        self.parentElement.remove()
    } else {
        // log('点击的不是删除按钮')
    }
})


//
// // 创建一个插入 todo 列表项到 HTML 页面的 HTML 文本
// var editTodo = function(todo) {
//     log('进入 editTodo 函数，', todo)
//     var todoCell = todoTemplate(todo)
//     // 插入 todo-list
//     var todoList = e('.todo-list')
//     log('insertTodo, todoList', todoList)
//     todoList.insertAdjacentHTML('beforeend', todoCell)
// }
//
// /*
// 编辑一个 todo 信息
// */
// var todoList = e('.todo-list')
// todoList.addEventListener('click', function(event) {
//     var self = event.target
//     log('self', self)
//     if (self.classList.contains('todo-edit')) {
//         log('点到了，编辑按钮')
//
//         log('click edit')
//         var input = e('#id-input-todo')
//         var todo = input.value
//         log('edit todo', todo)
//         editTodo(todo)
//     }
// })
