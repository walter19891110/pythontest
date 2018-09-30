

from flask import Flask, jsonify, request, make_response, abort
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource, reqparse, fields, marshal


# 初始化参数，尽量使用你的包名或模块名
app = Flask('test_flask')
auth = HTTPBasicAuth()  # HTTP的基本认证模式 用户名+密码
api = Api(app)

# 任务格式
task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')
}

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


class UserAPI(Resource):
    """
    RESTful API
    用户管理相关
    GET: 查询
    POST: 创建
    PUT: 修改
    DELETE: 删除
    """
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


api.add_resource(UserAPI, '/users/<int:id>', endpoint='user')  # 使用endpoint把函数注册路由到框架上


class TaskListAPI(Resource):
    decorators = [auth.login_required]  # 添加修饰器，用户名密码验证

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided', location='json')
        self.reqparse.add_argument('description', type=str, default="", location='json')
        super(TaskListAPI, self).__init__()  # super() 调用父类函数，这里调用Resource的初始化函数

    def get(self):
        pass

    def post(self):
        pass


class TaskAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        pass

    def put(self, id):
        task = list(filter(lambda t: t['id'] == id, tasks))
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        print(args)
        for k, v in args.items():
            if v is not None:
                task[k] = v
        return {'task':  marshal(task, task_fields)}

    def delete(self, id):
        pass

api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<int:id>', endpoint='task')


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