# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import User, Question, Comments
from exts import db
from decoration import login_require

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    content = {
        'question': Question.query.order_by(Question.create_time.desc()).all()
    }
    return render_template('index.html', **content)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        phone = request.form.get('phone')
        pwd = request.form.get('pwd')

        user = User.query.filter(User.phone == phone, User.password == pwd).first()

        if user:
            session['user_id'] = user.id
            session.permanent = True

            return redirect(url_for('index'))
        else:
            return '帐号或密码错误'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        phone = request.form.get('phone')
        username = request.form.get('username')
        pwd_one = request.form.get('pwd_one')
        pwd_two = request.form.get('pwd_one')

        user = User.query.filter(User.phone == phone).first()

        if user:
            return '用户已存在'
        else:
            if pwd_one != pwd_two:
                return '两次输入密码不一致'
            else:
                user = User(phone=phone, username=username, password=pwd_one)

                db.session.add(user)
                db.session.commit()

                return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/ask', methods=['GET', 'POST'])
@login_require
def ask():
    if request.method == 'GET':
        return render_template('ask.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)

        user_id = session.get('user_id')
        print(user_id)
        user = User.query.filter(User.id == user_id).first()
        question.author = user

        db.session.add(question)
        db.session.commit()

        return redirect(url_for('index'))


@app.route('/detail/<int:question_id>')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    #get all comments
    #question_model.comments_all()
    return render_template('detail.html', question_model=question_model)


@app.route('/comment', methods=['POST'])
@login_require
def comment():
    new_comment = request.form.get('comment')
    question_id = request.form.get('question_id')
    answer = Comments(comment_content=new_comment)

    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question

    db.session.add(answer)
    db.session.commit()

    return redirect(url_for('detail', question_id=question_id))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
