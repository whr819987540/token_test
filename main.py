from urllib import request
from flask import Flask,redirect,render_template,request,url_for
from flask_bootstrap import Bootstrap
from db.db import DB
app = Flask(__name__)
Bootstrap(app)
db = DB()

@app.route("/",methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login/",methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("login.html",text="请登录")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        ret = db.login(username,password)
        print(ret)
        if ret[0]:
            # redirect 加参数只能在路由里面
            return redirect(url_for("info",username=username))
        else:
            return render_template("login.html",text=ret[1])

@app.route("/register/",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html",text="请注册") 
    elif request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        password = request.form.get("password")
        ret = db.register(username,name,password)
        print(ret)
        if ret[0]:
            return redirect(url_for("login"))
        else:
            return render_template("register.html",text=ret[1]) 
        
# 应该修改为需要登录
@app.route("/info/",methods=["GET"])
def info():
    username = request.args.get("username")
    ret = db.name_select(username)
    if ret[0]:
        return render_template("info.html",text=f"Hello, {ret[1]}.")
    else:
        return render_template("login.html",text=ret[1])

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000,debug=True)