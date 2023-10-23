import oracledb

connection = oracledb.connect(
    user="Group9",
    password="bUXuxiJUS",
    host="140.117.69.60",
    port=1521,
    service_name="ORCLPDB1",
)
cursor = connection.cursor()



# with oracledb.connect(
#     user="Group9",
#     password="bUXuxiJUS",
#     host="140.117.69.60",
#     port=1521,
#     service_name="ORCLPDB1",
# ) as connection:
#     with connection.cursor() as cursor:
# sql = """select sysdate from dual"""
# for r in cursor.execute(sql):
# print(r)


# connection.close()


# import oracledb


# dsn = """(DESCRIPTION=
#              (FAILOVER=on)
#              (ADDRESS_LIST=
#                (ADDRESS=(PROTOCOL=tcp)(HOST=140.117.69.60)(PORT=1521))
#              (CONNECT_DATA=(SERVICE_NAME=ORCLPDB1)))"""

# cs='''(description = (retry_count=20)(retry_delay=3)(address=(protocol=tcp)
#      (port=1521)(host=140.117.69.60))
#      (connect_data=(service_name=ORCLPDB1))
#      (security=(ssl_server_dn_match=no)))'''

# cs='''(description = (retry_count=20)(retry_delay=3)(address=(protocol=tcp)
#      (port=1521)(host=140.117.69.60))
#      (connect_data=(service_name=ORCLPDB1)))'''

# connection = oracledb.connect(user="Group9", password="bUXuxiJUS", dsn=cs)

# connection = oracledb.connect(
#     user="Group9", password="bUXuxiJUS", dsn="140.117.69.60/ORCLPDB1"
# )


# cp = oracledb.ConnectParams(host="140.117.69.60", port="1521", service_name="ORCLPDB1")
# dsn = cp.get_connect_string()
# connection = oracledb.connect(user="Group9", password="bUXuxiJUS", dsn=dsn)

# cursor = connection.cursor()
# sql = """select sysdate from dual"""
# for r in cursor.execute(sql):
#     print(r)
