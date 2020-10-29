import requests
import base64
from global_setting import *
import random
import time
import itertools
import hashlib
import copy
rfids=["313930353039303033363532","313930353130303035323530","313930353130303035303638","313930353039303033323433","313930353130303035303738","313930353130303035323237","313930353039303033363039","313930353130303035323431","313930353130303035323236","313930353039303034303631","313930353130303035313733","313930353039303034313130","313930353039303034313233","313930353130303035323633","313930353130303035313534","313930353039303033363136","313930353039303034313038","313930353039303033343137","313930353130303035323834"]
rfids15=["313930353039303033363634","313930353039303034313136","313930353039303034303631","313930353039303033363039","313930353039303034313038","313930353039303033343137","313930353039303033363532","313930353039303034303934","313930353039303033363136","313930353039303033363331","313930353039303034313130","313930353039303034303836","313930353039303034313233","313930353039303033363031","313930353039303033323433"]
#rfid = list(set(rfids+rfids15))
rfid3=["313930353130303035313935","313930353130303035313539","313930353130303035313734","313930353130303035303738","313930353130303035303631","313930353130303035303439","313930353130303035323131","313930353130303035323134","313930353130303035323733","313930353130303035313733","313930353130303035323436","313930353130303035323237","313930353130303035323236","313930353130303035323431","313930353130303035323530"]
rfid1 = ["313930353130303035303532","313930353130303035303638","313930353130303035313534","313930353130303035323633","313930353130303035313933","313930353130303035323834"]
R1=["E28068940000500587C454B4","E28068940000400587C43CB4","E28068940000400587C450B4","E28068940000500587C434B4","E28068940000500587C42CB4","E28068940000500587C438B4"]
R2=["E28068940000400587C428B4","121190000089000000000000","E28068940000500587C410B4","E28068940000500587C468B4","E28068940000500587C3FCB4","121190000088000000000000","E28068940000500587C458B4"]
R3=["E28068940000400587C400B4","E28068940000500587C464B4","313831323130303030303232","E28068940000500587C420B4","E28068940000400587C40CB4","E28068940000500587C44CB4","E28068940000400587C3F8B4"]
R4=["E28068940000500587C440B4","E28068940000400587C460B4","E28068940000400587C414B4","121190000090000000000000","E28068940000400587C46CB4","E28068940000400587C418B4","E28068940000400587C424B4","313930363235303030303036","E28068940000500587C41CB4"]

R20190830 = ["E28068940000400587C64CB4",
"E28068940000500587C650B4",
"E28068940000400587C654B4",
"313238313930303030303039",
"E28068940000500587C660B4",
"313238313930303030303130",
"313238313930303030303037",
"313238313930303030303038",
"313331313930303030303032",
"E28068940000500587C654B3",
"313331313930303030303031",
"313331313930303030303033",
"E28068940000500587C62CB3",
"313331313930303030303034",
"E28068940000400587C644B3",
"313331313930303030303035",
"E28068940000500587C65CB4"]
R2019083002=["E28068940000500587C624B4",
"E28068940000500587C628B4",
"E28068940000500587C614B4",
"E28068940000500587C644B4",
"313231313930303030323937",
"E28068940000400587C608B4",
"E28068940000500587C60CB4",
"E28068940000500587C618B4",
"E28068940000400587C620B4",
"E28068940000500587C63CB4",
"E28068940000500587C630B4",
"313238313930303030303033",
"E28068940000400587C638B4",
"E28068940000400587C640B4"]
print(rfid3,len(rfid3))
house_code = ["A","B","T","Z1","Z2","Z3","Z8","Z9","Z10","D","LAX","H","SZ","H001","GZ","CQ01"]
def ramdom_decimal(max,decimal):
    import random
    a = round(random.randint(0,max)+ random.random(),decimal)
    return a
def get_date(type):
    from datetime import datetime
    now = datetime.now()
    date = now.strftime(type)
    #print(date)
    return date
def get_combine():
    a = itertools.combinations(["A","B","C"],2)
    for i in a:
        print(i)
    return a
header_test = {
"Content-Type": "application/json;charset=UTF-8",
}

def lading_info(cang,bags):
    LadingInfo={
            "lading_number":"LA"+get_date("%Y%m%d%H%M%S")+str(int(time.time()))+str(random.randint(1,10000)),
            #"bag_count":bags,
            "bag_count": len(bags),
            "ware_house_code":cang,
            "transport_type": "C",
            "airline_company":"yif_api",
            "originai_rport":"起飞机场airport_api",
            "destinationai_rport":"目的机场airport_api",
            "est_originai_time":get_date("%Y-%m-%d %H:%M:%S"),
            "est_destinationai_time":get_date("%Y-%m-%d %H:%M:%S"),
            "tur_originai_time":get_date("%Y-%m-%d %H:%M:%S"),
            "tur_destinationai_time":get_date("%Y-%m-%d %H:%M:%S"),
            "lading_weight":ramdom_decimal(100,3),
            "lading_volume_weight":ramdom_decimal(100,3),
            "customer_company_name":"前海云途",
            "customer_company_code":"YT"}
    return LadingInfo
def bag_info():
    l = list(range(1,10000))
    baginfo = {
            "bag_number":"SF"+random.choice(house_code)+str(int(time.time()))+str(random.sample(l,1)[0]),
            #"rf_id":"RFID"+str(int(time.time()))+str(random.randint(1,10000)),
            "rf_id": "RFID",
            "bag_count":random.randint(1,10),
            "bag_weight":ramdom_decimal(10,3),
            "bag_volume_weight":ramdom_decimal(10,3),
            "customer_company_code":"YT",
            "line_code":""}
    #time.sleep(2)
    return str(baginfo)
def bag_data(bag1):
    baginfo = {
            "bag_number":"SF"+get_date("%Y%m%d")+str(int(time.time()))+str(random.randint(1,10000)),
            "rf_id":"RFID"+str(int(time.time()))+str(random.randint(1,10000)),
            "bag_count":random.randint(1,10),
            "bag_weight":ramdom_decimal(10,3),
            "bag_volume_weight":ramdom_decimal(10,3),
            "customer_company_code":"YT"}
    bags=[]
    for bag in bag1:
        bag = bag_info().replace("RFID",bag )
        bags.append(bag)
    bagstr= str(bags).replace('"',"")
    return eval(bagstr)
def bag_product_line(bags,pline):
    bag_product ={
        "bag_number":"2",
        "destinationai_house":"4",
        "sort_id":"1"}

    bag_number=[]
    for bag in bags:
        #print(bag)
        #lines = random.randint(1,4)
        lines =  4
        for line in range(lines):
            bag_product["bag_number"] = bag["bag_number"]

            bag_product["sort_id"]=line+1
            if line==0:
                bag_product["destinationai_house"] = pline
            elif line==1:
                bag_product["destinationai_house"] = "MX"
            # elif line==2:
            #     bag_product["destinationai_house"] = "F"
            # elif line==3:
            #     bag_product["destinationai_house"] = "ECDC"
            bag_number.append(str(bag_product))
    #print(bag_number)
    bag_numberstr=str(bag_number).replace('"',"")
    print(bag_numberstr)
    return eval(bag_numberstr)

def request_ots(cang,bag,online=0):
    '''
    cang是仓库代码
    bag是袋子数量
    '''
    re = requests.session()
    ots_data["LadingInfo"]=lading_info(cang,bag)
    data_sum = ots_data["LadingInfo"]["bag_count"]
    baginfo = bag_data(bag)
    print("提单袋子数：",data_sum,"入库袋子数：",len(baginfo))
    ots_data["BagInfos"]=baginfo
    ots_data["BagProductLines"] = bag_product_line(baginfo,pline=ots_data["LadingInfo"]["ware_house_code"])
    print(str(ots_data).replace("'",'"'))
    if online:
        print(urls["G2G_OTSURL_online"])
        responese = re.post(url=urls["G2G_OTSURL_online"],json=ots_data,headers=header_test)
    else:
        responese = re.post(url=urls["otsurl"], json=ots_data, headers=header_test)
    redata = responese.content.decode("utf-8")
    state = responese.status_code
    print("状态码：",state,"返回信息：",redata)
def bag_generate():
    bags = []
    list_rifd = ["E28068940000500587C5D8B4",
"E28068940000500587C59CB4",
"313331313930303030303038",
"E28068940000500587C5A0B4",
"313231313930303030333331",
"E28068940000400587C5D0B4",
"E28068940000400587C604B4",
"E28068940000400587C5E0B4",
"313231313930303030333032",
"E28068940000400587C5A4B4",
"E28068940000400587C5DCB4",
"E28068940000500587C590B4",
"E28068940000400587C5C4B4",
"E28068940000500587C650B4",
"313231313930303030323934",
"313231313930303030323736",
"E28068940000400587C570B4",
"E28068940000500587C56CB4",
"E28068940000400587C598B4"]
    rfid_7=["313231313930303030333331",
"313331313930303030303038",
"313331313930303030303036",
"313331313930303030303130",
"313231313930303030333332",
"313231313930303030333334",
"E28068940000400587C604B4"]
    for i in rfid_7:
        bags.append(str(i))
    return bags
def random_bag(bagnumer):
    bags = []
    for i in range(bagnumer):
        bag = "BAG" + time.strftime("%m%d%H%M%S") + str(random.randint(1000, 9999)) + str(random.randint(1000, 9999))
        bags.append(str(bag))
        #time.sleep(1)
    return bags
#print(bag_data(3))
#print(bag_product_line(bag_data(3)))
#print(get_date("%Y-%m-%d %H:%M:%S"))
if __name__=="__main__":
    bag = ["1","2","3","4","5","6"]
    a = random_bag(10)
    for i in range(1):
        request_ots("MD",a,online=0)