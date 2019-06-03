from app import app, db
from flask import render_template,flash, redirect, url_for, g
from app.forms import LoginForm, RegisterForm, SearchForm, CreatePost
from flask_login import current_user, login_user, logout_user
from sqlalchemy import text
from app.models import User
import datetime
from flask.json import jsonify

@app.before_request
def before_request():
    g.search_form = SearchForm()


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    is_auth = False
    if current_user.is_authenticated:
        is_auth = True

    #sql = text("select * from post order by date")
    sql = text("select post.id, title, content, date, username from post inner join users on users.id=post.user_id order by date")
    result = db.engine.execute(sql)
    posts = [{key: value for (key, value) in row.items()} for row in result]
    for post in posts:
        post['date'] = post['date'].split(' ', 1)[0]

    auth_form = LoginForm()
    reg_form = RegisterForm()
    if auth_form.validate_on_submit():
        sql = text("select * from users where username=\'{0}\' and password=\'{1}\';"\
                   .format(auth_form.username_login.data, auth_form.password_login.data))
        result = db.engine.execute(sql).first()
        ##if len(dictResult)==0:
        if result == None:
            flash("Invalid username or password")
        else:
            user = User.query.filter_by(username=auth_form.username_login.data).first()

            login_user(user, remember=auth_form.remember_me.data)
            return redirect(url_for('account'))

    if reg_form.validate_on_submit():
        sql = text("insert into users(username, password, email) values (\'{0}\', \'{1}\', \'{2}\');"
                   .format(reg_form.username_reg.data, reg_form.password_reg.data, reg_form.email_reg.data))
        result = db.engine.execute(sql)
        flash('Вы зарегистрированы!')

    if g.search_form.validate():    #Доделать
        search_req = g.search_form.search.data
        sql = text("select * from post where content LIKE '%{}%' or title LIKE '%{}%';".format(search_req))
        result = db.engine.execute(sql)

    return render_template('index.html', auth_form=auth_form, reg_form=reg_form, is_auth=is_auth, posts=posts)

@app.route('/account', methods=['POST', 'GET'])
def account():
    create_form = CreatePost()

    if create_form.validate_on_submit():
        sql = text("insert into post(user_id, title, content, date, views) values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
                   .format(current_user.id, create_form.title.data, create_form.content.data, datetime.datetime.utcnow(), 0));
        result = db.engine.execute(sql)
        return redirect(url_for('index'))
    is_auth = False
    if current_user.is_authenticated:
        is_auth = True
    return render_template("account.html", is_auth=is_auth, create_form=create_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/post/id=<item>')
def post(item):
    sql = text("select * from post where id = \'{}\'".format(item))
    result = db.engine.execute(sql)
    posts = [{key: value for (key, value) in row.items()} for row in result]
    return render_template('post.html', posts = posts)

