from request_fms import *
from connect_mysql import *
from common_util import *
from fee_data_pqm import fee_to_zhuanyun
from config import *
'''发货中转'''
def fahuo_jiesuan_yugu(fahuo_number,org_code,destination,box,waybill_number,charge_weight,customerCode,bill_count,servercode,transfertype,source,iffahuo):
    data_list=[]
    for i in range(fahuo_number):
        data = request_fahuo_fee(org_code,destination,box,waybill_number,charge_weight,customerCode,bill_count,servercode,transfertype,source,iffahuo)
        data_list.append(data)
    return data_list
'''发货中转环节-实际'''
def sql_to_fhzzbill(servercod):
    airbill_code = 'GGDZ' + ymd_ms() + rand1_9()
    airbill_sql = "INSERT INTO `fms_db_now`.`transport_reconcile_bill`(`reconcile_number`, `server_code`, `source`, `start_time`, `end_time`, `body_id`, `bill_status`, `deal_status`, `audit_status`, `allocation_status`, `amount`, `confirm_amount`, `currency`, `car_count`, `differ_count`, `remark`, `create_by`, `create_on`, `update_by`, `update_on`, `audit_by`, `audit_on`, `reconcile_by`, `reconcile_on`, `rule_content`) VALUES " \
                  "('%s', '%s', '1', '%s', NOW(), 5, 'E', 'S', 'E', 'N', 300.00, 300.00, 'RMB ', 1, 1, '发货中转对账', 1, NOW(), 0, NULL, 1, NOW(), 1, NOW(), NULL);"\
                  %(airbill_code,servercod,y_m_d000())
    sql_select_billid = "select reconcile_id from  transport_reconcile_bill  where reconcile_number='%s';" % (airbill_code)
    if excute_sql(fms_db,fms_conn,airbill_sql)==1:
        if excute_sql(fms_db, fms_conn, sql_select_billid) == 1:
            bill_id = fms_db.fetchall()[0][0]
            print(bill_id)
            return bill_id
    else:
        print("遇到异常!!!")
def sql_to_fhzzbill_details(billid,servercod,currency,lading_list):
    for lading_number in lading_list:
        select_sql = "select reconcile_number from transport_reconcile_bill  where reconcile_id='%s';"%(billid)
        if excute_sql(fms_db, fms_conn, select_sql) == 1:
            md5_str = fms_db.fetchall()[0][0]+y_m_d()
            print("md5_str",md5_str)
            hash_code = md5_32_upper(md5_str)
            sql_data = "INSERT INTO `fms_db_now`.`transport_reconcile_bill_detail`(`reconcile_id`, `hash_code`, `car_number`, `delivery_day`,`delivery_time`, `server_code`, `reconcile_status`, `deal_status`, `deal_type`, `allocation_status`, `is_revoke`, `is_refuse`, `amount`, `confirm_amount`, `currency`, `charge_weight`, `charge_unit`, `box`, `org_code`, `destination`, `arrival_time`, `remark`, `refuse_remark`) VALUES " \
                       "( %s, '%s', '%s', '%s',NOW(), '%s', 'F', 'S', 'B', 'N', 'N', 'N', 300.0000, 300.0000, '%s', 3.000, 'kg', 2, 'FX', '数字转运点', '%s', 'test-python', '');" \
                       % (billid, hash_code, lading_number, y_m_d(), servercod, currency, y_m_d000())
            if excute_sql(fms_db, fms_conn, sql_data) != 1:
                print("遇到异常")
                return 0
        else:
            print("遇到异常")
    return lading_list
def sql_to_fhzzbill_fee(billid,servercode,currency,lading_list):
    print("发货中转对账编号增加审核费用-----")
    for lading_number in lading_list:
        select_sql = "select * from transport_reconcile_bill_detail where reconcile_id in(select reconcile_id from transport_reconcile_bill  where car_number='%s' and delivery_day='%s' and reconcile_id=%s)"%(lading_number,y_m_d(),billid)
        if excute_sql(fms_db, fms_conn, select_sql) == 1:
            detail_ids = fms_db.fetchall()
            for detail_id in detail_ids:
                fee_list = ["tp", "B7", "TT"]
                length = len(fee_list)
                for i in range(length):
                    if i == 0 or random.randint(1, length) == 3:
                        sql_data="INSERT INTO `fms_db_now`.`transport_reconcile_fee`( `bill_detail_id`, `server_code`, `fee_code`, `deal_type`, `amount`, `differ`, `currency`, `create_on`) VALUES " \
                                 "(%s, '%s', '%s', 'B', 200.000, 'N', '%s', NOW());"\
                                    %(detail_id[0],servercode,fee_list[i],currency)
                        if excute_sql(fms_db, fms_conn, sql_data) != 1:
                            print("遇到异常")
                            return 0
def sql_to_fhzzbill_fentan_bag(lading_sum,org_code,destination,bag_list,shipper_list,Charge_Weight,fh_servercode,if_pqm,source):
    lading_list=[]
    for i in range(lading_sum):
        lading_number = request_fahuo_withbag_fee(bag_list=bag_list, org_code=org_code, destination=destination, charge_weight=Charge_Weight, shipper_list=shipper_list, servercode=fh_servercode, if_pqm=if_pqm,source=source)
        lading_list.append(lading_number)
    billid = sql_to_fhzzbill(servercod=fh_servercode)
    sql_to_fhzzbill_details(billid=billid, lading_list=lading_list,servercod=fh_servercode,currency=currency)
    sql_to_fhzzbill_fee(billid=billid, lading_list=lading_list,servercode=fh_servercode,currency=currency)
def sql_to_fhzzbill_fentan(lading_sum,org_code,destination,box,waybill_number,charge_weight,customerCode,bill_count,servercode,transfertype,source,iffahuo):
    lading_list=[]
    for i in range(lading_sum):
        lading_number = request_fahuo_fee(org_code,destination,box,waybill_number,charge_weight,customerCode,bill_count,servercode,transfertype,source,iffahuo)
        lading_list.append(lading_number)
    billid = sql_to_fhzzbill(servercod=servercode)
    sql_to_fhzzbill_details(billid=billid, lading_list=lading_list,servercod=servercode,currency=currency)
    sql_to_fhzzbill_fee(billid=billid, lading_list=lading_list,servercode=servercode,currency=currency)
'''调拨环节-预估'''
def diaobo_jiesuan_yugu(diaobo_number,bag_number, waybill_number, customerCode, yt_number, transfertype,transport_type_code,servercode, source):
    data_list=[]
    for i in range(diaobo_number):
        data = request_diaobo_fee(bag_number, waybill_number+i, customerCode, yt_number, transfertype,transport_type_code,servercode, source)
        data_list.append(data)
    return data_list
'''调拨环节-实际'''
def sql_to_diaobobill(servercod):
    airbill_code = 'DBDZ' + ymd_ms() + rand1_9()
    airbill_sql = "INSERT INTO `fms_db_now`.`transfer_reconcile`(`check_status`, `deal_status`, `push_status`, `allocation_status`, `audit_status`, `service_code`, `transport_type`, `og_body_code`, `bill_code`, `bill_amount`, `sure_amount`, `currency`, `bill_count`, `pending_count`, `compar_start`, `compar_end`, `source`, `remark`, `createdby`, `createdon`, `updateby`, `updateon`, `audit_by`, `audit_on`, `reconcile_by`, `reconcile_on`, `last_update_time`) VALUES " \
                  "('E', 'S', 'N', 'N', 'E', '%s', 'WL', '1', '%s', 140.00, 140.00, 'HKD', 1, 0, '%s', NOW(), '1', 'kaid1', 1, NOW(), 966, NOW(), 966, NOW(), 1, NOW(),NOW());"\
                  %(servercod,airbill_code,y_m_d000())
    sql_select_billid = "select reconcile_id from  transfer_reconcile  where bill_code='%s';" % (airbill_code)
    if excute_sql(fms_db,fms_conn,airbill_sql)==1:
        if excute_sql(fms_db, fms_conn, sql_select_billid) == 1:
            bill_id = fms_db.fetchall()[0][0]
            print(bill_id)
            return bill_id
    else:
        print("遇到异常!!!")
def sql_to_diaobobill_details(billid,servercod,currency,lading_list):
    for lading_number in lading_list:
        sql_data = "INSERT INTO `fms_db_now`.`transfer_reconcile_detail`(`reconcile_id`, `check_status`, `deal_status`, `allocation_status`, `process_type`, `is_revoke`, `is_back`, `service_code`, `transport_number`, `processed_amount`, `total_amount`, `car_type`, `currency`, `weight`, `confirm_weight`, `weight_unit`, `box_count`, `createdby`, `createdon`, `back_remark`, `remark`, `start_transit`, `end_transit`, `departure_time`, `arrival_time`, `reconcile_by`, `reconcile_on`, `update_by`, `last_update_time`) VALUES " \
                   "( %s, 'R', 'S', 'N', 'S', 'N', 'N', '%s', '%s', 140.00, 140.00, '', '%s', 123.000, 0.000, 'KG', 100, 1, NOW(), '', '', 'YT-GZ', 'YT-XM', NOW(), NOW(), 1, NOW(), 966, NOW());"\
                   %(billid,servercod,lading_number,currency)
        if excute_sql(fms_db, fms_conn, sql_data) == 1:
            select_detail_id ="select reconcile_detail_id from transfer_reconcile_detail where reconcile_id=%s and transport_number='%s';"%(billid,lading_number)
            if excute_sql(fms_db,fms_conn,select_detail_id)==1:
                detail_id = fms_db.fetchall()[0][0]
                fee_list = ["O3", "O4", "O5", "O6", "O8", "OL"]
                length = len(fee_list)
                for i in range(length):
                    if i == 0 or random.randint(1, length) == 3:
                        differ_sql="INSERT INTO `fms_db_now`.`transfer_reconcile_differ_detail`(`reconcile_detail_id`, `differ_type`, `sys_value`, `service_value`, `deal_type`, `deal_value`, `is_differ`, `createon`, `dealon`, `last_update_time`) VALUES " \
                                    "( %s, '%s', 2.00, 100.00, 'S', 100.00, 'Y', NOW(), NOW(),NOW());"%(detail_id,fee_list[i])
                        if excute_sql(fms_db, fms_conn, differ_sql) != 1:
                            print("遇到异常")
                            return 0
    return lading_list
def sql_to_diaobobill_fee(billid,servercode,currency,lading_list):
    print("调拨对账对账编号增加审核费用-----")
    for lading_number in lading_list:
        fee_list = ["A8", "B7", "A4","VA", "E2", "B1","B3", "D4", "H7"]
        length = len(fee_list)
        for i in range(length):
            if i == 0 or random.randint(1, length) == 3:
                sql_data="INSERT INTO `fms_db_now`.`transfer_reconcile_fee`(`reconcile_id`, `fk_code`, `amount`, `currency`, `createdby`, `createon`, `service_code`, `transport_number`, `departure_time`, `last_update_time`) VALUES " \
                         "( %s, '%s', 30.00, '%s', 1, NOW(), '%s', '%s', NOW(), NOW());"\
                            %(billid,fee_list[i],currency,servercode,lading_number)
                if excute_sql(fms_db, fms_conn, sql_data) != 1:
                    print("遇到异常")
                    return 0
def sql_to_diaobobill_fentan_bag(lading_sum,bag_list, shipper_list,if_pqm,transport_type_code,servercode, source,currency):
    lading_list=[]
    for i in range(lading_sum):
        diaobo_number=random.randint(10000,99999)
        lading_number = request_diaobo_withbag_fee(bag_list,shipper_list,diaobo_number,transport_type_code,servercode,if_pqm,source)
        lading_number=lading_number.replace("DH","")
        lading_list.append(lading_number)
    billid = sql_to_diaobobill(servercod=servercode)
    sql_to_diaobobill_details(billid=billid, lading_list=lading_list,servercod=servercode,currency=currency)
    sql_to_diaobobill_fee(billid=billid, lading_list=lading_list,servercode=servercode,currency=currency)
def sql_to_diaobobill_fentan(lading_sum,bag_number, waybill_number, customerCode, yt_number, transfertype,transport_type_code,servercode, source,currency):
    lading_list=[]
    for i in range(lading_sum):
        lading_number = request_diaobo_fee(bag_number, waybill_number+i, customerCode, yt_number, transfertype,transport_type_code,servercode, source)
        lading_number=lading_number.replace("DH","")
        lading_list.append(lading_number)
    billid = sql_to_diaobobill(servercod=servercode)
    sql_to_diaobobill_details(billid=billid, lading_list=lading_list,servercod=servercode,currency=currency)
    sql_to_diaobobill_fee(billid=billid, lading_list=lading_list,servercode=servercode,currency=currency)
'''清关环节'''
#预估结算
def qglading_jiesuan_yugu(ladingnumber, lading_index, bag_number,servercode,qg_servercode, waybill_number, customerCode, Charge_Weight, yt_number, fee_number, transfertype, ifotherfee, source):
    data_list=[]
    for i in range(ladingnumber):
        data = request_customer_fee(lading_index+i, bag_number,servercode,qg_servercode, waybill_number, customerCode, Charge_Weight, yt_number, fee_number, transfertype, ifotherfee, source)
        data_list.append(data)
    return data_list
#实际结算-清关提单对账
def sql_to_qgbill(servercod):
    airbill_code = 'QGTDDZ' + ymd_ms() + rand1_9()
    #YIFQG
    airbill_sql = "INSERT INTO `fms_db_now`.`lading_customs_bill`(`check_status`, `deal_status`, `service_code`, `check_number`, `amount`, `currency`, `rate`, `checkby`, `checkon`, `remark`, `createdby`, `createdon`, `updateby`, `updateon`, `pending_count`, `settingId`, `bill_cycle_start`, `bill_cycle_end`, `service_bodyid`, `confirmed_amount`, `total_count`, `auditby`, `auditon`, `allocation_State`, `audit_status`) VALUES " \
                  "('P', 'E', '%s', '%s', 400.00, 'RMB', 1.0000, 2243, NOW(), '', 1, NOW(), 1, NOW(), 0, 64, '%s', '%s', 2, 400.00, 1, 2243, NOW(), 'N', 'Y');"\
                  %(servercod,airbill_code,y_m_d000(),y_m_d000())
    sql_select_billid = "select lading_billId from  lading_customs_bill  where check_number='%s';" % (airbill_code)
    if excute_sql(fms_db,fms_conn,airbill_sql)==1:
        if excute_sql(fms_db, fms_conn, sql_select_billid) == 1:
            bill_id = fms_db.fetchall()[0][0]
            print(bill_id)
            return bill_id
    else:
        print("遇到异常!!!")
def sql_to_qgbill_cardetails(billid,lading_list):
    for lading_number in lading_list:
        sql_data = "INSERT INTO `fms_db_now`.`lading_customs_billdetails`( `lading_billId`, `check_status`, `deal_status`, `is_revoke`, `lading_number`, `sum_amount`, `currency`, `bill_count`, `box_count`, `weight`, `volume`, `HScode_count`, `airport`, `finishtime`, `remark`, `audit_status`, `verifi_status`, `data_type`, `auditby`, `auditon`, `allocation_State`, `allocation_Id`, `dataSource`, `is_back`, `back_remark`, `chargeable_weight`, `source_id`, `deal_amount`) VALUES " \
                   "(%s, 'N', 'E', 'N', '%s', 13.96, 'RMB', 10, 2, NULL, NULL, NULL, 'AMS', NOW(), '我司为准', 'W', 'N', 'F', NULL, NULL, 'W', NULL, 'B', NULL, NULL, 3.000, 1, 3.96);"\
               %(billid,lading_number)
        if excute_sql(fms_db, fms_conn, sql_data) != 1:
            print("遇到异常")
            return 0
    bill_carid="SELECT billdetailId FROM lading_customs_billdetails where lading_billId=%s"%(billid)
    if excute_sql(fms_db, fms_conn, bill_carid) == 1:
        car_id = fms_db.fetchall()
        car_id_list=[]
        for id in car_id:
            car_id_list.append(id[0])
        return car_id_list
    else:
        return []
def sql_to_qgbill_fee(car_id_list):
    print("清关对账对账编号增加审核费用-----")
    for car_id in car_id_list:
        fee_list = ["D4", "A8", "qg", "J9", "Z5", "S6"]
        length = len(fee_list)
        for i in range(length):
            if i == 0 or random.randint(1, length) == 3:
                sql_data="INSERT INTO `fms_db_now`.`lading_bill_fee`(`billdetailId`, `amount`, `fee_type`, `rate`, `currency`, `auditby`, `auditon`, `fee_source`, `remark`, `is_audit`) VALUES " \
                         "(%s, 2.64, '%s', 1.0000, 'RMB', 1, NOW(), 'S', NULL, 'Y');"\
                        %(car_id,fee_list[i])
                if excute_sql(fms_db, fms_conn, sql_data) != 1:
                    print("遇到异常")
                    return 0
def sql_to_qgbill_fentan_bag(lading_list,bag_list, shipper_list,qg_servercode, customerCode,if_vat,source):
    car_list=[]
    for lading_number in lading_list:
        car_number1 = request_customer_withbag_fee(lading_number=lading_number, bag_list=bag_list, shipper_list=shipper_list, qg_servercode=qg_servercode, customerCode=customerCode, if_vat=if_vat, source=source)
        car_list.append(car_number1)
    billid = sql_to_qgbill(servercod=qg_servercode)
    car_id_list = sql_to_qgbill_cardetails(billid=billid, lading_list=car_list)
    sql_to_qgbill_fee(car_id_list=car_id_list)
def sql_to_qgbill_fentan(lading_number,lading_index, bag_number,servercode,qg_servercode, waybill_number, customerCode, Charge_Weight, yt_number, fee_number, transfertype, ifotherfee, source):
    car_list=[]
    for i in range(lading_number):
        car_number1 = request_customer_fee(lading_index=str(lading_index+i),bag_number=bag_number,
                              waybill_number=waybill_number,customerCode=customerCode,
                              Charge_Weight=Charge_Weight,yt_number=yt_number,
                              fee_number=fee_number,transfertype=transfertype,
                              ifotherfee=ifotherfee,servercode=servercode,source=source,qg_servercode=qg_servercode)
        car_list.append(car_number1)
    billid = sql_to_qgbill(servercod=qg_servercode)
    car_id_list = sql_to_qgbill_cardetails(billid=billid, lading_list=car_list)
    sql_to_qgbill_fee(car_id_list=car_id_list)
#实际结算-清关运单对账
def sql_to_qgydbill(servercod):
    airbill_code = 'QGYDDZ' + ymd_ms() + rand1_9()
    #YIFQG
    airbill_sql = "INSERT INTO `fms_db_now`.`vat_customs_bill`( `check_status`, `deal_status`, `service_code`, `check_number`, `body_id`, `amount`, `currency`, `rate`, `checkby`, `checkon`, `remark`, `start_time`, `end_time`, `createdby`, `createdon`, `updateby`, `updateon`, `bill_count`, `import_count`, `audit_status`, `auditby`, `auditon`, `settingId`, `hawbcode_type`) VALUES " \
                  "('E', 'S', '%s', '%s', 64, 9.00, 'RMB', 1.0000, 1, NOW(), '', '%s', '%s', 1, NOW(), 1, NOW(), 1, 0, 'W', 1, NOW(), 65, 1);"\
                  %(servercod,airbill_code,y_m_d000(),y_m_d000())
    sql_select_billid = "select vat_billId from  vat_customs_bill  where check_number='%s';" % (airbill_code)
    if excute_sql(fms_db,fms_conn,airbill_sql)==1:
        if excute_sql(fms_db, fms_conn, sql_select_billid) == 1:
            bill_id = fms_db.fetchall()[0][0]
            print(bill_id)
            return bill_id
    else:
        print("遇到异常!!!")
def sql_to_qgydbill_details(billid,lading_list):
    for lading_number in lading_list:
        sql_data = "INSERT INTO `fms_db_now`.`vat_customs_billdetails`(`vat_billId`, `settingId`, `check_status`, `deal_status`, `is_revoke`, `hawbcode`, `lading_number`, `amount`, `ship_charge`, `currency`, `remark`, `audit_status`, `verifi_status`, `data_type`, `auditby`, `auditon`, `is_back`, `back_remark`, `hawbcode_type`, `air_port`, `sourcesystem`, `refercode`) VALUES " \
                   "(%s, 65, 'F', 'S', 'N', '%s', NULL, 9.00, 5.32, 'RMB', '', 'W', '1', 'B', 1, NULL, 'N', NULL, 1, '', NULL, NULL);"\
               %(billid,lading_number)
        if excute_sql(fms_db, fms_conn, sql_data) != 1:
            print("遇到异常")
            return 0

def sql_to_qgydbill_fee(billid,car_id_list):
    print("清关对账对账编号增加审核费用-----")
    for car_id in car_id_list:
        fee_list = ["BF", "VA", "P8", "D4"]
        length = len(fee_list)
        for i in range(length):
            if i == 0 or random.randint(1, length) == 3:
                sql_data="INSERT INTO `fms_db_now`.`vat_bill_fee`(`billId`, `hawbcode`, `amount`, `fee_type`, `rate`, `currency`, `auditby`, `auditon`, `fee_source`, `remark`, `is_audit`) VALUES " \
                         "(%s, '%s', 3.00, '%s', NULL, 'RMB', 1, NOW(), 'B', '', 'Y');"\
                        %(billid,car_id,fee_list[i])
                if excute_sql(fms_db, fms_conn, sql_data) != 1:
                    print("遇到异常")
                    return 0
def sql_to_qgydbill_fentan_bag(lading_list,bag_list,shipper_list,qg_servercode, customerCode, source):
    car_list=[]
    for lading_number in lading_list:
        car_number1 = request_customer_withbag_fee(lading_number=lading_number, bag_list=bag_list, shipper_list=shipper_list, qg_servercode=qg_servercode, customerCode=customerCode, if_vat=1, source=source)
        car_list.append(car_number1)
    billid = sql_to_qgydbill(servercod=qg_servercode)
    time.sleep(5)
    print("休眠5s")
    for lading_number in car_list:
        bill_yd = "select shipper_hawbcode from lading_bsn_relate where lading_id IN(select customs_id from customs_info where lading_number='%s') and relate_type='C';" % (
            lading_number)
        if excute_sql(fms_db, fms_conn, bill_yd) == 1:
            yd_code = list(fms_db.fetchall())
            yd_code = [yd[0] for yd in yd_code]
            print(yd_code)
            sql_to_qgydbill_details(billid=billid, lading_list=yd_code)
            sql_to_qgydbill_fee(car_id_list=yd_code, billid=billid)
        else:
            return []
def sql_to_qgydbill_fentan(lading_number,lading_index, bag_number,servercode,qg_servercode, waybill_number, customerCode, Charge_Weight, yt_number, fee_number, transfertype, ifotherfee, source):
    car_list=[]
    for i in range(lading_number):
        car_number1 = request_customer_fee(lading_index=str(lading_index+i),bag_number=bag_number,
                              waybill_number=waybill_number,customerCode=customerCode,
                              Charge_Weight=Charge_Weight,yt_number=yt_number,
                              fee_number=fee_number,transfertype=transfertype,
                              ifotherfee=ifotherfee,servercode=servercode,source=source,qg_servercode=qg_servercode,if_vat=1)
        car_list.append(car_number1)
    billid = sql_to_qgydbill(servercod=qg_servercode)
    time.sleep(5)
    print("休眠5s")
    for lading_number in car_list:
        bill_yd = "select shipper_hawbcode from lading_bsn_relate where lading_id IN(select customs_id from customs_info where lading_number='%s') and relate_type='C';" % (
            lading_number)
        if excute_sql(fms_db, fms_conn, bill_yd) == 1:
            yd_code = list(fms_db.fetchall())
            yd_code = [yd[0] for yd in yd_code]
            print(yd_code)
            sql_to_qgydbill_details(billid=billid, lading_list=yd_code)
            sql_to_qgydbill_fee(car_id_list=yd_code, billid=billid)
        else:
            return []

'''中转环节'''
def sql_to_carbill(servercod):
    airbill_code = 'ZZDZ' + ymd_ms() + rand1_9()
    airbill_sql = "INSERT INTO `fms_db_now`.`xfe_shipperbillinfo`( `Contrast_state`, `State`, `ServerCode`, `Importcode`, `Bill_amount`, `Currency_code`, `Rate`, `Remark`, `Import_by`, `Import_time`, `Createdby`, `Createdon`, `Last_update_by`, `Last_update_on`, `pending_count`, `XrsId`, `auditby`, `auditon`, `compar_starton`, `compar_endedon`, `sure_amount`, `allocation_status`, `data_source`, `service_bodyid`, `service_bodycode`, `reconcile_name`) " \
                  "VALUES ('E', 'E', '%s', '%s', 607.59, 'RMB', 1.0000, '', 1, '%s', 1, '%s', NULL, NULL, 0, NULL, 1, '%s', '%s', '%s', 607.59, 'N', 'Z', 2, NULL, '所有费用项-卡车');"\
                  %(servercod,airbill_code,now(),now(),now(),now(),now())
    sql_select_billid = "select XsId from  xfe_shipperbillinfo  where Importcode='%s';" % (airbill_code)
    if excute_sql(fms_db,fms_conn,airbill_sql)==1:
        if excute_sql(fms_db, fms_conn, sql_select_billid) == 1:
            bill_id = fms_db.fetchall()[0][0]
            print(bill_id)
            return bill_id
    else:
        print("遇到异常!!!")
def sql_to_carbill_cardetails(billid,car_list):
    time.sleep(2)
    for car_number in car_list:
        sql_car_id = "SELECT transit_Id FROM transit_info WHERE car_number='%s';"%(car_number)
        if excute_sql(fms_db, fms_conn, sql_car_id) == 1:
            car_id = fms_db.fetchall()[0][0]
            sql_data = "INSERT INTO `fms_db_now`.`xfe_shipperbillinfo_detail`( `XsId`, `Contrast_state`, `State`, `DataType`, `deal_type`, `deal_amount`, `Is_revoke`, `Carcode`, `Amount`, `Currency_code`, `Rate`, `Plates`, `Boxs`, `charge_weight`, `charge_unit`, `Weight`, `Lumber`, `Start`, `End`, `CarStartTime`, `CarEndTime`, `Remarks`, `Audit_status`, `Verifi_status`, `Auditby`, `Auditon`, `Allocation_State`, `allocation_Id`, `is_back`, `back_remark`, `transit_id`) " \
                   "VALUES (%s, 'W', 'E', 'Z', 'B', 112.53, 'N', '%s', 112.53, 'RMB', 1.0000, NULL, NULL, 3.000, 'KG', 2.000, NULL, 'MD', 'MX', '%s', '%s', '举例', 'W', '1', NULL, NULL, 'N', NULL, NULL, NULL,%s);"\
                   %(billid,car_number,now(),now(),car_id)
            if excute_sql(fms_db, fms_conn, sql_data) != 1:
                print("遇到异常")
                return 0
    bill_carid="SELECT XsdId FROM xfe_shipperbillinfo_detail where XsId=%s"%(billid)
    if excute_sql(fms_db, fms_conn, bill_carid) == 1:
        car_id = fms_db.fetchall()
        car_id_list=[]
        for id in car_id:
            car_id_list.append(id[0])
        return car_id_list
    else:
        return []
def sql_to_carbill_fee(car_id_list):
    print("中转对账对账编号增加审核费用-----")
    for car_id in car_id_list:
        fee_list = ["A8", "TT", "B7","P4", "W4", "tp"]
        length = len(fee_list)
        for i in range(length):
            if i == 0 or random.randint(1, length) == 3:
                sql_data="INSERT INTO `fms_db_now`.`xfe_bill_audit_fee`(`xsd_id`, `amount`, `fk_code`, `currency`, `server_code`, `is_differ`, `createdby`, `createdon`) " \
                         "VALUES (%s, 30.00, '%s', 'RMB', 'yif', 'N', 0, '%s');"\
                        %(car_id,fee_list[i],now())
                if excute_sql(fms_db, fms_conn, sql_data) != 1:
                    print("遇到异常")
                    return 0
def sql_to_carbill_fentan_bag(car_sum,car_number,bag_list,CountryCode,transit_country,customerCode,servercode,source,if_pqm,iffahuo):
    car_list=[]
    for i in range(car_sum):
        car_number1 = request_car_with_bag_fee(data=car_number+i, CountryCode=CountryCode, transit_country=transit_country, bag_list=bag_list, customerCode=customerCode, source=source, if_pqm=if_pqm,servercode=servercode, iffahuo=iffahuo)
        car_list.append(car_number1)
    billid = sql_to_carbill(servercod=servercode)
    car_id_list = sql_to_carbill_cardetails(billid=billid, car_list=car_list)
    sql_to_carbill_fee(car_id_list=car_id_list)
def sql_to_carbill_fentan(car_sum,car_number,CountryCode,transit_country,bag_number,waybill_number,customerCode,yt_number,servercode,transfertype,source,iffahuo):
    car_list=[]
    for i in range(car_sum):
        car_number1 = request_car_fee(car_number+i,CountryCode,transit_country,bag_number,waybill_number,customerCode,yt_number,servercode,transfertype,source,iffahuo)
        car_list.append(car_number1)
    billid = sql_to_carbill(servercod=servercode)
    car_id_list = sql_to_carbill_cardetails(billid=billid, car_list=car_list)
    sql_to_carbill_fee(car_id_list=car_id_list)
'''空运环节'''
def sql_to_airbill(servercod):
    airbill_code = 'KYDZ' + ymd_ms() + rand1_9()
    airbill_sql = "INSERT INTO `fms_db_now`.`air_import_shipperbill_info`(`contrast_state`, `state`, `server_code`, `importcode`, `bill_amount`, `bill_count`, `currency_code`, `remark`, `import_by`, `import_time`, `createdby`, `createdon`, `last_update_by`, `last_update_on`, `bill_startTime`, `bill_endTime`, `og_bodyId`, `allocation_state`, `laborcost_state`, `audit_state`, `auditby`, `auditon`, `laborcost_createdby`, `laborcost_createdtime`, `laborcost_allocationby`, `laborcost_allocationtime`, `data_source`, `sure_amount`)" \
                  " VALUES ('E', 'S', '%s', '%s', 142.56, 1, 'RMB', '', 1, '%s', 1, '%s', 1, '%s', '%s', '%s', 64, 'N', 'N', 'Y', 1, '%s', 1, '%s', NULL, NULL, 'B', 142.56);"\
                  %(servercod,airbill_code,now(),now(),now(),y_m_d000(),y_m_d000(),now(),now())
    sql_select_billid = "select isid from  air_import_shipperbill_info  where importcode='%s';" % (airbill_code)
    if excute_sql(fms_db,fms_conn,airbill_sql)==1:
        if excute_sql(fms_db, fms_conn, sql_select_billid) == 1:
            bill_id = fms_db.fetchall()[0][0]
            print(bill_id)
            return bill_id
    else:
        print("遇到异常!!!")
def sql_to_airbill_ladingdetails(billid,currency,lading_list):
    for lading_number in lading_list:
        sql_data = "INSERT INTO `fms_db_now`.`air_shipperbill_lading_detail`( `isid`, `contrast_state`, `state`, `audit_state`, `eliminate_state`, `allocation_state`, `allocation_Id`, `laborcost_state`, `laborcost_allocation_Id`, `iscancel`, `lading_number`, `amount`, `currency_code`, `process_type`, `remark`, `createdon`, `createdby`, `auditby`, `auditon`, `eliminateby`, `eliminateon`, `last_update_on`, `last_update_by`, `DataSource`, `isback`) " \
                   "VALUES (%s, 'N', 'S', 'Y', 'N', 'N', NULL, 'N', 0, 'N', '%s', 432.49, '%s', 'B', '', '%s', 1, 1, '%s', 0, '%s', '%s', 1, 'B', 'N');"\
                   %(billid,lading_number,currency,now(),now(),now(),now())
        if excute_sql(fms_db, fms_conn, sql_data) != 1:
            print("遇到异常")
            return 0
        sql_data_lading_details="INSERT INTO `lading_detail`(`lading_number`, `lading_weight`, `volume_weight`, `chargeable_weight`, `bsn_chargeWeight`, `lading_volume`, `count_number`, `amount`, `currency`, `bag_count`, `source`, `volume_unit`, `chargeable_unit`, `lading_unit`) " \
                                "VALUES ('%s', 1.188, 3.564, 1.188, 0.000, 0.000, 0, 432.49, 'RMB', 1, 'B', '', '', '');"\
                                %(lading_number)
        if excute_sql(fms_db, fms_conn, sql_data_lading_details) != 1:
            print("遇到异常")
            return 0
    return lading_list
def sql_to_airbill_fee(billid,lading_list):
    print("空运对账对账编号增加审核费用-----")
    for lading_number in lading_list:
        fee_list = ["A4", "G7", "TC","SC", "G6", "G2"]
        length = len(fee_list)
        for i in range(length):
            if i == 0 or random.randint(1, length) == 3:
                sql_data="INSERT INTO `fms_db_now`.`lading_fee`( `lading_number`, `price_number`, `fk_code`, `charg_unit`, `charg_type`, `amount`, `currency`, `rate`, `source`, `deal_type`, `is_audit`, `isid`, `create_on`, `createdby`, `remark`, `server_code`) " \
                            "VALUES ( '%s', 113, '%s', 'W', 'DJ', 4.28, 'RMB', 1.0000, 'B', '', 'Y', %s, '%s', 1, NULL, NULL);"\
                            %(lading_number,fee_list[i],billid,now())
                if excute_sql(fms_db, fms_conn, sql_data) != 1:
                    print("遇到异常")
                    return 0
def sql_to_airbill_fentan_bag(lading_sum,lading_index,bag_list,shipper_list,customerCode,Charge_Weight,servercode,currency,source):
    lading_list=[]
    for i in range(lading_sum):
        lading_number = request_airlading_withbag_fee(lading_number=str(lading_index+i), bag_list=bag_list, shipper_list=shipper_list, customerCode=customerCode, servercode=servercode, Charge_Weight=Charge_Weight,currency=currency,fee_number=3, source=source)
        lading_list.append(lading_number)
    billid = sql_to_airbill(servercod=servercode)
    sql_to_airbill_ladingdetails(billid=billid,currency=currency, lading_list=lading_list)
    sql_to_airbill_fee(billid=billid, lading_list=lading_list)
    return lading_list
def sql_to_airbill_fentan(lading_sum,lading_index,bag_number,waybill_number,customerCode,Charge_Weight,yt_number,fee_number,servercode,transfertype,ifotherfee,currency,source):
    lading_list=[]
    for i in range(lading_sum):
        lading_number,bags = request_airlading_fee(lading_index+i+1,bag_number,waybill_number,customerCode,Charge_Weight,yt_number,fee_number,servercode,transfertype,ifotherfee,source)
        lading_list.append(lading_number)
    billid = sql_to_airbill(servercod=servercode)
    sql_to_airbill_ladingdetails(billid=billid,currency=currency, lading_list=lading_list)
    sql_to_airbill_fee(billid=billid, lading_list=lading_list)
def sql_to_lipei_settlement(servercode,check_type,checkpattern):
    '''
    :param servercode: 服务商代码
    :param checkpattern: A总金额对账 D明细对账
    :return: 返回账单id
    '''
    print("创建理赔对账编号-----")
    bill_code = 'MDDZ' + ymd_ms() + rand1_9()
    sql_bill = "INSERT INTO `fms_db_now`.`end_reconcile_bill`( `check_status`, `deal_status`, `check_type`, `check_pattern`, `bill_type`, `service_code`, `check_number`, `amount`, `currency`, `rate`, `rate_enable`, `checkby`, `checkon`, `createdby`, `createdon`, `updateby`, `updateon`, `bill_count`, `differCount`, `remark`, `audit_status`, `auditby`, `auditon`, `verifi_status`, `settingId`, `compar_starton`, `compar_endedon`, `sure_amount`, `allocation_state`, `issplit`) " \
               "VALUES ('E', 'S', '%s', '%s', 'Y', '%s','%s' , 5000.00, 'RMB', NULL, NULL, 966, '%s', 1, '%s', 966, '%s', 1, 1, '', 'W', NULL, NULL, NULL, -1, '%s', '%s', 0.00, 'N', NULL);" \
               %(check_type,checkpattern,servercode,bill_code,now(),now(),now(),now(),now())
    sql_select_bill ="select end_reconcile_billId from  end_reconcile_bill  where check_number='%s' and check_type='C';"%(bill_code)
    if excute_sql(fms_db,fms_conn,sql_bill)==1:
        if excute_sql(fms_db, fms_conn, sql_select_bill) == 1:
            bill_id = fms_db.fetchall()[0][0]
            print(bill_id)
            return bill_id
    else:
        print("遇到异常!!!")
def sql_to_chongpai_settlement(servercode,check_type,bill_type):
    '''
    :param servercode: 服务商代码
    :return: 返回账单id
    '''
    print("创建海外重派对账编号-----")
    bill_code = 'MDDZ' + ymd_ms() + rand1_9()
    sql_bill = "INSERT INTO `fms_db_now`.`end_reconcile_bill`( `check_status`, `deal_status`, `check_type`, `check_pattern`, `bill_type`, `service_code`, `check_number`, `amount`, `currency`, `rate`, `rate_enable`, `checkby`, `checkon`, `createdby`, `createdon`, `updateby`, `updateon`, `bill_count`, `differCount`, `remark`, `audit_status`, `auditby`, `auditon`, `verifi_status`, `settingId`, `compar_starton`, `compar_endedon`, `sure_amount`, `allocation_state`, `issplit`) " \
               "VALUES ('E', 'S', '%s', NULL, '%s', '%s','%s' , 5000.00, 'RMB', NULL, NULL, 966, '%s', 1, '%s', 966, '%s', 1, 1, '', 'W', NULL, NULL, NULL, -1, '%s', '%s', 0.00, 'N', NULL);" \
               %(check_type,bill_type,servercode,bill_code,now(),now(),now(),now(),now())
    sql_select_bill ="select end_reconcile_billId from  end_reconcile_bill  where check_number='%s';"%(bill_code)
    if excute_sql(fms_db,fms_conn,sql_bill)==1:
        if excute_sql(fms_db, fms_conn, sql_select_bill) == 1:
            bill_id = fms_db.fetchall()[0][0]
            print(bill_id)
            return bill_id
    else:
        print("遇到异常!!!")
def sql_moduan_mingxi(billId,hawbcode):
    serial_number=0
    for i in hawbcode:
        serial_number=serial_number+1
        servercode = "RE" + i
        sql_moduan_mingxi ="INSERT INTO `fms_db_now`.`end_reconcile_billdetails`(`billId`, `serial_number`, `deal_status`, `hawbcode`, `servicecode`, `currency`, `remark`, `verifi_status`, `audit_status`, `data_type`, `amount`, `charge_weight`, `operation_status`, `country_code`, `measure_nuit`, `check_status`, `serverchannelcode`, `bill_date`, `check_amount`) " \
                       "VALUES (%s, %s, 'S', '%s', '%s', 'RMB', 'test-python', '1', 'W', 'B', 2.19, 21.9, 'O', 'US', 'kg', 'P', 'TEST008', '%s', 0.00);"\
                       %(billId,serial_number,i,servercode,now())
        if excute_sql(fms_db, fms_conn, sql_moduan_mingxi) == 1:
            pass
        else:
            print("遇到异常!!!")
def sql_MDlading_shenhe_fee(billId):
    print("末端提单对账增加审核费用-----")
    sql_select_billdetailId = "select billdetailId from  end_reconcile_billdetails where billId=%s" % (billId)
    if excute_sql(fms_db, fms_conn, sql_select_billdetailId) == 1:
        list_billdetails = fms_db.fetchall()
        print(list_billdetails)
    else:
        print("遇到异常")
        return 0
    for billdetail in list_billdetails:
        fee_list = ["L3","QQ","E2"]
        length = len(fee_list)
        for i in range(length):
            if i==0 or random.randint(1,length)==3:
                data = "INSERT INTO `fms_db_now`.`end_reconcile_audit_fee`( `billdetailid`, `feeId`, `auditby`, `auditon`, `remark`, `deal_type`, `fee_type`, `amount`, `currency`) " \
               "VALUES (%s, 0, 1, '%s', '对比已通过-脚本', 'B', '%s', 143.210, 'RMB');"\
               %(billdetail[0],now(),fee_list[i])
                if excute_sql(fms_db, fms_conn, data) != 1:
                    print("遇到异常")
                    return 0

def sql_moduan_shenhe_fee(billId,ifmingxi=1):
    print("海外重派对账编号增加理赔审核费用-----")
    sql_select_billdetailId = "select billdetailId from  end_reconcile_billdetails where billId=%s" % (billId)
    if excute_sql(fms_db, fms_conn, sql_select_billdetailId) == 1:
        list_billdetails = fms_db.fetchall()
        print(list_billdetails)
    else:
        print("遇到异常")
        return 0
    if ifmingxi==1:
        for billdetail in list_billdetails:
            fee_list = ["L3","QQ","E2"]
            length = len(fee_list)
            for i in range(length):
                if i==0 or random.randint(1,length)==3:
                    data = "INSERT INTO `fms_db_now`.`end_reconcile_audit_fee`( `billdetailid`, `feeId`, `auditby`, `auditon`, `remark`, `deal_type`, `fee_type`, `amount`, `currency`) " \
                   "VALUES (%s, 0, 1, '%s', '对比已通过-脚本', 'B', '%s', 143.210, 'RMB');"\
                   %(billdetail[0],now(),fee_list[i])
                    if excute_sql(fms_db, fms_conn, data) != 1:
                        print("遇到异常")
                        return 0
def sql_to_chongpai_daijiesuan_bag(shipper_list,customerCode,if_pqm,servercode,source):
    '''
    理赔明细对账-实际
    :param yd_number:
    :param waybill_number:
    :param customerCode:
    :param transfertype:
    :param servercode:
    :param source:
    :return:
    '''
    billid = sql_to_chongpai_settlement(servercode,check_type="O",bill_type="A")
    hawbcode_list=[]
    request_chongpai_withbag_fee(shipper_list,customerCode,servercode,if_pqm,source)
    for hawbcode in shipper_list:
        hawbcode = hawbcode + "-1"
        hawbcode_list.append(hawbcode)
    sql_moduan_mingxi(billId=billid, hawbcode=hawbcode_list)
    sql_moduan_shenhe_fee(billId=billid)
    data_to_asyncdata(billid=billid,servercode=servercode,BsnType="O",pattern="R")
    return hawbcode_list
def sql_to_chongpai_daijiesuan(yd_number,waybill_number,customerCode,transfertype,servercode,source):
    '''
    理赔明细对账-实际
    :param yd_number:
    :param waybill_number:
    :param customerCode:
    :param transfertype:
    :param servercode:
    :param source:
    :return:
    '''
    billid = sql_to_chongpai_settlement(servercode,check_type="O",bill_type="A")
    hawbcode_list=[]
    for i in range(yd_number):
        hawbcode = request_chongpai_fee(waybill_number,customerCode,transfertype,servercode,source)
        hawbcode = hawbcode + "-1"
        hawbcode_list.append(hawbcode)
    sql_moduan_mingxi(billId=billid, hawbcode=hawbcode_list)
    sql_moduan_shenhe_fee(billId=billid)
    data_to_asyncdata(billid=billid,servercode=servercode,BsnType="O",pattern="R")
    return hawbcode_list
def sql_to_MDYD_settlement(servercode,check_type,bill_type):
    '''
    :param servercode: 服务商代码
    :return: 返回账单id
    '''
    print("创建海外重派对账编号-----")
    bill_code = 'MDDZ' + ymd_ms() + rand1_9()
    sql_bill = "INSERT INTO `fms_db_now`.`end_reconcile_bill`( `check_status`, `deal_status`, `check_type`, `check_pattern`, `bill_type`, `service_code`, `check_number`, `amount`, `currency`, `rate`, `rate_enable`, `checkby`, `checkon`, `createdby`, `createdon`, `updateby`, `updateon`, `bill_count`, `differCount`, `remark`, `audit_status`, `auditby`, `auditon`, `verifi_status`, `settingId`, `compar_starton`, `compar_endedon`, `sure_amount`, `allocation_state`, `issplit`) " \
               "VALUES ('E', 'S', '%s', NULL, '%s', '%s','%s' , 5000.00, 'RMB', NULL, NULL, 966, '%s', 1, '%s', 966, '%s', 1, 1, '', 'W', NULL, NULL, NULL, -1, '%s', '%s', 0.00, 'W', NULL);" \
               %(check_type,bill_type,servercode,bill_code,now(),now(),now(),now(),now())
    sql_select_bill ="select end_reconcile_billId from  end_reconcile_bill  where check_number='%s';"%(bill_code)
    if excute_sql(fms_db,fms_conn,sql_bill)==1:
        if excute_sql(fms_db, fms_conn, sql_select_bill) == 1:
            bill_id = fms_db.fetchall()[0][0]
            print(bill_id)
            return bill_id
    else:
        print("遇到异常!!!")
def sql_MDlading_mingxi(billId,lading_list,service_code):
    serial_number=0
    for i in lading_list:
        get_qudao_guojia = "select ServerChannelCode,CountryCode, count(*),sum(ServerChargeWeight) from bsn_receivablebusiness where " \
                        "BsId in(select BsId from lading_bsn_relate where lading_id in(select lading_id from lading_info where lading_number='%s')) GROUP BY ServerChannelCode,CountryCode" % (
                            i)

        get_bsn_data = "select BsId,ShipperCode,ServerChargeWeight,ShipperWeight,ServerWeight,ServerChannelCode,CountryCode from bsn_receivablebusiness where " \
                       "BsId in(select BsId from lading_bsn_relate where lading_id in(select lading_id from lading_info where lading_number='%s'));"%(i)
        service_coed ="select service_code from lading_info where lading_number='%s'"%(i)
        #服务商代码
        if excute_sql(fms_db, fms_conn, service_coed) == 1:
            service_code = fms_db.fetchall()[0][0]
        else:
            print("遇到异常!!!")
        #末端对账提单与运单关系
        if excute_sql(fms_db, fms_conn, get_bsn_data) == 1:
            bsn_data_list  = fms_db.fetchall()
            for BsId,ShipperCode,ServerChargeWeight,ShipperWeight,ServerWeight,ServerChannelCode,CountryCode in bsn_data_list:
                ServerChargeWeight = float(repr(ServerChargeWeight).split("'")[1])
                ShipperWeight = float(repr(ShipperWeight).split("'")[1])
                ServerWeight = float(repr(ServerWeight).split("'")[1])
                sql_bsn = "INSERT INTO `fms_db_now`.`end_reconcile_lading_bsn`( `billId`, `lading_number`, `BsId`, `ShipperCode`, `ServerChargeWeight`, `ShipperWeight`, `ServerWeight`, `amount`, `serverchannelcode`, `country_code`, `service_code`) VALUES " \
                          "(%s, '%s', %s, '%s', %s, %s, %s, 0.00, '%s', '%s', '%s');"\
                          %(billId,i,BsId,ShipperCode,ServerChargeWeight,ShipperWeight,ServerWeight,ServerChannelCode,CountryCode,service_code)
                if excute_sql(fms_db, fms_conn, sql_bsn) == 1:
                    pass
                else:
                    print("遇到异常!!!")
        else:
            print("遇到异常!!!")
        #末端对账提单明细
        if excute_sql(fms_db, fms_conn, get_qudao_guojia) == 1:
            qudao_guojia  = fms_db.fetchall()
            for qudao,guojia,yd_sum,yd_weight in qudao_guojia:
                serial_number = serial_number + 1
                yd_weight = float(repr(yd_weight).split("'")[1])
                sql_moduan_mingxi = "INSERT INTO `fms_db_now`.`end_reconcile_lading_billdetails`( `billId`, `serial_number`, `deal_status`, `lading_number`, `currency`, `remark`, `bill_count`, `verifi_status`, `audit_status`, `data_type`, `amount`, `charge_weight`, `serverchannelcode`, `country_code`, `measure_nuit`, `check_status`, `bill_date`, `check_amount`, `allocation_state`, `allocation_Id`) VALUES " \
                                    "( %s, %s, 'S', '%s', 'USD', '导入测试提单啦', 1, '1', 'W', 'B', 73.00, 20.500, '%s', '%s', 'KG', 'R', '%s', 0.00, 'N', NULL);" \
                                    % (billId, serial_number,i,qudao,guojia, y_m_d000())
                if excute_sql(fms_db, fms_conn, sql_moduan_mingxi) == 1:
                    sql_lading_detali = "select lad_detailId,serial_number from end_reconcile_lading_billdetails where billId=%s and serial_number=%s;"%(billId,serial_number)
                    if excute_sql(fms_db, fms_conn, sql_lading_detali) == 1:
                        lad_detailId,serial_number = fms_db.fetchall()[0]
                        sql_to_audit ="INSERT INTO `fms_db_now`.`end_reconcile_lading_billdetails_audit`(`lad_detailId`, `bill_count`, `charge_weight`, `serverchannelcode`, `country_code`) VALUES " \
                                      "(%s, %s, %s, '%s', '%s');"%(lad_detailId,yd_sum,yd_weight,qudao,guojia)

                        if excute_sql(fms_db, fms_conn, sql_to_audit) == 1:
                            pass
                        else:
                            print("遇到异常!!!")
                fee_code_list = ["E2", "E1", "T1", "ch","H6"]
                for fee_code in fee_code_list:
                    sql_to_fee = "INSERT INTO `fms_db_now`.`end_reconcile_lading_bill_fee`(`billId`, `serial_number`, `amount`, `fee_type`, `rate`, `currency`, `auditby`, `auditon`, `fee_source`, `remark`, `is_audit`) VALUES " \
                                 "(%s, %s, 30.000, '%s', 1.0000, 'USD', 0, '%s', 'B', '', 'N');" % (billId, serial_number,fee_code,y_m_d000())
                    if excute_sql(fms_db, fms_conn, sql_to_fee) == 1:
                        sql_select = "select feeId from end_reconcile_lading_bill_fee where billId=%s and serial_number=%s and  fee_type='%s';"%(billId,serial_number,fee_code)
                        if excute_sql(fms_db, fms_conn, sql_select) == 1:
                            fee_id = fms_db.fetchall()[0][0]
                            sql_to_audit_fee = "INSERT INTO `fms_db_now`.`end_reconcile_lading_audit_fee`( `lad_detailId`, `feeId`, `auditby`, `auditon`, `remark`, `deal_type`, `fee_type`, `amount`, `currency`) VALUES " \
                                               "(%s, %s, 1, NOW(), '对比已通过-python脚本', 'B', '%s', 21.000, 'USD');" % (lad_detailId,fee_id, fee_code)
                            if excute_sql(fms_db, fms_conn, sql_to_audit_fee) == 1:
                                pass
                            else:
                                print("遇到异常4!!!")
                        else:
                            print("遇到异常5!!!")
                    else:
                        print("遇到异常2!!!")
        else:
            print("遇到异常0!!!")
        #插入提单运单关系表
        sql ="select b.lad_bsnId, a.lad_detailId from (select lad_detailId,serverchannelcode,country_code from  end_reconcile_lading_billdetails_audit where " \
             "lad_detailId in(select lad_detailId from end_reconcile_lading_billdetails where billId in(%s))) a RIGHT JOIN (select lad_bsnId,serverchannelcode,country_code" \
             " from end_reconcile_lading_bsn where billId in(%s)) b on a.serverchannelcode=b.serverchannelcode and a.country_code=b.country_code"%(billId,billId)
        if excute_sql(fms_db, fms_conn, sql) == 1:
            data_list = fms_db.fetchall()
            for data in data_list:
                filter_sql ="INSERT INTO `fms_db_now`.`end_reconcile_lading_bsn_filter`( `lad_bsnid`, `lad_detailid`) VALUES ( %s, %s);"%(data[0],data[1])
                if excute_sql(fms_db, fms_conn, filter_sql) == 1:
                    pass
                else:
                    print("遇到异常8!!!")
        else:
            print("遇到异常9!!!")
def sql_to_MDlading_daijiesuan_bag(lading_list,md_servercode):
    '''
    :return:
    '''
    billid = sql_to_chongpai_settlement(servercode=md_servercode,check_type="N",bill_type="T")
    sql_MDlading_mingxi(billid, lading_list,service_code=md_servercode)
    return lading_list
def sql_to_MDlading_daijiesuan(lading_number,md_servercode,lading_index,bag_number,waybill_number,customerCode,Charge_Weight,yt_number,fee_number,servercode,transfertype,ifotherfee,source):
    '''
    理赔明细对账-实际
    :param yd_number:
    :param waybill_number:
    :param customerCode:
    :param transfertype:
    :param servercode:
    :param source:
    :return:
    '''
    billid = sql_to_chongpai_settlement(servercode=md_servercode,check_type="N",bill_type="T")
    hawbcode_list=[]
    bag_list=[]
    for i in range(lading_number):
        lading,bags =request_airlading_fee(lading_index+i+1,bag_number,waybill_number,customerCode,Charge_Weight,yt_number,fee_number,servercode,transfertype,ifotherfee,source)
        hawbcode_list.append(lading)
        for bag in bags:
            bag_list.append(bag["bag_labelcode"])
        #末端账单与提单明细
        #sql = "select * from end_reconcile_lading_billdetails where billId in(select end_reconcile_billId from  end_reconcile_bill  where check_number='%s');"%(lading)
    car_data = fahuo_with_bag(bag_list=bag_list, server_code="5555555", bill_count=1, charge_weight=3.33, org_code="43", destination="CC", source=1)
    fee_to_zhuanyun(Car_Number=car_data["car_number"], Waybill_Code=car_data["departure_number"],
                    Server_Code="5555555", source=source, Charge_Weight=3.33, Start_Place="43",
                    end_Place="CC", BusinessTime=now_T())
    time.sleep(5)
    print("休眠5秒,让数据入库")
    sql_MDlading_mingxi(billid, hawbcode_list,md_servercode)
    # sql_moduan_mingxi(billId=billid, hawbcode=hawbcode_list)
    # sql_moduan_shenhe_fee(billId=billid)
    #data_to_asyncdata(billid=billid,servercode=servercode,BsnType="O",pattern="R")
    return hawbcode_list
def sql_to_MDYD_daijiesuan_bag(shipper_code_list, servercode):
    '''
    理赔明细对账-实际
    :param yd_number:
    :param waybill_number:
    :param customerCode:
    :param transfertype:
    :param servercode:
    :param source:
    :return:
    '''
    billid = sql_to_chongpai_settlement(servercode,check_type="N",bill_type="Y")
    sql_moduan_mingxi(billId=billid, hawbcode=shipper_code_list)
    sql_moduan_shenhe_fee(billId=billid)
    #data_to_asyncdata(billid=billid,servercode=servercode,BsnType="O",pattern="R")
    return shipper_code_list
def sql_to_MDYD_daijiesuan(lading_number,lading_index, bag_number, waybill_number, customerCode,Charge_Weight, yt_number, fee_number, servercode, transfertype, ifotherfee,source):
    '''
    理赔明细对账-实际
    :param yd_number:
    :param waybill_number:
    :param customerCode:
    :param transfertype:
    :param servercode:
    :param source:
    :return:
    '''
    billid = sql_to_chongpai_settlement(servercode,check_type="N",bill_type="Y")
    shipper_code_list = []
    bag_list = []
    for i in range(lading_number):
        lading, bags = request_airlading_fee(lading_index + i + 1, bag_number, waybill_number, customerCode,
                                             Charge_Weight, yt_number, fee_number, servercode, transfertype, ifotherfee,
                                             source)
        for bag in bags:
            bag_list.append(bag["bag_labelcode"])
            shipper_code_list = shipper_code_list +bag["shipperItems"]
        # 末端账单与提单明细
        # sql = "select * from end_reconcile_lading_billdetails where billId in(select end_reconcile_billId from  end_reconcile_bill  where check_number='%s');"%(lading)
    car_data = fahuo_with_bag(bag_list=bag_list, server_code="5555555", box=1, bill_count=1, charge_weight=3.33,
                              org_code="43", destination="CC", source=1)
    fee_to_zhuanyun(Car_Number=car_data["car_number"], Waybill_Code=car_data["departure_number"],
                    Server_Code="5555555", source=source, Charge_Weight=3.33, Start_Place="43",
                    end_Place="CC", BusinessTime=now_T())
    time.sleep(5)
    print("休眠5秒,让数据入库")

    sql_moduan_mingxi(billId=billid, hawbcode=shipper_code_list)
    sql_moduan_shenhe_fee(billId=billid)
    #data_to_asyncdata(billid=billid,servercode=servercode,BsnType="O",pattern="R")
    return shipper_code_list
def sql_lipei_mingxi(billId,hawbcode,ifmingxi=1):
    print("理赔对账编号增加运单对账明细-----")
    if ifmingxi==1:
        serial_number=0
        for i in hawbcode:
            serial_number=serial_number+1
            sql_moduan_mingxi ="INSERT INTO `fms_db_now`.`claims_reconcile_billdetails`(`billId`, `serial_number`, `deal_status`, `check_status`, `audit_status`, `hawbcode`, `servicecode`, `serverchannelcode`, `country_code`, `currency`, `amount`, `check_amount`, `bill_date`, `remark`)" \
                               "VALUES (%s, %s, 'S', 'R', 'W', '%s', '', '', '', 'RMB', 0.580, 0.000, '%s', '');"\
                           %(billId,serial_number,i,now)
            if excute_sql(fms_db, fms_conn, sql_moduan_mingxi) == 1:
                pass
            else:
                print("遇到异常!!!")
    else:
        sql_moduan_mingxi = "INSERT INTO `fms_db_now`.`claims_reconcile_billdetails`(`billId`, `serial_number`, `deal_status`, `check_status`, `audit_status`, `hawbcode`, `servicecode`, `serverchannelcode`, `country_code`, `currency`, `amount`, `check_amount`, `bill_date`, `remark`)" \
                            "VALUES (%s, 1, 'S', 'R', 'W', '', '', '', '', 'RMB', 68.330, 0.000, '%s', '');" \
                            % (billId, now)
        if excute_sql(fms_db, fms_conn, sql_moduan_mingxi) != 1:
            print("遇到异常!!!")
def sql_lipei_shenhe_fee(billId,servercode,ifmingxi=1):
    print("理赔对账编号增加理赔审核费用-----")
    sql_select_billdetailId = "select billdetailId from  claims_reconcile_billdetails where billId=%s" % (billId)
    if excute_sql(fms_db, fms_conn, sql_select_billdetailId) == 1:
        list_billdetails = fms_db.fetchall()
        print(list_billdetails)
    else:
        print("遇到异常")
        return 0
    if ifmingxi==1:
        for billdetail in list_billdetails:
            sql_lipei_fentan_fee ="INSERT INTO `fms_db_now`.`claims_reconcile_audit_fee`(`billdetailId`, `feeId`, `deal_type`, `fee_type`, `amount`, `currency`, `server_code`, `auditedon`, `auditedby`, `remark`)" \
                              " VALUES ( %s, 0, 'B', 'CD', 0.260, 'RMB', '%s', '%s', 1, '脚本py对比已通过');"\
                              %(billdetail[0],servercode,now())
            if excute_sql(fms_db, fms_conn, sql_lipei_fentan_fee) != 1:
                print("遇到异常")
                return 0
    else:
        sql_lipei_fentan_fee = "INSERT INTO `fms_db_now`.`claims_reconcile_audit_fee`(`billdetailId`, `feeId`, `deal_type`, `fee_type`, `amount`, `currency`, `server_code`, `auditedon`, `auditedby`, `remark`)" \
                               " VALUES ( %s, 0, 'B', 'CD', 68.330, 'RMB', NULL, '%s', 1, '');" \
                               % (list_billdetails[0][0], now())
        if excute_sql(fms_db, fms_conn, sql_lipei_fentan_fee) != 1:
            print("遇到异常")
            return 0
def sql_to_liepei_mingxi_daijiesuan_bag(shipper_list,servercode,source):
    '''
    理赔明细对账-实际
    :param yd_number:
    :param waybill_number:
    :param customerCode:
    :param transfertype:
    :param servercode:
    :param source:
    :return:
    '''
    billid = sql_to_lipei_settlement(servercode, checkpattern="D",check_type="C")
    request_lipei_with_bag(shipper_list,servercode,source)
    sql_lipei_mingxi(billId=billid, hawbcode=shipper_list)
    sql_lipei_shenhe_fee(billId=billid,servercode=servercode)
    data_to_asyncdata(billid=billid,servercode=servercode,BsnType="M",pattern="R")
    return shipper_list
def sql_to_liepei_mingxi_daijiesuan(yd_number,waybill_number,customerCode,transfertype,servercode,source):
    '''
    理赔明细对账-实际
    :param yd_number:
    :param waybill_number:
    :param customerCode:
    :param transfertype:
    :param servercode:
    :param source:
    :return:
    '''
    billid = sql_to_lipei_settlement(servercode, checkpattern="D",check_type="C")
    hawbcode_list=[]
    for i in range(yd_number):
        hawbcode = request_lipei(waybill_number,customerCode,transfertype,servercode,source)
        hawbcode_list.append(hawbcode)
    sql_lipei_mingxi(billId=billid, hawbcode=hawbcode_list)
    sql_lipei_shenhe_fee(billId=billid,servercode=servercode)
    data_to_asyncdata(billid=billid,servercode=servercode,BsnType="M",pattern="R")
    return hawbcode_list

def sql_fentan_log(billid, fen_type):
    print("理赔对账编号插入分摊job队列-----")

    sql_to_fentanlog = "INSERT INTO `fms_db_now`.`allocation_log`( `allocationBy`, `allocationOn`, `allocation_type`, `number_id`, `data_type`, `state`) " \
                       "VALUES ( 1, '%s', '%s', %s, NULL, 0);"%(now(),fen_type,billid)
    if excute_sql(fms_db, fms_conn, sql_to_fentanlog) != 1:
            print("遇到异常")
            return 0
def sql_to_liepei_ZONG_daijiesuan_bag(shipper_list,servercode,source):
    '''
    理赔总金额对账-实际
    :param yd_number:
    :param waybill_number:
    :param customerCode:
    :param transfertype:
    :param servercode:
    :param source:
    :return:
    '''
    billid = sql_to_lipei_settlement(servercode, checkpattern="A",check_type="C")
    request_lipei_with_bag(shipper_list,servercode,source)
    for haocode in shipper_list:
        sql_lipei_bsn_realte = "INSERT INTO `fms_db_now`.`claims_reconcile_amount_bsnrelate`(`billId`, `bsId`, `hawbcode`, `createdon`, `createdby`) " \
                               "VALUES (%s, 1, '%s', '%s', 651);"\
                               %(billid,haocode,now())
        if excute_sql(fms_db, fms_conn, sql_lipei_bsn_realte) != 1:
            print("遇到异常")
            return 0
    sql_lipei_mingxi(billId=billid, hawbcode=shipper_list,ifmingxi=2)
    sql_lipei_shenhe_fee(billId=billid,servercode=servercode, ifmingxi=2)
    #sql_fentan_log(billid, fen_type="M")
    data_to_asyncdata(billid=billid,servercode=servercode,BsnType="M", pattern="A")
    data_leipei_to_fentan(billid, servercode)
    return shipper_list
def sql_to_liepei_ZONG_daijiesuan(yd_number,waybill_number,customerCode,transfertype,servercode,source):
    '''
    理赔总金额对账-实际
    :param yd_number:
    :param waybill_number:
    :param customerCode:
    :param transfertype:
    :param servercode:
    :param source:
    :return:
    '''
    billid = sql_to_lipei_settlement(servercode, checkpattern="A",check_type="C")
    hawbcode_list=[]
    for i in range(yd_number):
        hawbcode = request_lipei(waybill_number,customerCode,transfertype,servercode,source)
        hawbcode_list.append(hawbcode)
    for haocode in hawbcode_list:
        sql_lipei_bsn_realte = "INSERT INTO `fms_db_now`.`claims_reconcile_amount_bsnrelate`(`billId`, `bsId`, `hawbcode`, `createdon`, `createdby`) " \
                               "VALUES (%s, 1, '%s', '%s', 651);"\
                               %(billid,haocode,now())
        if excute_sql(fms_db, fms_conn, sql_lipei_bsn_realte) != 1:
            print("遇到异常")
            return 0
    sql_lipei_mingxi(billId=billid, hawbcode=hawbcode_list,ifmingxi=2)
    sql_lipei_shenhe_fee(billId=billid,servercode=servercode, ifmingxi=2)
    #sql_fentan_log(billid, fen_type="M")
    data_to_asyncdata(billid=billid,servercode=servercode,BsnType="M", pattern="A")
    data_leipei_to_fentan(billid, servercode)
    return hawbcode_list
def data_to_asyncdata(billid,BsnType,servercode,pattern):
    type_name=""
    if BsnType=="M":
        print("理赔数据插入待结算队列")
        type_name="理赔"
    elif BsnType=="O":
        print("海外重派数据插入待结算队列")
        type_name = "海外重派"
    sql_data = "select check_number from  end_reconcile_bill  where end_reconcile_billId=%s;"%(billid)
    if excute_sql(fms_db, fms_conn, sql_data) == 1:
        check_number = fms_db.fetchall()[0][0]
    else:
        check_number =""
        print("遇到异常")
        return 0
    sql_data = " INSERT INTO `fms_db_now`.`fms_async_data`(`data_key`, `data_content`, `business_type`, `upload_date`, `uploadby`, `deal_date`, `deal_date_end`, `deal_state`, `remark`) " \
               "VALUES ('%s', '{\"BsnType\":\"%s\",\"BsnNumber\":\"%s\",\"SourceType\":\"%s\",\"Source\":\"B\",\"ServerCode\":\"%s\"}', 'ES', '%s', 0, '%s', NULL, 'P', '%s费用审核同步待结算队列-脚本。');"\
               %(check_number,BsnType,check_number,pattern,servercode,now(),now(),type_name)
    if excute_sql(fms_db, fms_conn, sql_data) != 1:
            print("遇到异常")
            return 0
def data_leipei_to_fentan(billid,servercode):
    print("理赔总金额数据插入待分摊队列")
    data_sql = "INSERT INTO `fms_db_now`.`fms_async_data`( `data_key`, `data_content`, `business_type`, `upload_date`, `uploadby`, `deal_date`, `deal_date_end`, `deal_state`, `remark`)" \
               " VALUES ('%s', '{\"NumberType\":\"Claims\",\"Number\":\"%s\",\"ServiceCode\":\"%s\",\"CustomerBodyId\":1,\"AllocationBy\":651,\"OperatorType\":\"Complete\",\"SourceType\":\"2\",\"ServerType\":\"2\",\"id\":%s,\"allocation_type\":null,\"source\":\"B\"}', 'AL', '%s', 651, '%s', '%s', 'N', '成功推送到分摊队列。');"\
               %(billid,billid,servercode,billid,now(),now(),now())
    if excute_sql(fms_db, fms_conn, data_sql) != 1:
            print("遇到异常")
            return 0
'''
以下是各个环节预估的代码
'''

def chongpai_jiesuan_yugu(yd_number,waybill_number,customerCode, transfertype, servercode, source):
    '''
    重派预估
    :param yd_number:
    :param waybill_number:
    :param customerCode:
    :param transfertype:
    :param servercode:
    :param source:
    :return:
    '''
    data_list=[]
    for i in range(yd_number):
        data =  request_chongpai_fee(waybill_number+i, customerCode, transfertype, servercode, source)
        data_list.append(data)
    return data_list

def lipei_jiesuan_yugu(yd_number,waybill_number, customerCode, transfertype, servercode, source):
    data_list=[]
    for i in range(yd_number):
        data = request_lipei(waybill_number+i, customerCode, transfertype, servercode, source)
        data_list.append(data)
    return data_list

if __name__=="__main__":
    lading_index = lading_generate() #xxx-2040xxxx 提单序列号，避免重复
    waybill_number = random.randint(10000000,99999999) #运单序列号
    bag_number = 1 #袋子数量
    Charge_Weight = 1.188 #空运提单重量
    fee_number = 2 #空运提单费用个数  末端费用项个数
    yd_number= 4#运单数量
    yt_number = 4 #袋子的运单数量
    transfertype = 1 #不等于1 则随机状态 运单的转运状态
    ifotherfee = 1 #空运提单费用是否需要其他费用项
    car_number = 10 #卡车序列号
    ifoversea = 2 #1海外中转，2发货中港
    operation_type_code = ["ST", "CL", "CI", "CO", "PU"]
    operation_type_code = random.choice(operation_type_code)
    transport_type_code = "KC"  #运输方式(KC卡车、AN航空、WL快递)
    #,"TEST008""AB123","yif" #"5555555"发货中转
    chongpai_server = "TEST007"
    bill_count=5
    #servercode =random.choice(server_list)
    CountryCode="MD"
    transit_country="MX"
    org_code="43"
    destination="CC"
    qg_servercode="MIX0144"#"YIFQG" #YIFQG YS
    md_servercode="BJYWW"
    customerCode = "C00326"  # "C00326"  556273  C00092  556230 2 #客户代码-运单使用  #wt客户C02672 100001 C02621
    source = 1  # 系统来源 1 YT 2 WT
    lading_sum=1
    car_sum=1
    iffahuo=1
    ladingnumber=1 #提单数量
    servercode_diaobo="5555555"
    fh_servercode="5555555"
    currency="RMB"
    data_list=[]
    if_yichang = 0  # 0则用新的提单和运单
    server_list = ["yif"]#, "kenny_code","yif"
    servercode = sys_data.severCode
    print(servercode)
    if if_yichang==0:
        bag_list, shipper_list, bag_shipper_list = data_bag_shipper_list(bag_number, waybill_number, customerCode, yt_number,md_servercode, transfertype, source)
        '''保存袋子和运单的数据，用于做其他环节的结算'''
        with open("bag_list.txt","w") as f:
            f.write(str(bag_list))
        with open("shipper_list.txt", "w") as f:
            f.write(str(shipper_list))
        with open("bag_shipper_list.txt", "w") as f:
            f.write(str(bag_shipper_list))
    else:
        '''读取保存的袋子和运单数据，'''
        with open("bag_list.txt", "r") as f:
            bag_list = eval(f.readlines()[0])
        with open("shipper_list.txt", "r") as f:
            shipper_list = eval(f.readlines()[0])
        with open("bag_shipper_list.txt", "r") as f:
            bag_shipper_list = eval(f.readlines()[0])

    #实际- 空运
    lading_list = sql_to_airbill_fentan_bag(lading_sum, lading_index, bag_list, shipper_list, customerCode,Charge_Weight, servercode, currency, source)
    # 实际-调拨
    sql_to_diaobobill_fentan_bag(lading_sum=lading_sum, bag_list=bag_shipper_list, shipper_list=shipper_list, if_pqm=0,transport_type_code=transport_type_code, servercode=servercode, source=source,currency=currency)
    #实际 - 理赔明细对账
    #sql_to_liepei_mingxi_daijiesuan_bag(shipper_list, servercode, source)
    # #实际-理赔总金额对账
    sql_to_liepei_ZONG_daijiesuan_bag(shipper_list,servercode, source)
    # # 实际-海外重派结算
    sql_to_chongpai_daijiesuan_bag(shipper_list=shipper_list,customerCode=customerCode,if_pqm=0,servercode=servercode,source=source)
    # 实际-中转
    sql_to_carbill_fentan_bag(car_sum, car_number, bag_list, CountryCode, transit_country, customerCode, servercode,source, if_pqm=0, iffahuo=1)
    #实际-发货中转 --末端预估需要发货中转
    sql_to_fhzzbill_fentan_bag(lading_sum, org_code, destination, bag_list, shipper_list, Charge_Weight, servercode,if_pqm=0, source=source)
    #实际-清关提单
    #sql_to_qgbill_fentan_bag(lading_list=lading_list, bag_list=bag_list, shipper_list=shipper_list, qg_servercode=servercode, customerCode=customerCode,if_vat=0,source=source)
    # 实际-清关明细
    sql_to_qgydbill_fentan_bag(lading_list=lading_list, qg_servercode=qg_servercode,bag_list=bag_list,shipper_list=shipper_list, customerCode=customerCode, source=source)
    # 实际-末端明细
    sql_to_MDYD_daijiesuan_bag(shipper_code_list=shipper_list, servercode=md_servercode)
    # 实际-末端提单
    #sql_to_MDlading_daijiesuan_bag(lading_list, md_servercode)
    '''单独环节'''
    #理赔预估费用插入
    #lipei_jiesuan_yugu(yd_number=yt_number, waybill_number=waybill_number, customerCode=customerCode, transfertype=transfertype, servercode=servercode, source=source)
    # #实际-理赔明细对账
    #sql_to_liepei_mingxi_daijiesuan(yd_number=yt_number,waybill_number=waybill_number,customerCode=customerCode,transfertype=transfertype,servercode=servercode,source=source)
    # #实际-理赔总金额对账
    #sql_to_liepei_ZONG_daijiesuan(yd_number=yt_number, waybill_number=waybill_number, customerCode=customerCode, transfertype=transfertype, servercode=servercode, source=source)
    #海外重派预估费用插入
    #chongpai_jiesuan_yugu(yd_number=yd_number, waybill_number=waybill_number, customerCode=customerCode, transfertype=transfertype, servercode=servercode, source=source)
    # 实际-海外重派结算
    #sql_to_chongpai_daijiesuan(yd_number, waybill_number, customerCode, transfertype, servercode, source)
    # 实际-末端运单对账单生成
    #sql_to_MDYD_daijiesuan(yd_number, waybill_number, customerCode, transfertype, servercode, source)

    # 实际-空运
    #sql_to_airbill_fentan(lading_sum, lading_index, bag_number, waybill_number, customerCode, Charge_Weight, yt_number,fee_number, servercode, transfertype, ifotherfee,currency, source)

    # 实际-卡车
    #sql_to_carbill_fentan(car_sum, car_number, CountryCode, transit_country, bag_number, waybill_number, customerCode,yt_number, servercode, transfertype, source, iffahuo=1)

    # 预估-清关提单
    #qglading_jiesuan_yugu(ladingnumber, lading_index, bag_number, servercode, qg_servercode, waybill_number,customerCode, Charge_Weight, yt_number, fee_number, transfertype, ifotherfee, source)
    # 实际-清关提单对账单生成
    #sql_to_qgbill_fentan(lading_number=1, lading_index=lading_index, bag_number=bag_number, servercode=servercode, qg_servercode=qg_servercode, waybill_number=waybill_number,customerCode=customerCode, Charge_Weight=Charge_Weight, yt_number=yt_number, fee_number=fee_number, transfertype=transfertype, ifotherfee=ifotherfee, source=source)
    # 实际-清关运单对账单生成
    #sql_to_qgydbill_fentan(lading_number=1, lading_index=lading_index, bag_number=bag_number, servercode=servercode, qg_servercode=qg_servercode, waybill_number=waybill_number,customerCode=customerCode, Charge_Weight=Charge_Weight, yt_number=yt_number, fee_number=fee_number, transfertype=transfertype, ifotherfee=ifotherfee, source=source)

    # 预估-发货中转
    #fahuo_jiesuan_yugu(fahuo_number=1,org_code=org_code,destination=destination,box=bag_number,waybill_number=waybill_number,charge_weight=Charge_Weight,customerCode=customerCode,bill_count=2,servercode=fh_servercode,transfertype=transfertype,source=source,iffahuo=2)

    # 实际-发货中转
    #sql_to_fhzzbill_fentan(lading_sum=1, org_code=org_code,destination=destination,box=bag_number,waybill_number=waybill_number,charge_weight=Charge_Weight,customerCode=customerCode,bill_count=2,servercode=fh_servercode,transfertype=transfertype,source=source,iffahuo=2)

    # 预估-调拨运输
    #diaobo_jiesuan_yugu(diaobo_number=1,bag_number=bag_number, waybill_number=waybill_number, customerCode=customerCode, yt_number=yt_number, transfertype=transfertype,transport_type_code=transport_type_code,servercode=servercode, source=source)

    # 实际-调拨运输
    #sql_to_diaobobill_fentan(lading_sum=lading_sum, bag_number=bag_number, waybill_number=waybill_number, customerCode=customerCode, yt_number=yt_number, transfertype=transfertype,transport_type_code=transport_type_code,servercode=servercode, source=source,currency=currency)

    # 实际-末端运单对账单生成
    #sql_to_MDYD_daijiesuan(lading_number=1, lading_index=lading_index, bag_number=bag_number, waybill_number=waybill_number, customerCode=customerCode, Charge_Weight=Charge_Weight,yt_number=yt_number, fee_number=fee_number, servercode=servercode, transfertype=transfertype, ifotherfee=ifotherfee, source=source)
    # 实际-末端提单对账
    #sql_to_MDlading_daijiesuan(lading_number=1,md_servercode=md_servercode, lading_index=lading_index, bag_number=bag_number, waybill_number=waybill_number, customerCode=customerCode, Charge_Weight=Charge_Weight,yt_number=yt_number, fee_number=fee_number, servercode=servercode, transfertype=transfertype, ifotherfee=ifotherfee, source=source)