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
                    specialization = request.form["specialization"]
                    position = request.form["position"]
                    education = request.form["education"]
                    experience = request.form["experience"]

                    doctorinput = {
                        "dId": "d" + mId,
                        "username": username,
                        "specialization": specialization,
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
                    return redirect(url_for("api.index"))
                elif identity == "FRONT_DESK":
                    return redirect(url_for("api.index"))
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
    if request.method == "POST":
        dId = Doctors.get_doctors_id(current_user.mId)[0]
        if request.form["recordId"] != "" and request.form["appointmentId"] != "" and request.form["patientId"] != "" and request.form["visit_time"] != "" and request.form["diagnosis"] != "":
            newrecordId = request.form["recordId"]
            newappointmentIde = request.form["appointmentId"]
            newpatientId = request.form["patientId"]
            newvisit_time = request.form["visit_time"]
            newdiagnosis = request.form["diagnosis"]
            addinput = {
                "recordId": newrecordId,
                "appointmentId": newappointmentIde,
                "patientId": newpatientId,
                "visit_time": newvisit_time,
                "diagnosis": newdiagnosis,
                "dId": dId
            }
            MedicalRecords.add_records_doctors(addinput)
            mrRecord = MedicalRecords.get_all_records()
        elif request.form["recorddId"] != "":
            recorddId = request.form["recorddId"]
            dData = MedicalRecords.search_records_id(recorddId)
            if dData is not None:
                print(dData[0])
                MedicalRecords.delete_records(dData[0])
                mrRecord = MedicalRecords.get_all_records()
            else:
                mrRecord = MedicalRecords.get_all_records()
            mrRecord = MedicalRecords.get_all_records()
        else:
            mrRecord = MedicalRecords.get_all_records()
    else:
        if (
            request.values.get("keyword") != ""
            and request.values.get("keyword") is not None
        ):
            search = request.values.get("keyword")
            mrRecord = MedicalRecords.get_records_from_patients_id(search)
        else:
            mrRecord = MedicalRecords.get_all_records()

    returnData = []
    for i in range(len(mrRecord)):
        pData = Patients.get_patients_name_mr(mrRecord[i][2])
        returnData.append(
            {
                "recordId": mrRecord[i][0],
                "appointmentId": mrRecord[i][1],
                "patientsId": mrRecord[i][2],
                "patientName": pData[1],
                "patientBirthday": pData[2].strftime("%Y/%m/%d"),
                "patientMobile": pData[3],
                "patientPhone": pData[4],
                "patientAddress": pData[5],
                "patientHabbit": pData[6],
                "patientCD": pData[7],
                "patientNotes": pData[8],
                "vistTime": mrRecord[i][3].strftime("%Y/%m/%d %H:%M:%S"),
                "diagnosis": str(mrRecord[i][4]),
            }
        )
    return render_template("record.html", user=current_user.name, data=returnData)


@api.route("/personal", methods=["GET", "POST"])
@login_required
def personal():
    if current_user.role == "Doctor":
        dData = Doctors.get_doctor(current_user.mId)
        returnData = [
            {
                "no": dData[0],
                "name": dData[1],
                "specialization": dData[2],
                "position": dData[3],
                "education": dData[4],
                "experience": dData[5]
            }
        ]
        if request.method == "POST":
            updated_data = {
                "name": request.form.get("name"),
                "specialization": request.form.get("specialization"),
                "position": request.form.get("position"),
                "education": request.form.get("education"),
                "experience": request.form.get("experience")
            }
            Doctors.update_doctor(current_user.mId, updated_data)
            dData = Doctors.get_doctor(current_user.mId)
            returnData = [
                {
                    "no": dData[0],
                    "name": dData[1],
                    "specialization": dData[2],
                    "position": dData[3],
                    "education": dData[4],
                    "experience": dData[5]
                }
            ]
    elif current_user.role == "FRONT_DESK":
        dData = Frontdeskpersonel.get_fdp(current_user.mId)
        returnData = [
            {
                "no": dData[0],
                "name": dData[1]
            }
        ]
        if request.method == "POST":
            updated_data = {
                "name": request.form.get("name")
            }
            Frontdeskpersonel.update_fdp(current_user.mId, updated_data)
            dData = Frontdeskpersonel.get_fdp(current_user.mId)
            returnData = [
                {
                    "name": dData[1]
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
    if request.method == "POST":
        if request.form["acupointId"] != "" and request.form["acupointName"] != "":
            newacupointName = request.form["acupointName"]
            newacupointId = request.form["acupointId"]

            addinput = {
                "acupointId": newacupointId,
                "acupointName": newacupointName,
            }
            Acupoints.add_acupoints(addinput)
            acupointData = Acupoints.get_acupoints()
        elif request.form["acupointdId"] != "":
            acupointdId = request.form["acupointdId"]
            dData = Acupoints.search_acupoints_id(acupointdId)
            if dData is not None:
                print(dData[0])
                Acupoints.delete_acupoints(dData[0])
                acupointData = Acupoints.get_acupoints()
            else:
                acupointData = Acupoints.get_acupoints()
            acupointData = Acupoints.get_acupoints()
        else:
            acupointData = Acupoints.get_acupoints()
    else:
        if (
            request.values.get("keyword") != ""
            and request.values.get("keyword") is not None
        ):
            search = request.values.get("keyword")
            acupointData = Acupoints.search_acupoints(search)
        else:
            acupointData = Acupoints.get_acupoints()

    returnData = []
    for i in range(len(acupointData)):
        returnData.append(
            {
                "id": acupointData[i][0],
                "name": acupointData[i][1],
            }
        )
    return render_template("acupoint.html", user=current_user.name, data=returnData)



@api.route("/appointment", methods=["GET", "POST"])
@login_required
def appointment():
    if request.method == "POST":
        if request.form["appointmentId"] != "" and request.form["patientId"] != "" and request.form["appointmentTime"] != "" and request.form["reason"] != "":
            newappointmentId = request.form["appointmentId"]
            newpatientId = request.form["patientId"]
            newappointmentTime = request.form["appointmentTime"]
            newreason = request.form["reason"]
            newfdPersonnelId = request.form["fdPersonnelId"]

            addinput = {
                "appointmentId": newappointmentId,
                "patientId": newpatientId,
                "appointmentTime": newappointmentTime,
                "reason": newreason,
                "fdPersonnelId": newfdPersonnelId
            }
            Appointments.add_appointments(addinput)
            appointmentsData = Appointments.get_appointments()
        elif request.form["appointmentdId"] != "":
            appointmentdId = request.form["appointmentdId"]
            dData = Appointments.search_appointments_id(appointmentdId)
            if dData is not None:
                print(dData[0])
                Appointments.delete_appointments(dData[0])
                appointmentsData = Appointments.get_appointments()
            else:
                appointmentsData = Appointments.get_appointments()
            appointmentsData = Appointments.get_appointments()
        else:
            appointmentsData = Appointments.get_appointments()
    else:
        if (
            request.values.get("keyword") != ""
            and request.values.get("keyword") is not None
        ):
            search = request.values.get("keyword")
            appointmentsData = Appointments.search_appointments(search)
        else:
            appointmentsData = Appointments.get_appointments()

    returnData = []
    for i in range(len(appointmentsData)):
        returnData.append(
            {
                "id": appointmentsData[i][0],
                "patients_name": appointmentsData[i][1],
                "appointment_time": appointmentsData[i][2],
                "reason": appointmentsData[i][3],
                "front_desk_id": appointmentsData[i][4],
            }
        )
    return render_template("appointment.html", user=current_user.name, data=returnData)




analysis = Blueprint("analysis", __name__, template_folder="../templates")


@api.route("/dashboard")
@login_required
def dashboard():
    revenue = []
    dataa = []
    for i in range(1, 13):
        row = Analysis.month_price(i)

        if not row:
            revenue.append(0)
        else:
            for j in row:
                revenue.append(j[1])

        row = Analysis.month_count(i)

        if not row:
            dataa.append(0)
        else:
            for k in row:
                dataa.append(k[1])

    row = Analysis.category_sale()
    datab = []
    for i in row:
        temp = {"value": i[0], "name": i[1]}
        datab.append(temp)

    row = Analysis.member_sale()

    datac = []
    nameList = []
    counter = 0

    for i in row:
        counter = counter + 1
        datac.append(i[0])
    for j in row:
        nameList.append(j[2])

    counter = counter - 1

    row = Analysis.member_sale_count()
    countList = []

    for i in row:
        countList.append(i[0])

    return render_template(
        "dashboard.html",
        counter=counter,
        revenue=revenue,
        dataa=dataa,
        datab=datab,
        datac=datac,
        nameList=nameList,
        countList=countList,
        user=current_user.name,
    )


@api.route("/treatment", methods=["GET", "POST"])
@login_required
def treatment():
    if request.method == "POST":
        if request.form["medicalRecordId"] != "" and request.form["reactionId"] != "" and request.form["acupointId"] != "" and request.form["treatmentDescription"] != "":
            newtmedicalRecordId = request.form["medicalRecordId"]
            newreactionId = request.form["reactionId"]
            newacupointId = request.form["acupointId"]
            newtreatmentDescription = request.form["treatmentDescription"]
            addinput = {
                "medicalRecordId": newtmedicalRecordId,
                "reactionId": newreactionId,
                "acupointId": newacupointId,
                "treatmentDescription": newtreatmentDescription
            }
            Treatment.add_treatment(addinput)
            treatmentData = Treatment.get_treatment()
        elif request.form["medicalRecorddId"] != "" and request.form["reactiondId"] != "" and request.form["acupointdId"] != "":
            medicalRecorddId = request.form["medicalRecorddId"]
            reactiondId = request.form["reactiondId"]
            acupointdId = request.form["acupointdId"]
            delinput = {
                "medicalRecorddId": medicalRecorddId,
                "reactiondId": reactiondId,
                "acupointdId": acupointdId
            }
            dData = Treatment.search_treatments(delinput)
            if dData is not None:
                Treatment.delete_treatment(delinput)
                treatmentData = Treatment.get_treatment()
            else:
                treatmentData = Treatment.get_treatment()
            treatmentData = Treatment.get_treatment()
        else:
            treatmentData = Treatment.get_treatment()
    else:
        if (
            request.values.get("keyword") != ""
            and request.values.get("keyword") is not None
        ):
            search = request.values.get("keyword")
            treatmentData = Treatment.search_treatment(search)
        else:
            treatmentData = Treatment.get_treatment()

    returnData = []
    for i in range(len(treatmentData)):
        returnData.append(
            {
                "medicalRecordId": treatmentData[i][0],
                "reactionId": treatmentData[i][1],
                "acupointId": treatmentData[i][2],
                "treatmentDescription": treatmentData[i][3],
            }
        )
    return render_template("treatment.html", user=current_user.name, data=returnData)
