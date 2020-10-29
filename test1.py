import random
def test():
    with open("线上运单_157-26368731.txt","r") as f:
        data = f.readlines()
        print(len(data))
        list_all = []
        j = 10
        list_yd = []
        for i in range(len(data)):
            if 0<i<5000:
                i = data[i].strip()
                j -= 1
                if j >=0:
                    list_yd.append(i)
                else:
                    list_all.append(list_yd)
                    list_yd = []
                    j = 10
        print(list_all,len(list_all))

if __name__=="__main__":
    import requests
    import json

    # url = "http://10.168.95.105:5000/api/BilJsoncharged/AddBilJsoncharged"
    # base_dict = {"Waybill_Code": "YT2020072116400002", "Currency_Code": "YD", "Customer_Code": "AUTO-CUSTO",
    #              "Product_Code": "PK0029", "Server_Code": "", "Server_Type": "PS", "ServerPlace_Code": "",
    #              "System_Code": "YT", "Og_id_ChargeFirst": "YT-HQB-SZ", "Og_id_ChargeSecond": "",
    #              "Arrival_Date": "2020-07-21T16:40:20", "Country": "AR", "Postcode": "518000", "City": "005001",
    #              "Province": "005", "Charge_Weight": 5.0, "Unit_Code": "KG", "Unit_Length": "CM", "Unit_Area": None,
    #              "Unit_Bulk": None, "Unit_Volume": None, "ExtraService": "ss", "ExtraService_Coefficient": "0.8",
    #              "Pieces": 5, "Category_Code": "5", "Declared_Value": 0.8, "Currency": None, "Tariff": "0.6",
    #              "Airline": "中国南方", "Departure_Airport": "宝安机场", "Destination_Airport": "伦敦机场",
    #              "Customs_Clearance_Port": "QHKA", "Start_Place": "MD", "end_Place": "MX", "Remark": None, "Ticket": 5,
    #              "HS_Code": 5, "Box_Number": 5, "First_Long": 0.0, "Two_Long": 0.0, "Three_Long": 0.0,
    #              "BusinessTime": "2020-03-11T00:00:00", "airline_two_code": "BR", "detailEntities": None,
    #              "Goods_Code": None, "IsFinalCharge": False, "ChargType": None, "HCustomsNumber": 0.0,
    #              "MCustomsNumber": 0.0, "LCustomsNumber": 0.0, "HCargoValueNumber": 0.0, "MCargoValueNumber": 0.0,
    #              "LCargoValueNumber": 0.0, "Charge_Volume": 5.0, "Truck_Number": 1, "Tray_Number": 1, "TimeUnti": "Day",
    #              "TimeVaule": 5, "TrackingNumber": "33P"}
    # request_pqm_url_1 = url
    # json_data_1 = {
    #     "id": 0,
    #     "waybill_code": "YT2020072116400002",
    #     "jsonstring": json.dumps(base_dict, ensure_ascii=False),
    #     "error_count": "",
    #     "error_message": "",
    #     "system_source": "YT"
    # }
    # data = requests.post(url=request_pqm_url_1, json=json_data_1).text
    # print(request_pqm_url_1, "结果" + data)
    # if "Code" in data:
    #     print("运单推送PQM计费表成功！！！")
    #     print(json_data_1)
    # else:
    #     print("运单推送PQM计费表失败:", data, request_pqm_url_1, json_data_1)
    serverchannelcode_dict = {
        #"TEST008":[],
        "yif":["TEST007","SHQ"],#"GZYJ","SPLUSZ"
        "AB123":["TEST007","SHQ"]#"HERMES","ABCZ"
    }
    a,b=serverchannelcode_dict["yif"]
    Customs_Clearance_Port, Currency = ["AMS", "RMB"]
    print(a,b,Customs_Clearance_Port, Currency)
