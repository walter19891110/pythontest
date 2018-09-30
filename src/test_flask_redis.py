from flask import Flask
import rediscluster
import time

app = Flask(__name__)


class MyRedis():

    def conn_redis_cluster(self):
        redis_nodes = [{"host": "127.0.0.1", "port": "6379"},
                       {"host": "127.0.0.1", "port": "6479"},
                       {"host": "127.0.0.1", "port": "7379"},
                       {"host": "127.0.0.1", "port": "7479"},
                       {"host": "127.0.0.1", "port": "8379"},
                       {"host": "127.0.0.1", "port": "8479"}
                      ]
        self.r = rediscluster.StrictRedisCluster(startup_nodes=redis_nodes)

    def set(self, key, value, ex):
        self.r.set(key, value, ex)

    def get(self, key):
        return self.r.get(key)


my_redis = MyRedis()
my_redis.conn_redis_cluster()


@app.route('/')
def index():
    key = 'time'
    value = time.time()
    my_redis.set(key, value, 100)
    print(my_redis.get("name"))

    return str(value)

if __name__ == '__main__':
    app.run(debug=True)
