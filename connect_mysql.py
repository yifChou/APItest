import pymysql
import random
def connect_sql(database_name):
    try:
        conn = pymysql.connect(
            host = "10.168.95.60",
            port = 3306,
            user="root",
            password="a135246A",
            database=database_name,
            charset="utf8")
        print(conn)
        cursor = conn.cursor()
        return cursor,conn
    except Exception as e:
        print(e)
def connect_it_100(database_name):
    try:
        conn = pymysql.connect(
            host = "IT-100",
            port = 3308,
            user="mysql",
            password="a135246A",
            database=database_name,
            charset="utf8")
        print(conn)
        cursor = conn.cursor()
        return cursor,conn
    except Exception as e:
        print(e)
def connect_fms_now(database_name):
    try:
        conn = pymysql.connect(
            host = "192.168.88.195",
            port = 3306,
            user="admin",
            password="91ScbOPLzHlYm7b",
            database=database_name,
            charset="utf8")
        print(conn)
        cursor = conn.cursor()
        return cursor,conn
    except Exception as e:
        print(e)
def connect_fms_now1(database_name):
    try:
        conn = pymysql.connect(
            host = "192.168.88.195",
            port = 3306,
            user="fms_user",
            password="zEsZoJvcXJOC3MZ3tvw7",
            database=database_name,
            charset="utf8")
        print(conn)
        cursor = conn.cursor()
        return cursor,conn
    except Exception as e:
        print(e)
# sql = "select pm_id from bil_payment where  pm_id <5000"
#
# sum = cursor.execute(sql)
# result = cursor.fetchall()
# print(type(result))
# cursor.close()
# conn.close()
#db,conn = connect_sql(database_name="tms")
fms_db,fms_conn = connect_fms_now(database_name="fms_db_now")
def excute_sql(db,conn,sql):
    try:
        print("执行前：",sql)
        success = db.execute(sql)
        conn.commit()
        print(sql,"\n","成功",success,"条")
        return 1
    except Exception as e:
        conn.rollback()
        print(e)
        return e
if __name__ =="__main__":
    fms_bsid = "INSERT INTO `bsn_receivablebusiness` (`BsId`, `ShipperCode`, `ReferCode`, `ServerCode`, `ProductCode`, `CountryCode`, `ShipperChargeWeight`, `ShipperOgId`, `ArrivalDate`, `Saller`, `CustomerId`, `ServerChannelCode`, `TransferstatusType`, `PostCode`, `ServerChargeWeight`, `IsHold`, `IsResetCharge`, `CheckOutOn`, `SourceSystem`, `SourceId`, `OperationStatus`, `SyncId`, `ReturnRemark`, `ReturnType`, `ReturnDate`, `IsVirtual`, `IssueKindCode`, `ShipperWeight`, `ServerWeight`) " \
               "select id-1+%s, CONCAT('%s',%s+id), CONCAT('refercode',%s+id), '202005121005', '%s', 'AF', '1.500', '25', NOW(), '794', '%s', 'TEST007', 'S', '69988-5566', '1.500', 'Y', 'N', NOW(), %s, '1000', 'O', '220097565', '', 'S', NULL, 'N', '', '00000001.500', '00000001.500' from test_tmp WHERE id BETWEEN 1 AND %s"
    if excute_sql(fms_db, fms_conn, fms_bsid) != 1:
        print("遇到异常!!!")
