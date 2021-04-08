from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, UserMixin, current_user
from website.views.backend.database import AuthenticationStore
from decouple import config
from flask_login import LoginManager
from secrets import compare_digest
from website.views.bot.botpanel import BotStats

auth = Blueprint('auth', __name__)
stat = BotStats()

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
        if not compare_digest(password, password_repeat):
            return
        if db.redis.exists(username):
            return
        db.create_user(user=username, password=password)
        return redirect(url_for('auth.login'))
    return render_template('login/signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("index.html")
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


@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('login/dashboard.html', username=current_user.id), 200


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@auth.route('/stats')
@login_required
def stats():
    return render_template('bot/bot.html', stats=stat.get_stats())


@auth.route('/usage')
@login_required
def usage():
    return render_template('usage/usage.html')


@auth.route('/webhook', methods=['POST'])
@login_required
def webhook():
    print(request.form)
    message = request.form['message']
    stat.send_webhook(message)
    return '', 204
