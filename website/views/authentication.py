from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, UserMixin, current_user
from website.views.database import AuthenticationStore
from decouple import config
from flask_login import LoginManager
from secrets import compare_digest

auth = Blueprint('auth', __name__)


login_manager = LoginManager()


@auth.record_once
def on_load(state):
    login_manager.init_app(state.app)


@login_manager.user_loader
def load_user(username):
    user = User()
    if db.redis.exists(username):
        user.id = username
    return user


db = AuthenticationStore(host=config('HOST'), port=config('PORT'), password=config('PASSWORD'))


class User(UserMixin):
    pass


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password2']
        print(username, password, password_repeat)
        if not compare_digest(password, password_repeat):
            print("here")
            return
        if db.redis.exists(username):
            print("here1")
            return
        db.create_user(user=username, password=password)
        return redirect(url_for('auth.login'))
    return render_template('login/signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    if request.method == "POST":
        username = request.form['username']
        if not db.redis.exists(username):
            flash("Username does not exist")
            return redirect(url_for('auth.login'))
        if db.validate_hex(user=username, password=request.form.get('password')):
            user = User()
            user.id = username
            login_user(user)
            return redirect(url_for('auth.dashboard'))
        else:
            flash("Password is incorrect")
            return redirect(url_for('auth.login'))
    return render_template('login/login.html'), 200


@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('login/dashboard.html', username=current_user.id), 200


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))