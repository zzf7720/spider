from flask import Flask,g
from Proxy_Pool.db import Redis_Client

__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g,'redis'):
        g.redis = Redis_Client()
    return g.redis

@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'

@app.route('/random')
def get_proxy():
    conn = get_conn()
    return conn.random()

@app.route('/count')
def get_counts():
    conn = get_conn()
    return str(conn.count())

if __name__ == '__main__':
    app.run()

