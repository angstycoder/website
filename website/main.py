from flask import render_template, Flask, redirect, url_for, flash
from .views import authentication
from os import urandom


app = Flask(__name__)


app.register_blueprint(authentication.auth)


app.secret_key = urandom(12)


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(Exception)
def page_not_found(error):
    return render_template('error-pages/404.html', code=error.code,
                           name=error.name, message=error.description), 404


@app.errorhandler(401)
def page_not_found(error):
    flash("You were logged out")
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.run(debug=False)
