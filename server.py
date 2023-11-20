from flask import Flask, g
from storage import RedisClient
from settings import API_HOST, API_PORT, API_THREADED


app = Flask(__name__)


@app.route('/getproxy')
def getproxy():
    if not hasattr(g, 'db'):
        g.db = RedisClient()
    try:
        host, port = str(g.db.random()).split(':')
        return {'code': 1, 'ip': host, 'port': port}
    except Exception as e:
        return {'code': 0, 'msg': str(e)}


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)
