/*
基本的 js 代码
用来进行前端逻辑的处理，实现基本的函数，且引用顺序在其他的js文件之前
其他的 js 文件即可使用该 js 文件中的内容
1, 给 add button 绑定事件
2，在事件处理函数中，获取 input 的值
3，用获取的值 组装一个 todo-cell HTML 字符串
4，插入到 todo-list 中
*/

// 定义一个 log函数，输出我们的日志文件
var log = function() {
    console.log.apply(console, arguments);
}

// 传入一个值，在 HTML 文本中找到对应的 HTML 内容
var e = function(sel) {
    // log('进入函数e 获取需要输出的值， 此处需要获取的元素节点为：', sel)
    return document.querySelector(sel);
}

/*
ajax 函数
 */
var ajax = function (method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    // 设置 请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据格式为 applicatioin/json
    // 这个不是必须的（浏览器会忽略这个
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function () {
        if (r.readyState === 4) {
            // r.response 存的就是服务器发过来的 放在 HTTP BODY 中的数据
            responseCallback(r.response)
        }
    }
    // data = JSON.stringify(data)
    // 把数据转换为 json 格式字符串
    // data = JSON.parse(data)
    console.log(data, typeof(data))

    // 发送请求
    r.send(data)
}

// TODO API
// 获取所有的todo
var apiTodoAll = function(callback) {
    // log('执行了 apiTodoAll函数', callback)
    var path = '/api/todo/all'
    ajax('GET', path, '', callback)
}

// 增加一个 todo
var apiTodoAdd = function (form, callback) {
    // log('执行了 apiTodoAdd 函数', callback)
    var path = '/api/todo/add'
    // log('apiTodoAdd', form, typeof form, callback)
    ajax('POST', path, form, callback)
}

// 删除一个 todo
var apiTodoDelete = function (id, callback) {
    // log('执行了 apiTodoAdd 函数', callback)
    var path = '/api/todo/delete?id=' + id
    log('apiTodoDelete', id)
    ajax('GET', path, '', callback)
}