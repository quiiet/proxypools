from flask import Flask, g
from proxypools.my_redis.redis_func import RedisSave


__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisSave()
    return g.redis


@app.route('/')
def index():
    return '<h2>Welcome to The ProxyPool</h2>'


@app.route('/random')
def get_proxy():
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_counts():
    conn = get_conn()
    return str(conn.count())
