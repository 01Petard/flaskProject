from flask import Flask

app = Flask(__name__)


@app.route('/flask/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/hello/<string:name>')
def name(name):
    return '你的名字是： ' + name


@app.route('/hello/<int:money>')
def pay(money):
    return '你付了 %d 元' % money


@app.route('/hello/<float:rest>')
def rest(rest):
    return '你还剩 %f 元' % rest


if __name__ == '__main__':
    app.run(port=6000, debug=True, threaded=True)
