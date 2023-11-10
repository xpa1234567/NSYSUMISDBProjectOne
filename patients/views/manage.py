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

patients = Blueprint("patients", __name__, template_folder="../templates")


@patients.route("/", methods=["GET", "POST"])
def home():
    return render_template("indexfp.html")


@patients.route("/register", methods=["POST", "GET"])
def register():
    # if request.method == "POST":
        # user_account = request.form["account"]
        # exist_account = Member.get_all_account()
        # account_list = []
        # for i in exist_account:
        #     account_list.append(i[0])

        # if user_account in account_list:
        #     flash("Falied!")
        #     return redirect(url_for("patients.register"))
        # else:
        #     input = {
        #         "name": request.form["username"],
        #         "account": user_account,
        #         "password": request.form["password"],
        #         "identity": request.form["identity"],
        #     }
        #     Member.create_member(input)
        #     return redirect(url_for("api.login"))

    return render_template("registerfp.html")

@patients.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("patients.home"))
    else:
        if request.method == "POST":
            account = request.form["account"]
            password = request.form["password"]
            data = Member.get_member(account)

            try:
                DB_password = data[0][1]
                user_id = data[0][2]
                identity = data[0][3]

            except:
                flash("*沒有此帳號")
                return redirect(url_for("api.login"))

            if DB_password == password:
                user = User()
                user.id = user_id
                login_user(user)
                return redirect(url_for("patients.home"))
                # if( identity == 'user'):
                #     return redirect(url_for('bookstore.bookstore'))
                # else:
                #     return redirect(url_for('manager.productManager'))

            else:
                flash("*密碼錯誤，請再試一次")
                return redirect(url_for("patients.login"))

        return render_template("loginfp.html")
    

@patients.route("/period", methods=["GET", "POST"])
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


@patients.route("/record", methods=["GET", "POST"])
@login_required
def record():
    return render_template("record.html", user=current_user.name)
