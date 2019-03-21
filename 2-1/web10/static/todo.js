// 定义函数，根据输入的参数值，生成 todo 模板
var todoTemplate = function(todo) {
    // log('进入函数 todoTemplate 获取需要输出的值， 此处需要获取的元素节点为：', title)
    var title = todo.title
    var id = todo.id
    var t = `
        <div class="todo-cell" data-id="${id}">
            <button class="todo-delete" id="">删除</button>
            <span>${title}</span>
        </div>
    `
    // log('todoTemplate, t', t)
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
}

// 创建一个插入 todo 列表项到 HTML 页面的 HTML 文本
var insertTodo = function(todo) {
    // log('进入insertTodo函数，', todo.title)
    var todoCell = todoTemplate(todo)
    // 插入 todo-list
    var todoList = e('.todo-list')
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

var clear_input = function(input) {
    input.value = ''
}

// 加载 Todo.txt 中的所有的todo 信息，并添加到页面中
var loadTodos = function() {
    // 调用 ajax api 来载入数据
    apiTodoAll(function (r) {
        // log('loadTodos r', r, typeof r)
        // 解析为数组
        var todos = JSON.parse(r)
        // log('todos', todos, typeof todos)

        // 循环添加到页面中
        for(var i = 0; i < todos.length; i++) {
            var todo = todos[i]
            // log('todo', todo)
            insertTodo(todo)
        }
    })
}

// 为 add 按钮添加绑定事件
var bindEventTodoAdd = function() {
    // 给新增按钮 绑定监听事件
    var b = e('#id-button-add')
    // 注意， 第二个参数可以直接给出定义函数
    b.addEventListener('click', function() {
        var input = e('#id-input-todo')
        var title = input.value
        // lo@g('click add', title)
        var form = {
            "title": title
        }
        clear_input(input)
        form = JSON.stringify(form)
        apiTodoAdd(form, function (r) {
            // 收到返回的数据， 插入到页面中
            var todo = JSON.parse(r)
            insertTodo(todo)
        })
    })
}

// 为删除一个 todo 添加监听事件
var bindEventTodoDelete = function() {
    // 给新增按钮 绑定监听事件
    var todoList = e('.todo-list')
    todoList.addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('todo-delete')) {
            // 删除这个todo
            var todoCell = self.parentElement
            var todo_id = todoCell.dataset.id
            apiTodoDelete(todo_id, function (r) {
                log('删除成功', todo_id)
                todoCell.remove()
            })
        }
    })
}

var bindEvents = function () {
    bindEventTodoAdd()
    bindEventTodoDelete()
}

var __main = function() {
    bindEvents()
    loadTodos()
}

__main()



/*
给 删除 按钮 绑定删除的事件
1，绑定事件
2，删除整个 todo-cell 元素
*/

// var todoList = e('.todo-list')
// // 事件响应函数 会被传入一个参数，就是事件本身
// todoList.addEventListener('click', function(event) {
//     // log('click todoList', event)
//     // 我们可以通过event.target 来得到被点击的 元素
//     var self = event.target
//     // log('被点击的元素', self)
//     // 通过比较被点击元素的 class 来判断元素是否是我们想要的
//     // classList 属性保存了元素的所有class
//     // 在HTML 中 一个元素可以有多个class 用空格分开
//     // log(self.classList)
//     // 判断是否拥有某个 class 的方法如下
//     if (self.classList.contains('todo-delete')) {
//         // log('点到了 删除按钮')
//         // 删除 self 的父节点
//         // parentElement 可以访问到元素的父节点
//         log('self.parentElement', self.parentElement)
//         self.parentElement.remove()
//     } else {
//         // log('点击的不是删除按钮')
//     }
// })


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
