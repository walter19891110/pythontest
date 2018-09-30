

from flask import Flask, jsonify, request, make_response, abort
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource


# 初始化参数，尽量使用你的包名或模块名
app = Flask("test_flask")
auth = HTTPBasicAuth()  # HTTP的基本认证模式 用户名+密码

# 任务列表
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')  # 修饰器
def index():
    return 'Hello,world!'


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))  # 检查tasks内部元素，是否有元素的id的值和参数id相匹配
    if len(task) == 0:                                       # 有的话，就返回列表形式包裹的这个元素，如果没有，则报错404
        abort(404)
    return jsonify({'tasks': task[0]})                      # 否则，将这个task以JSON的响应形式返回


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:  # 如果请求里面没有JSON数据，或者在JSON数据里面，title的内容是空的
        abort(404)  # 返回404报错
    task = {
        'id': tasks[-1]['id'] + 1,  # 取末尾task的id号，并加一作为新的数据的id号
        'title': request.json['title'],  # title必须要设置，不能为空
        'description': request.json.get('description', ""),  # 描述可以添加，但是也可以不写，默认为空
        'done': False
    }

    tasks.append(task)  # 完了以后，添加这个task进tasks列表
    return jsonify({'task': task}), 201  # 并返回这个添加的task内容，和状态码


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)  # 调试的时候用，遇到错误会自动弹出用户名和密码框
    # return make_response(jsonify({'error': 'Unauthorized access'}), 403)  # 正式的时候用，返回403，不会弹出对话框，让客户端自己处理登录问题

if __name__ == "__main__":

    print("test flask!")

    app.run(debug=True)  # 调试时用，好处，修改代码后，不用重启程序