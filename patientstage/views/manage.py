from flask import Flask, request, template_rendered, Blueprint
from flask import url_for, redirect, flash
from flask import render_template
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)


manage = Blueprint("patients", __name__, template_folder="../templates")


# 預約時段
@manage.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template("././home.html", user=current_user.name)


@manage.route("/period", methods=["GET", "POST"])
@login_required
def period():
    return render_template("period.html", user=current_user.name)


@manage.route("/record", methods=["GET", "POST"])
@login_required
def record():
    return render_template("record.html", user=current_user.name)
