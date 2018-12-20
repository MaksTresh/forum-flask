from flask import render_template, flash, redirect, url_for, request, send_from_directory
from app import app, db
from app.forms import *
from datetime import datetime
from flask_login import current_user, login_user, logout_user
from app.models import User, Post, Comment
import re
import os

UPLOAD_FOLDER = r'your\path\flood1lka\uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    posts = list()
    for i in Post.query.order_by(Post.rating):
        posts.append({})
        posts[len(posts)-1]['author'] = {'username': User.query.filter_by(id=i.user_id).first().username}
        posts[len(posts)-1]['header'] = i.header
        posts[len(posts)-1]['body'] = i.body
        posts[len(posts)-1]['rate'] = i.rating
        posts[len(posts)-1]['id'] = i.id
        posts[len(posts)-1]['date'] = str(i.timestamp)[:10]
    posts.reverse()
    page = request.args.get('page', default = 1, type = int)
    pages_block = {}
    pages_block['avaible'] = (len(posts) - 1) // 20 + 1
    pages_block['active'] = page if 1 <= page <= pages_block['avaible'] else 1

    login_form = LoginForm()
    register_form = RegistrationForm()
    profile_form = ProfileForm()
    newtheme_form = NewThemeForm()
    return render_template('forum.html', posts=posts, pages_block=pages_block, login_form=login_form, register_form=register_form, profile_form=profile_form, newtheme_form=newtheme_form)

@app.route('/post')
@app.route('/post.html')
def post():
    post_id = request.args.get('id', default = 1, type = int)
    posts = list()
    isExist = False
    for i in Post.query.order_by(Post.rating):
        posts.append({})
        posts[len(posts)-1]['author'] = {'username': User.query.filter_by(id=i.user_id).first().username}
        posts[len(posts)-1]['header'] = i.header
        posts[len(posts)-1]['body'] = i.body
        posts[len(posts)-1]['rate'] = i.rating
        posts[len(posts)-1]['id'] = i.id
        posts[len(posts)-1]['last_seen'] = i.last_seen
        if i.id == post_id:
            isExist = True
            el = posts[len(posts)-1]

    comments = list()
    for i in Comment.query.order_by(Comment.id):
        if i.post_id != post_id:
            continue
        comments.append({})
        comments[len(comments)-1]['author'] = {'username': User.query.filter_by(id=i.user_id).first().username}
        comments[len(comments)-1]['body'] = i.body
        comments[len(comments)-1]['id'] = i.id
        comments[len(comments)-1]['image'] = i.image

    comments_id = request.args.get('comment', default = 1, type = int)
    comments_block = {}
    comments_block['avaible'] = (len(comments) - 1) // 20 + 1
    comments_block['active'] = comments_id if 1 <= comments_id <= comments_block['avaible'] else 1
    
    login_form = LoginForm()
    register_form = RegistrationForm()
    profile_form = ProfileForm()
    newtheme_form = NewThemeForm()
    comment_form = CommentForm()

    if isExist:
        elObj = Post.query.filter_by(id=post_id).first()
        elObj.last_seen = datetime.utcnow().isoformat()
        if int(str(elObj.timestamp)[:10].replace('-','')) - int(str(el['last_seen'])[:10].replace('-','')) >= 5:
            elObj.rating -= 1
            el['rate'] = elObj.rating
        db.session.commit()
        return render_template('post.html', user={'username': 'Эльдар Рязанов'}, post=el, comments=comments, comments_block=comments_block, login_form=login_form, register_form=register_form, profile_form=profile_form, newtheme_form=newtheme_form, comment_form=comment_form)
    else:
        flash('Error: такого поста нет.')
        return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильно введен e-mail или пароль.')
            return redirect(url_for('index'))
        login_user(user)
        return redirect(url_for('index'))
    else:
        flash('Неправильно введен e-mail или пароль.')
        return redirect('index')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрированы!')
        return redirect(url_for('index'))
    else:
        if form.password.data != form.password2.data:
            flash('Пароли не совпадают!')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if current_user.is_authenticated:
        form = ProfileForm()
        user = User.query.filter_by(username=current_user.username).first()
        if form.validate_on_submit() and (form.email.data != '' or form.email2.data != ''):
            prov = User.query.filter_by(email=form.email2.data).first()
            if prov is not None:
                flash('Email занят!')
                return redirect(url_for('index'))
            if form.email.data != '' or form.email2.data != '':
                if form.email.data != user.email:
                    flash('Неверный старый email.')
                else:
                    flash('Email успешно изменен.')
                    user.email = form.email2.data
        elif form.email.data != '' or form.email2.data != '':
            flash('Неверный формат эл. адресса!')
        if form.password.data != '' or form.password2.data != '':
            if not user.check_password(form.password.data):
                flash('Неверный старый пароль.')
            else:
                flash('Пароль успешно изменен.')
                user.set_password(form.password2.data)
        db.session.commit()
        return redirect(url_for('index'))
    flash('Error: no login')
    return redirect(url_for('index'))

@app.route('/newtheme', methods=['GET', 'POST'])
def newtheme():
    if current_user.is_authenticated:
        form = NewThemeForm()
        if form.validate_on_submit():
            if len(form.header.data) > 30:
                flash('Превышено максимальное количество символов в заголовке (max.: 30)!')
                return redirect(url_for('index'))
            if len(form.body.data) > 1000:
                flash('Превышено максимальное количество символов в описании темы (max.: 1000)!')
                return redirect(url_for('index'))
            post = Post(header=form.header.data, body=form.body.data, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Тема успешно создана.')
            return redirect(url_for('index'))
        else:
            flash('Нужно заполнить и имя и описание темы!')
            return redirect(url_for('index'))
    flash('Error: no login')
    return redirect(url_for('index'))

@app.route('/plus', methods=['GET'])
def plus():
    postid = request.args.get('postid', default = 1, type = int)
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        if user is None:
            flash('Error: not valid user.')
            return redirect(url_for('index'))
        post = Post.query.filter_by(id=postid).first()
        prov = True
        likes = user.likes
        if likes is not None:
            for i in likes.split():
                if i == str(postid):
                    prov = False
            if prov:
                user.likes += ' '+str(postid)
                post.rating = str(int(post.rating)+1)
            else:
                flash('Вы уже оценили этот пост!')
                return redirect('/post?id='+str(postid))
        else:
            user.likes = str(postid)
            post.rating = str(int(post.rating)+1)
        db.session.commit()
        flash('Рейтинга у поста успешно изменен.')
        return redirect('/post?id='+str(postid))
    flash('Error: no login')
    return redirect('/post?id='+str(postid))

@app.route('/minus', methods=['GET'])
def minus():
    postid = request.args.get('postid', default = 1, type = int)
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        if user is None:
            flash('Error: not valid user.')
            return redirect(url_for('index'))
        post = Post.query.filter_by(id=postid).first()
        prov = True
        likes = user.likes
        if likes is not None:
            for i in likes.split():
                if i == str(postid):
                    prov = False
            if prov:
                user.likes += ' '+str(postid)
                post.rating = str(int(post.rating)-1)
            else:
                flash('Вы уже оценили этот пост!')
                return redirect('/post?id='+str(postid))
        else:
            user.likes = str(postid)
            post.rating = str(int(post.rating)-1)
        db.session.commit()
        flash('Рейтинга у поста успешно изменен.')
        return redirect('/post?id='+str(postid))
    flash('Error: no login')
    return redirect('/post?id='+str(postid))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/file', methods=['GET', 'POST'])
def file():
    if current_user.is_authenticated:
        form = CommentForm()
        postid = request.args.get('postid', default = 1, type = int)
        data = re.match(r'\<textarea id=\"body\" name=\"body\" required\>(.*)\<\/textarea\>', str(form.body))
        if form.validate_on_submit() or data is not None:
            arr = []
            for i in Comment.query.order_by(Comment.id):
                arr.append(i)
            filename = arr[len(arr)-1].id+1 if len(arr)-1 >= 0 else 1
            print(filename)
            try:
                file = request.files['image']
            except:
                file=''
                filename = ''
            if file:
                if allowed_file(file.filename):
                    path = os.path.join(UPLOAD_FOLDER, str(filename))
                    file.save(path)
                else:
                    flash('Файл должен быть картинкой!')
                    return redirect('/post?id='+str(postid))
            comment=Comment(body=data.group(1), image=filename, user_id=current_user.id, post_id=postid)
            db.session.add(comment)
            db.session.commit()
            flash('Сообщение успешно добавлено!')
            return redirect('/post?id='+str(postid))
        else:
            flash('Сообщение должно содержать как минимум один символ!')
            return redirect('/post?id='+str(postid))
    flash('Error: no login')
    return redirect('/post?id='+str(postid))