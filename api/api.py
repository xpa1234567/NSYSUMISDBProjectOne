import imp
from flask import render_template, Blueprint, redirect, request, url_for, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from link import *
from api.sql import *

api = Blueprint("api", __name__, template_folder="./templates")

login_manager = LoginManager(api)
login_manager.login_view = "api.login"
login_manager.login_message = "請先登入"


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(userid):
    user = User()
    user.id = userid
    data = Member.get_role(userid)
    try:
        user.role = data[0]
        user.name = data[1]
    except:
        pass
    return user


@api.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return render_template("index.html", loginFlag=current_user.is_authenticated)
    else:
        if request.method == "POST":
            account = request.form["account"]
            password = request.form["password"]

            data = Member.get_member(account)

            try:
                # MID, IDENTIFICATION_NUMBER, PASSWORD, IDENTITY
                userId = data[0][0]
                dbPassword = data[0][2]
                identity = data[0][3]

            except:
                flash("*沒有此帳號")
                return redirect(url_for("api.login"))

            if dbPassword == password:
                user = User()
                user.id = userId
                login_user(user)
                if identity == "Doctor":
                    return redirect(url_for("patients.home"))
                elif identity == "FRONT_DESK":
                    return redirect(url_for("patients.home"))
            else:
                flash("*密碼錯誤，請再試一次")
                return redirect(url_for("api.login"))
        return render_template("login.html", loginFlag=current_user.is_authenticated)


@api.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        identity = request.form["identity"]
        username = request.form["username"]
        account = request.form["account"]
        password = request.form["password"]

        # Checl Duplicates Accounts
        exist_account = Member.get_all_account()
        account_list = []
        for i in exist_account:
            account_list.append(i[0])

        if account in account_list:
            flash("Falied!")
            return redirect(url_for("api.register"))
        else:
            memberInput = {
                "account": account,
                "password": password,
                "identity": identity,
            }

            Member.create_member(memberInput)
            memberData = Member.get_member(account)

            try:
                # MID, IDENTIFICATION_NUMBER, PASSWORD, IDENTITY
                mId = memberData[0][0]
                if identity == "doctor":
                    speicalization = request.form["speicalization"]
                    position = request.form["position"]
                    education = request.form["education"]
                    experience = request.form["experience"]

                    doctorinput = {
                        "dId": "d" + mId,
                        "username": username,
                        "speicalization": speicalization,
                        "position": position,
                        "education": education,
                        "experience": experience,
                        "mId": mId,
                    }
                    Doctors.create_doc_member(doctorinput)
                    flash("Successed!")
                    return render_template("register.html")
                else:
                    fdpInput = {"pId": "fp" + mId, "username": username, "mId": mId}
                    Frontdeskpersonel.create_front_member(fdpInput)
                    flash("Successed!")
                    return render_template("register.html")
            except:
                flash("Failed!")
                return redirect(url_for("api.register"))
    return render_template("register.html")


@api.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
