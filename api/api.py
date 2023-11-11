import imp
from flask import (
    Flask,
    template_rendered,
    render_template,
    Blueprint,
    redirect,
    request,
    url_for,
    flash,
)
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
import json


api = Blueprint("api", __name__, template_folder="./templates")

login_manager = LoginManager(api)
login_manager.login_view = "api.login"
login_manager.login_message = "請先登入"


class User(UserMixin):
    pass


@api.route("/index", methods=["GET", "POST"])
@login_required
def index():
    return render_template("home.html", user=current_user.name)


# @login_manager.user_loader
# def user_loader(userId):
#     user = User()
#     user.id = userId
#     memberData = Member.get_role(userId)
#     patentsData = Patients.get_patients_name(memberData[1])
#     doctorData = Doctors.get_doctor_name(memberData[1])
#     print(patentsData)
#     print(doctorData)
#     try:
#         # IDENTITY,MID
#         user.role = memberData[0]
#         user.mId = memberData[1]
#         user.name = patentsData[0]
#     except:
#         pass
#     return user


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
            if identity == "doctor":
                identity = "Doctor"
            else:
                identity = "FRONT_DESK"
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
                if identity == "Doctor":
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
                    return redirect(url_for("api.period"))
                    # return redirect(url_for("index"))
                elif identity == "FRONT_DESK":
                    return redirect(url_for("api.period"))
                    # return redirect(url_for("index"))
                else:
                    flash("僅供診所人員使用!")
            else:
                flash("*密碼錯誤，請再試一次")
                return redirect(url_for("api.login"))
        return render_template("login.html", loginFlag=current_user.is_authenticated)


@api.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@api.route("/period", methods=["GET", "POST"])
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


@api.route("/record", methods=["GET", "POST"])
@login_required
def record():
    return render_template("record.html", user=current_user.name)


@api.route("/personal", methods=["GET", "POST"])
@login_required
def personal():
    if current_user.role == "Doctor":
        dData = Doctors.get_doctor(current_user.mId)
        returnData = [
            {
                "name": dData[1],
                "speicalization": dData[2],
                "positions": dData[3],
                "education": dData[4],
                "experience": dData[5],
            }
        ]

    else:
        returnData = [
            {
                "name": current_user.name,
            }
        ]
    return render_template("personal.html", user=current_user.name, data=returnData)


@api.route("/acupoint", methods=["GET", "POST"])
@login_required
def acupoint():
    return render_template("acupoint.html", user=current_user.name)
