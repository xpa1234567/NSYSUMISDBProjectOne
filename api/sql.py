from typing import Optional
from link import *


class DB:
    def connect():
        cursor = connection.cursor()
        return cursor

    def prepare(sql):
        cursor = DB.connect()
        cursor.prepare(sql)
        return cursor

    def execute(cursor, sql):
        cursor.execute(sql)
        return cursor

    def execute_input(cursor, input):
        cursor.execute(None, input)
        return cursor

    def fetchall(cursor):
        return cursor.fetchall()

    def fetchone(cursor):
        return cursor.fetchone()

    def commit():
        connection.commit()


class Frontdeskpersonel:
    def create_front_member(input):
        sql = "INSERT INTO FRONT_DESK_PERSONNEL (PERSONNEL_ID, NAME, MEMBER_ID) VALUES (:pId, :username , :mId)"
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def get_fdp_name(mId):
        sql = "SELECT NAME FROM FRONT_DESK_PERSONNEL WHERE MEMBER_ID = :id "
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": mId}))

    def get_fdp(mId):
        sql = "SELECT * FROM FRONT_DESK_PERSONNEL WHERE MEMBER_ID = :id "
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": mId}))

    def update_fdp(mId, data):
        sql = """
        UPDATE FRONT_DESK_PERSONNEL
        SET NAME = :name
        WHERE MEMBER_ID = :mId
        """
        params = {
            "name": data["name"],
            "mId": mId
        }
        DB.execute_input(DB.prepare(sql), params)
        DB.commit()


class Doctors:
    def get_doctor(mId):
        sql = "SELECT * FROM DOCTORS WHERE MEMBER_ID = :id "
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": mId}))

    def get_doctors_id(mId):
        sql = "SELECT DOCTOR_ID FROM DOCTORS WHERE MEMBER_ID = :id "
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": mId}))

    def create_doc_member(input):
        sql = "INSERT INTO DOCTORS (DOCTOR_ID, NAME, SPECIALIZATION, POSITION, EDUCATION, EXPERIENCE, MEMBER_ID) VALUES (:dId, :username, :specialization, :position, :education, :experience, :mId)"
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def get_doctor_name(mId):
        sql = "SELECT NAME FROM DOCTORS WHERE MEMBER_ID = :id "
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": mId}))

    def update_doctor(mId, data):
        sql = """
        UPDATE DOCTORS
        SET NAME = :name, SPECIALIZATION = :specialization, POSITION = :position, EDUCATION = :education, EXPERIENCE = :experience
        WHERE MEMBER_ID = :mId
        """
        params = {
            "name": data["name"],
            "specialization": data["specialization"],
            "position": data["position"],
            "education": data["education"],
            "experience": data["experience"],
            "mId": mId
        }
        DB.execute_input(DB.prepare(sql), params)
        DB.commit()


class Patients:
    def get_patient(mId):
        sql = "SELECT * FROM PATIENTS WHERE MEMBER_ID = :id "
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": mId}))

    def create_patients_member(input):
        sql = "INSERT INTO PATIENTS (PATIENT_ID, NAME, BIRTHDAY, MOBILE, PHONE, ADDRESS, DIET_AND_LIFESTYLE, CONGENITAL_DISEASE, NOTES, MEMBER_ID) VALUES (:pId, :patientsName, TO_DATE(:patientsBirthday, :format), :patientsMobilephone, :patientsPhone, :patientsAddress, :patientsHabbit, :patientsDisease, :patientsNote, :mId)"
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def get_patients_id(mId):
        sql = "SELECT PATIENT_ID FROM PATIENTS WHERE MEMBER_ID = :id "
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": mId}))

    def get_patients_name(mId):
        sql = "SELECT NAME FROM PATIENTS WHERE MEMBER_ID = :id "
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": mId}))

    def get_patients_name_mr(pId):
        sql = "SELECT * FROM PATIENTS WHERE PATIENT_ID = :id "
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": pId}))

    def update_patients(mId, data):
        sql = """
        UPDATE PATIENTS
        SET NAME = :name, BIRTHDAY = TO_DATE(:birthday, 'YYYY/MM/DD'), MOBILE = :mobile, PHONE = :phone, ADDRESS = :address, DIET_AND_LIFESTYLE = :dal, CONGENITAL_DISEASE = :cd, NOTES = :notes
        WHERE MEMBER_ID = :mId
        """
        params = {
            "name": data["name"],
            "birthday": data["birthday"],
            "mobile": data["mobile"],
            "phone": data["phone"],
            "address": data["address"],
            "dal": data["dal"],
            "cd": data["cd"],
            "notes": data["notes"],
            "mId": mId
        }
        DB.execute_input(DB.prepare(sql), params)
        DB.commit()


class Member:
    def get_role(userid):
        sql = "SELECT IDENTITY, MID FROM MEMBER WHERE MID = :id "
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": userid}))

    def get_member(account):
        sql = "SELECT MID, IDENTIFICATION_NUMBER, PASSWORD, IDENTITY FROM MEMBER WHERE IDENTIFICATION_NUMBER = :IDENTIFICATION_NUMBER"
        return DB.fetchall(
            DB.execute_input(DB.prepare(sql), {"IDENTIFICATION_NUMBER": account})
        )

    def get_all_account():
        sql = "SELECT IDENTIFICATION_NUMBER FROM MEMBER"
        return DB.fetchall(DB.execute(DB.connect(), sql))

    def create_member(input):
        sql = "INSERT INTO MEMBER (IDENTIFICATION_NUMBER, PASSWORD, IDENTITY) VALUES (:account, :password , :identity)"
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    # def delete_product(tno, pid):
    #     sql = "DELETE FROM RECORD WHERE TNO=:tno and PID=:pid "
    #     DB.execute_input(DB.prepare(sql), {"tno": tno, "pid": pid})
    #     DB.commit()

    # def get_order(userid):
    #     sql = "SELECT * FROM ORDER_LIST WHERE MID = :id ORDER BY APPOINTMENT_TIME DESC"
    #     return DB.fetchall(DB.execute_input(DB.prepare(sql), {"id": userid}))


class Acupoints:
    def get_acupoints():
        sql = "SELECT * FROM ACUPOINTS"
        return DB.fetchall(DB.execute(DB.connect(), sql))

    def search_acupoints(keyword):
        sql = "SELECT * FROM ACUPOINTS WHERE ACUPOINT_NAME LIKE :keyword"
        return DB.fetchall(
            DB.execute_input(DB.prepare(sql), {'keyword': '%' + keyword + '%'})
        )

    def search_acupoints_id(id):
        sql = "SELECT ACUPOINT_ID FROM ACUPOINTS WHERE ACUPOINT_ID = :id "
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": id}))

    def add_acupoints(input):
        sql = "INSERT INTO ACUPOINTS (ACUPOINT_ID, ACUPOINT_NAME) VALUES (:acupointId, :acupointName)"
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def delete_acupoints(id):
        sql = "DELETE FROM ACUPOINTS WHERE ACUPOINT_ID=:id "
        DB.execute_input(DB.prepare(sql), {"id": id})
        DB.commit()


class MedicalRecords:
    def get_all_records():
        sql = "SELECT * FROM MEDICAL_RECORDS"
        return DB.fetchall(DB.execute(DB.connect(), sql))

    def add_records_doctors(input):
        sql = "INSERT INTO MEDICAL_RECORDS (RECORD_ID, APPOINTMENT_ID, PATIENT_ID, VISIT_TIME, DIAGNOSIS, DOCTOR_ID) VALUES (:recordId, :appointmentId, :patientId, TO_DATE(:visit_time, 'YYYY-MM-DD HH24:MI:SS'), :diagnosis, :dId)"
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def search_records_id(id):
        sql = "SELECT RECORD_ID FROM MEDICAL_RECORDS WHERE RECORD_ID = :id"
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": id}))
        DB.commit()

    def search_records_patients(id):
        sql = "SELECT RECORD_ID FROM MEDICAL_RECORDS WHERE RECORD_ID = :id"
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": id}))

    def get_records_from_patients_id(pId):
        sql = "SELECT * FROM MEDICAL_RECORDS WHERE PATIENT_ID = :id ORDER BY RECORD_ID"
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {"id": pId}))


    def delete_records(id):
        sql = "DELETE FROM MEDICAL_RECORDS WHERE RECORD_ID=:id "
        DB.execute_input(DB.prepare(sql), {"id": id})
        DB.commit()


class Appointments:
    def get_appointments():
        sql = "SELECT * FROM APPOINTMENTS ORDER BY APPOINTMENT_ID"
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_max_appointments_id():
        sql = "SELECT MAX(APPOINTMENT_ID) FROM APPOINTMENTS"
        return DB.fetchone(DB.execute(DB.connect(), sql))

    def get_appointments_from_patients_id(pId):
        sql = "SELECT * FROM APPOINTMENTS WHERE PATIENT_ID = :id ORDER BY APPOINTMENT_ID"
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {"id": pId}))

    def search_appointments(keyword):
        sql = "SELECT * FROM APPOINTMENTS WHERE PATIENT_ID LIKE :keyword ORDER BY APPOINTMENT_ID"
        return DB.fetchall(
            DB.execute_input(DB.prepare(sql), {'keyword': '%' + keyword + '%'})
        )

    def search_appointments_id(id):
        sql = "SELECT APPOINTMENT_ID FROM APPOINTMENTS WHERE APPOINTMENT_ID = :id"
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": id}))

    def add_appointments(input):
        sql = "INSERT INTO APPOINTMENTS (APPOINTMENT_ID, PATIENT_ID, APPOINTMENT_TIME, REASON, FD_PERSONNEL_ID) VALUES (:appointmentId, :patientId, TO_DATE(:appointmentTime, 'YYYY-MM-DD HH24:MI:SS'), :reason, :fdPersonnelId)"
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def add_appointments_patients(input):
        sql = "INSERT INTO APPOINTMENTS (APPOINTMENT_ID, PATIENT_ID, APPOINTMENT_TIME, REASON) VALUES (:appointmentId, :patientId, TO_DATE(:appointmentTime, 'YYYY-MM-DD HH24:MI:SS'), :reason)"
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def delete_appointments(id):
        sql = "DELETE FROM APPOINTMENTS WHERE APPOINTMENT_ID=:id "
        DB.execute_input(DB.prepare(sql), {"id": id})
        DB.commit()


class Analysis:
    def month_price(i):
        sql = "SELECT EXTRACT(MONTH FROM APPOINTMENT_TIME), COUNT(APPOINTMENT_ID) FROM APPOINTMENTS WHERE EXTRACT(MONTH FROM APPOINTMENT_TIME)=:mon GROUP BY EXTRACT(MONTH FROM APPOINTMENT_TIME)"
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {"mon": i}))

    def month_count(i):
        sql = "SELECT EXTRACT(MONTH FROM APPOINTMENT_TIME), COUNT(APPOINTMENT_ID) FROM APPOINTMENTS WHERE EXTRACT(MONTH FROM APPOINTMENT_TIME)=:mon GROUP BY EXTRACT(MONTH FROM APPOINTMENT_TIME)"
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {"mon": i}))

    def category_sale():
        sql = "SELECT COUNT(*), ACUPOINT_NAME FROM(SELECT * FROM TREATMENT,ACUPOINTS WHERE TREATMENT.ACUPOINT_ID = ACUPOINTS.ACUPOINT_ID) GROUP BY ACUPOINT_NAME"
        return DB.fetchall(DB.execute(DB.connect(), sql))

    def member_sale():
        sql = "SELECT COUNT(*), MEDICAL_RECORDS.DOCTOR_ID, DOCTORS.NAME FROM TREATMENT, MEDICAL_RECORDS, DOCTORS WHERE TREATMENT.MEDICAL_RECORD_ID = MEDICAL_RECORDS.RECORD_ID AND MEDICAL_RECORDS.DOCTOR_ID = DOCTORS.DOCTOR_ID GROUP BY MEDICAL_RECORDS.DOCTOR_ID, DOCTORS.NAME ORDER BY COUNT(*) DESC"
        return DB.fetchall(DB.execute(DB.connect(), sql))

    def member_sale_count(): # doctor_medical_count
        sql = "SELECT COUNT(*), MEDICAL_RECORDS.DOCTOR_ID FROM MEDICAL_RECORDS GROUP BY MEDICAL_RECORDS.DOCTOR_ID ORDER BY COUNT(*) DESC"
        return DB.fetchall(DB.execute(DB.connect(), sql))


class Treatment:
    def get_treatment():
        sql = "SELECT * FROM TREATMENT ORDER BY MEDICAL_RECORD_ID, REACTION_ID"
        return DB.fetchall(DB.execute(DB.connect(), sql))

    def search_treatment(keyword):
        sql = "SELECT * FROM TREATMENT WHERE MEDICAL_RECORD_ID LIKE :keyword"
        return DB.fetchall(
            DB.execute_input(DB.prepare(sql), {'keyword': '%' + keyword + '%'})
        )

    def search_treatment_id(id):
        sql = "SELECT MEDICAL_RECORD_ID FROM TREATMENT WHERE MEDICAL_RECORD_ID = :id "
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": id}))

    def search_treatments(input):
        sql = "SELECT MEDICAL_RECORD_ID FROM TREATMENT WHERE MEDICAL_RECORD_ID = :medicalRecorddId AND REACTION_ID = :reactiondId AND ACUPOINT_ID = :acupointdId"
        return DB.fetchone(DB.execute_input(DB.prepare(sql), input))

    def add_treatment(input):
        sql = "INSERT INTO TREATMENT (MEDICAL_RECORD_ID, REACTION_ID, ACUPOINT_ID, TREATMENT_DESCRIPTION) VALUES (:medicalRecordId, :reactionId, :acupointId, :treatmentDescription)"
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def delete_treatment(input):
        sql = "DELETE FROM TREATMENT WHERE MEDICAL_RECORD_ID = :medicalRecorddId AND REACTION_ID = :reactiondId AND ACUPOINT_ID = :acupointdId"
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()



# class Cart:
#     def check(user_id):
#         sql = (
#             "SELECT * FROM CART, RECORD WHERE CART.MID = :id AND CART.TNO = RECORD.TNO"
#         )
#         return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": user_id}))

#     def get_cart(user_id):
#         sql = "SELECT * FROM CART WHERE MID = :id"
#         return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": user_id}))

#     def add_cart(user_id, time):
#         sql = "INSERT INTO CART VALUES (:id, :time, cart_tno_seq.nextval)"
#         DB.execute_input(DB.prepare(sql), {"id": user_id, "time": time})
#         DB.commit()

#     def clear_cart(user_id):
#         sql = "DELETE FROM CART WHERE MID = :id "
#         DB.execute_input(DB.prepare(sql), {"id": user_id})
#         DB.commit()


# class Product:
#     def count():
#         sql = "SELECT COUNT(*) FROM PRODUCT"
#         return DB.fetchone(DB.execute(DB.connect(), sql))

#     def get_product(pid):
#         sql = "SELECT * FROM PRODUCT WHERE PID = :id"
#         return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": pid}))

#     def get_all_product():
#         sql = "SELECT * FROM PRODUCT"
#         return DB.fetchall(DB.execute(DB.connect(), sql))

#     def get_name(pid):
#         sql = "SELECT PNAME FROM PRODUCT WHERE PID = :id"
#         return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": pid}))[0]

#     def add_product(input):
#         sql = (
#             "INSERT INTO PRODUCT VALUES (:pid, :name, :price, :category, :description)"
#         )

#         DB.execute_input(DB.prepare(sql), input)
#         DB.commit()

#     def delete_product(pid):
#         sql = "DELETE FROM PRODUCT WHERE PID = :id "
#         DB.execute_input(DB.prepare(sql), {"id": pid})
#         DB.commit()

#     def update_product(input):
#         sql = "UPDATE PRODUCT SET PNAME=:name, PRICE=:price, CATEGORY=:category, PDESC=:description WHERE PID=:pid"
#         DB.execute_input(DB.prepare(sql), input)
#         DB.commit()


# class Record:
#     def get_total_money(tno):
#         sql = "SELECT SUM(TOTAL) FROM RECORD WHERE TNO=:tno"
#         return DB.fetchone(DB.execute_input(DB.prepare(sql), {"tno": tno}))[0]

#     def check_product(pid, tno):
#         sql = "SELECT * FROM RECORD WHERE PID = :id and TNO = :tno"
#         return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": pid, "tno": tno}))

#     def get_price(pid):
#         sql = "SELECT PRICE FROM PRODUCT WHERE PID = :id"
#         return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": pid}))[0]

#     def add_product(input):
#         sql = "INSERT INTO RECORD VALUES (:id, :tno, 1, :price, :total)"
#         DB.execute_input(DB.prepare(sql), input)
#         DB.commit()

#     def get_record(tno):
#         sql = "SELECT * FROM RECORD WHERE TNO = :id"
#         return DB.fetchall(DB.execute_input(DB.prepare(sql), {"id": tno}))

#     def get_amount(tno, pid):
#         sql = "SELECT AMOUNT FROM RECORD WHERE TNO = :id and PID=:pid"
#         return DB.fetchone(DB.execute_input(DB.prepare(sql), {"id": tno, "pid": pid}))[
#             0
#         ]

#     def update_product(input):
#         sql = (
#             "UPDATE RECORD SET AMOUNT=:amount, TOTAL=:total WHERE PID=:pid and TNO=:tno"
#         )
#         DB.execute_input(DB.prepare(sql), input)

#     def delete_check(pid):
#         sql = "SELECT * FROM RECORD WHERE PID=:pid"
#         return DB.fetchone(DB.execute_input(DB.prepare(sql), {"pid": pid}))

#     def get_total(tno):
#         sql = "SELECT SUM(TOTAL) FROM RECORD WHERE TNO = :id"
#         return DB.fetchall(DB.execute_input(DB.prepare(sql), {"id": tno}))[0]


# class Order_List:
#     def add_order(input):
#         sql = "INSERT INTO ORDER_LIST VALUES (null, :mid, TO_DATE(:time, :format ), :total, :tno)"
#         DB.execute_input(DB.prepare(sql), input)
#         DB.commit()

#     def get_order():
#         sql = "SELECT OID, NAME, PRICE, APPOINTMENT_TIME FROM ORDER_LIST NATURAL JOIN MEMBER ORDER BY APPOINTMENT_TIME DESC"
#         return DB.fetchall(DB.execute(DB.connect(), sql))

#     def get_orderdetail():
#         sql = "SELECT O.OID, P.PNAME, R.SALEPRICE, R.AMOUNT FROM ORDER_LIST O, RECORD R, PRODUCT P WHERE O.TNO = R.TNO AND R.PID = P.PID"
#         return DB.fetchall(DB.execute(DB.connect(), sql))


# class Analysis:
#     def month_price(i):
#         sql = "SELECT EXTRACT(MONTH FROM APPOINTMENT_TIME), SUM(PRICE) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM APPOINTMENT_TIME)=:mon GROUP BY EXTRACT(MONTH FROM APPOINTMENT_TIME)"
#         return DB.fetchall(DB.execute_input(DB.prepare(sql), {"mon": i}))

#     def month_count(i):
#         sql = "SELECT EXTRACT(MONTH FROM APPOINTMENT_TIME), COUNT(OID) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM APPOINTMENT_TIME)=:mon GROUP BY EXTRACT(MONTH FROM APPOINTMENT_TIME)"
#         return DB.fetchall(DB.execute_input(DB.prepare(sql), {"mon": i}))

#     def category_sale():
#         sql = "SELECT SUM(TOTAL), CATEGORY FROM(SELECT * FROM PRODUCT,RECORD WHERE PRODUCT.PID = RECORD.PID) GROUP BY CATEGORY"
#         return DB.fetchall(DB.execute(DB.connect(), sql))

#     def member_sale():
#         sql = "SELECT SUM(PRICE), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY SUM(PRICE) DESC"
#         return DB.fetchall(DB.execute_input(DB.prepare(sql), {"identity": "user"}))

#     def member_sale_count():
#         sql = "SELECT COUNT(*), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY COUNT(*) DESC"
#         return DB.fetchall(DB.execute_input(DB.prepare(sql), {"identity": "user"}))
