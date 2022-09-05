from urllib import request
from flask import Flask, redirect, render_template, request, url_for, Response, make_response, jsonify
from flask_bootstrap import Bootstrap
from db.db import DB
from test.func import *
from test.token_test import token_generate, token_verify
app = Flask(__name__)
Bootstrap(app)
db = DB()
flask_config = load_config()['flask']


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/login/", methods=["POST", "GET"])
def login():
    """
        更新使用逻辑:
            登录成功后,新版本需要返回token,不方便直接重定向
            解决方案:
                1、在前端做检查token然后自动跳转的逻辑(不会)
                2、不自动跳转,让用户手动点击(使用这个)
    """
    if request.method == "GET":
        text = request.args.get("text")
        if text is None:
            text = "please login"
        return render_template("login.html", text=text)
    elif request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        ret = db.login(username, password)
        print(ret)
        if ret[0]:
            # # 将token放到响应的头部
            # response = make_response(render_template(
            #     "info.html", text="login success"))
            # response.status_code = 200
            # response.headers['token'] = token_generate(username)
            # return response
            # # 这个可以满足需求了，但是在页面中url不会变化，不好
            # # 还是应该使用重定向
            # # 重定向的参数可以放到url中

            # 一个需求是重定向时能够传递参数，一般方案是在url中传递参数，因为无法在body部分传递
            return redirect(url_for("info", username=username, token=token_generate(username)))
        else:
            return render_template("login.html", text=ret[1])


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", text="请注册")
    elif request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        password = request.form.get("password")
        ret = db.register(username, name, password)
        print(ret)
        if ret[0]:
            # url_for完全是用来生成url的，第一个参数是与之相同的视图函数
            # print(url_for("info", username=username)) # /info/?username=3
            return redirect(url_for("login"))
        else:
            return render_template("register.html", text=ret[1])


@app.route("/info/", methods=["GET"])
def info():
    print(request.args)
    username = request.args.get("username")
    token = request.args.get("token")
    if username is None or token is None:  # 参数错误，不合法的直接访问
        return redirect(url_for("login"))

    verify_res = token_verify(username, token)
    if not verify_res[0]:
        return redirect(url_for("login", text=verify_res[1]))

    ret = db.name_select(username)
    if ret[0]:
        return render_template("info.html", text=f"Hello, {ret[1]}.")
    else:  # 查询错误
        return redirect(url_for("login", text=ret[1]))


if __name__ == "__main__":
    app.run(host=flask_config['host'],
            port=flask_config['port'], debug=flask_config['debug'])
