from datetime import timedelta

# Flask modules
import flask
from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, current_user, login_required

# Local modules
from app.extensions import login_manager
from app.forms import LoginForm
from app.models import User

routes = Blueprint('routes', __name__, url_prefix="/")


@login_manager.user_loader
def load_user(user_id):
    return User.find_by_id(user_id)


@routes.route("/")
@login_required
def home():
    return render_template('index.html')


@routes.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes.home"))

    form = LoginForm()

    login = form.login.data
    password = form.password.data
    remember_me = form.remember_me.data

    if flask.request.method == "POST":
        user =  User.find_by_creds(login, password)
        if user is not None:
            flash(f'You successfully sing up!', 'success')
            login_user(user, duration=timedelta.max if remember_me else timedelta(days=1))
            return redirect(flask.request.args.get("next") or url_for("routes.home"))
        else:
            flash(f'Login failed, incorrect login or password','danger')

    return render_template('auth/login.html', form=form)

@routes.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("routes.login"))
