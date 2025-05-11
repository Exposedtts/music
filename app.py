# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, session, redirect, send_from_directory
from utils import query
from utils.shujufx import *
import os
app = Flask(__name__)
app.secret_key = 'Thsi is session_key you know ?'

#登录界面
@app.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        request.form = dict(request.form)

        def filer_in(item):
            return request.form['username'] in item and request.form['password'] in item

        users = query.querys('select * from user', [], 'select')
        filter_user = list(filter(filer_in, users))

        if len(filter_user):
            session['username'] = request.form['username']
            return redirect('/home')
        else:
            return render_template('error.html', message='邮箱或者密码错误')


# 退出路由
@app.route('/loginOut')
def loginOut():
    session.clear()
    return redirect('/login')


# 注册路由
@app.route('/register', methods=['GET', 'POST'])
def register():  # put application's code here
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        request.form = dict(request.form)
        print(request.form)
        # 判断第一次输入的密码和第二次输入的密码是否相同
        if request.form['password'] != request.form['passwordChecked']:
            return render_template('error.html', message='两次密码不符合')

        # 在之前的数据表里面是否存在
        def filter_fn(item):
            return request.form['username'] in item

        # 数据库
        users = query.querys('select * from user', [], 'select')
        filter_list = list(filter(filter_fn, users))
        if len(filter_list):
            return render_template('error.html', message='该用户已被注册')
        else:
            query.querys('insert into user(email,password,username) values(%s,%s,%s)',
                         [request.form['email'], request.form['password'], request.form['username']])
            return redirect('/login')
@app.route('/favicon.ico')#设置icon
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'templates'),#对于当前文件所在路径,比如这里是static下的favicon.ico
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# 重启项目的时候自动导入到登录界面  /login
@app.route('/')
def allRequest():
    return redirect('/login')

app.config['DEBUG'] = True

@app.route('/home', methods=['GET', 'POST'])
def home():
    # 获取用户名
    email = session.get('email')
    username = session.get('username')
    return render_template(
        'index.html',
        email = email,
        username=username,

    )
#歌单类型图
@app.route('/gendnxt', methods=['GET', 'POST'])
def gendnxt():
    username = session.get('username')
    typeEcharDate = gdlxt()
    return render_template(
        '歌单类型图.html',
        username= username,
        typeEcharDate=typeEcharDate,
    )

#歌单播放量排行榜
@app.route('/gedanlxphb', methods=['GET', 'POST'])
def gedanlxphb():
    username = session.get('username')
    mzi, bofcshu = gdbflphb()
    return render_template(
        '歌单播放量排行榜.html',
        username= username,
        mzi = mzi,
        bofcshu = bofcshu,
    )

#歌单收藏排行榜
@app.route('/gedanscphb',methods=['GET', 'POST'])
def gedanscphb():
    username = session.get('username')
    gedanshouc = gendanscphb()
    return render_template(
        '歌单收藏排行榜.html',
        username = username,
        gedanshouc = gedanshouc
    )

# 各年发布英文专辑数量
@app.route('/genianfbywzjsl',methods=['GET', 'POST'])
def genianfbywzjsl():
    username = session.get('username')
    nian,yfshuliang=gnfbywzjsl()
    return render_template(
        '各年发布英文专辑数量.html',
        username = username,
        nian =nian,
        yfshuliang = yfshuliang,
    )


# 专辑销量类型评分榜
@app.route('/zhuanjixlnxpfb', methods=['GET', 'POST'])
def zhuanjixlnxpfb():
    username = session.get('username')
    leixin, gpf, qpf, ypf = zjxlpfb()
    return render_template(
        '专辑销量类型评分榜.html',
        username = username,
        leixin = leixin,
        gpf = gpf,
        qpf = qpf,
        ypf = ypf,

    )
# 歌曲时长分析
@app.route('/gequshichang',methods=['GET', 'POST'])
def gequshichang():
    username = session.get('username')
    shic, shul = gqscfx()
    return render_template(
        '歌曲时长分析.html',
        username = username,
        shic=shic,
        shul=shul,
    )
# 歌名词云图
@app.route('/gemingcyt',methods=['GET', 'POST'])
def gemingcyt():
    username = session.get('username')
    # ciyuntutu = gmcyt()
    return render_template(
        '歌名词云图.html',
        username = username,
        # ciyuntutu = ciyuntutu,
    )

# 歌手前三十发歌量
@app.route('/geshouciyt',methods=['GET','POST'])
def geshouciyt():
    username =session.get('username')
    geshoucyuntu = gscyt()
    return render_template(
        '歌手前三十发歌量.html',
        username = username,
        geshoucyuntu = geshoucyuntu,
    )

#小时时间段评论次数
@app.route('/xiaoshisjdplcs',methods=['GET','POST'])
def xiaoshisjdplcs():
    username = session.get('username')
    xiaoshipls,plshu = dzqsdpl()
    return  render_template(
        '小时时间段评论次数.html',
        username = username,
        xiaoshipls = xiaoshipls,
        plshu = plshu,
    )
@app.route('/erroryemian')
def erroryemian():
    return  render_template(
        'login.html',
    )
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8000, debug=True)
    from livereload import Server
    app.run(debug=True)
    server = Server(app.wsgi_app)
    server.watch('**/*.*')
    server.serve()
    # app.run()
