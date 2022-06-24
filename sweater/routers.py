from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from sweater import app, db
from sweater.models import Authorization


@app.route('/')
def hello():
    return render_template("index.html")


@app.route('/home')
@login_required
def inside():
    return render_template("inside.html", name=current_user.login)


@app.route('/authorization', methods=['POST', 'GET'])
def authorizations():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']

        authorization = Authorization.query.filter_by(login=login).first()

        if authorization and check_password_hash(authorization.password, password):
            login_user(authorization)

            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('/')
        else:
            flash('Логин или пароль некорректны')
        return redirect(url_for('authorizations'))
    else:
        flash('Введите логин и пароль!')
        return render_template("authorization.html")


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello'))


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        password2 = request.form['password2']

        if not login or not password or not password2:
            flash('Заполните все поля!')
            return redirect(url_for('signup'))
        elif password != password2:
            flash('Пароли не равны')
            return redirect(url_for('signup'))
        else:
            hash_pwd = generate_password_hash(password)
            new_user = Authorization(login=login, password=hash_pwd)


        try:
            db.session.add(new_user) #Добавил
            db.session.commit() #Закрыл
            login_user(new_user)
            return redirect(url_for('inside'))
        except:
            return "Произошла ошибка!"
    else:
        flash('Введите логин и пароль')
        return render_template("signup.html")


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('authorizations') + '?next=' + request.url)

    return response