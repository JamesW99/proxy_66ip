#接口模块
#在浏览器中调用redis中的代理


from flask import Flask
from proxy_pool.db import RedisClient
from flask import g         #g常驻


app = Flask(__name__)

def get_conn():                         #具柄：存在直接返回，不存在创建一个
    if not hasattr(g,'redis'):
        g.redis = RedisClient()
    return g.redis



@app.route('/')
def index():                            #如果服务正常启动，则浏览器显示fLaSk
    return "fLaSk"



@app.route('/count')
def get_count():
    conn = get_conn()
    return "存在了{}个代理".format(conn.count())



@app.route('/random')
def get_proxy():
    conn = get_conn()
    return  conn.random()


if __name__ =="__main__":
    app.run()