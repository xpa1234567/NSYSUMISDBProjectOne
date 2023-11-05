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
import json

manage = Blueprint("patients", __name__, template_folder="../templates")


# 預約時段
@manage.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template("././home.html", user=current_user.name)


@manage.route("/period", methods=["GET", "POST"])
@login_required
def period():
    # https://joseph-dougal.medium.com/flask-ajax-bootstrap-tables-9036410cbc8
    data = [
        {
            "name": "John Doe",
            "position": "Sales",
            "salary": "$100,000",
            "start_date": "2015",
            "office": "New York",
            "extn": "5421",
        },
        {
            "name": "Larry Doe",
            "position": "Trader",
            "salary": "$100,000",
            "start_date": "2018",
            "office": "Tokyo",
            "extn": "2154",
        },
    ]



    return render_template(
        "period.html",
        user=current_user.name,
        data=data,
    )


@manage.route("/record", methods=["GET", "POST"])
@login_required
def record():
    return render_template("record.html", user=current_user.name)
