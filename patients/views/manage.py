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
from api.sql import *
import json


patients = Blueprint("patients", __name__, template_folder="../templates")

login_manager = LoginManager(patients)
login_manager.login_view = "patients.login"
login_manager.login_message = "請先登入"


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(userId):
    user = User()
    user.id = userId
    memberData = Member.get_role(userId)
    if memberData[0] == "Doctor":
        nameData = Doctors.get_doctor_name(memberData[1])
    elif memberData[0] == "FRONT_DESK":
        nameData = Frontdeskpersonel.get_fdp_name(memberData[1])
    else:
        nameData = Patients.get_patients_name(memberData[1])

    try:
        # IDENTITY,MID
        user.role = memberData[0]
        user.mId = memberData[1]
        user.name = nameData[0]
    except:
        pass
    return user


@patients.route("/", methods=["GET", "POST"])
def home():
    return render_template("indexfp.html", loginFlag=current_user.is_authenticated)


@patients.route("/index", methods=["GET", "POST"])
def index():
    return render_template("homefp.html", user=current_user.name)


@patients.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        patientsName = request.form["patientsName"]
        patientsAccount = request.form["patientsAccount"]
        patientspassword = request.form["patientspassword"]
        patientsBirthday = request.form["patientsBirthday"]
        patientsMobilephone = request.form["patientsMobilephone"]
        patientsPhone = request.form["patientsPhone"]
        patientsAddress = request.form["patientsAddress"]
        patientsHabbit = request.form["patientsHabbit"]
        patientsDisease = request.form["patientsDisease"]
        patientsNote = request.form["patientsNote"]

        identity = "PATIENT"

        # Checl Duplicates Accounts
        exist_account = Member.get_all_account()
        account_list = []
        for i in exist_account:
            account_list.append(i[0])

        if patientsAccount in account_list:
            flash("Falied!")
            return redirect(url_for("patients.register"))
        else:
            memberInput = {
                "account": patientsAccount,
                "password": patientspassword,
                "identity": identity,
            }

            Member.create_member(memberInput)
            memberData = Member.get_member(patientsAccount)

            try:
                # MID, IDENTIFICATION_NUMBER, PASSWORD, IDENTITY
                mId = memberData[0][0]
                format = "yyyy-mm-dd"
                patientsinput = {
                    "pId": "p" + mId,
                    "patientsName": patientsName,
                    "patientsBirthday": patientsBirthday,
                    "format": format,
                    "patientsMobilephone": patientsMobilephone,
                    "patientsPhone": patientsPhone,
                    "patientsAddress": patientsAddress,
                    "patientsHabbit": patientsHabbit,
                    "patientsDisease": patientsDisease,
                    "patientsNote": patientsNote,
                    "mId": mId,
                }
                Patients.create_patients_member(patientsinput)
                flash("Successed!")
                return render_template("registerfp.html")
            except:
                flash("Falied!")
                return redirect(url_for("patients.register"))

    return render_template("registerfp.html")


@patients.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("patients.home"))
    else:
        if request.method == "POST":
            patientsAccount = request.form["patientsAccount"]
            patientspassword = request.form["patientspassword"]

            data = Member.get_member(patientsAccount)

            try:
                # MID, IDENTIFICATION_NUMBER, PASSWORD, IDENTITY
                userId = data[0][0]
                dbPassword = data[0][2]
                identity = data[0][3]

            except:
                flash("*沒有此帳號")
                return redirect(url_for("patients.login"))

            if identity == "PATIENT":
                if dbPassword == patientspassword:
                    user = User()
                    user.id = userId
                    login_user(user)
                    return redirect(url_for("patients.index"))
                else:
                    flash("*密碼錯誤，請再試一次")
                    return redirect(url_for("patients.login"))
            else:
                flash("僅供病人使用!")
        return render_template("loginfp.html", loginFlag=current_user.is_authenticated)


@patients.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("patients.home"))


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
        "periodfp.html",
        user=current_user.name,
        data=data,
    )


@patients.route("/record", methods=["GET", "POST"])
@login_required
def record():
    pData = Patients.get_patient(current_user.mId)

    patientData = [
        {
            "name": pData[1],
            "birthday": pData[2].strftime("%Y/%m/%d"),
            "mobile": pData[3],
            "phone": pData[4],
            "address": pData[5],
            "dal": pData[6],
            "cd": pData[7],
            "note": pData[8],
        }
    ]

    return render_template("recordfp.html", user=current_user.name, data=patientData)
