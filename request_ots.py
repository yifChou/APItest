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
print(rfid3,len(rfid3))
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
"Host":"ots.g2guat.yunexpress.com",
"Content-Type":"application/json;charset=UTF-8"
}
#print(bag_data(3))
#print(bag_product_line(bag_data(3)))
#print(get_date("%Y-%m-%d %H:%M:%S"))
def get_md5(data):
    m=hashlib.md5()
    m.update(data.encode("utf-8"))
    #print(m.hexdigest()[8:-8],type(m.hexdigest()[8:-8]))
    return m.hexdigest()[8:-8].upper() #返回16位大写

header_test1 = {
"Content-Type": "application/json;charset=UTF-8",
"Content-Length": "228",
}
def get_authorizaiton(account,password):
    author =account + "&" + get_md5(account+"&"+password)
    header_test["Authorization"] = "Basic {}".format(author)
    print(header_test)
    return author
def rand_box():
    type_op = [1,2,3,4]
    number = random.randint(1,1000000)
    box = {
        "BoxNumber": "bos"+str(number),
        "ServiceType": random.choice(type_op),
        "Rfid": "rfid"+str(number),
        "PackageQuantity":4,
        "LabelUrl":"www.baidu.com"
    }
    #print(box)
    return box
def box_data(box_count):
    box_list = []
    for i in range(box_count):
        box_list.append(rand_box())
    return box_list
def rand_package(box=""):
    number = random.randint(1,1000000)
    track_number =["tracking_number"+str(number),""]
    label_url=["www.baidu.com","www.google.com","www.youtube.com","www.twitter.com"]
    service_type = [1,2,3,4]
    country = ["CN","US","AU","AM","JP","CR"]
    package_info = {
        "customer_order_number": "order_number"+str(number),
         "tracking_number": random.choice(track_number),
         "box_number": box,
         "service_type": random.choice(service_type),
         "label_url": random.choice(label_url),
         "label_size": random.choice(service_type),
         "package_weight": random.randint(1,1000),
         "weight_type": random.choice(service_type),
         "package_long": random.randint(1,10),
         "package_width":random.randint(1,10),
         "package_high": random.randint(1,10),
         "service": random.choice(service_type),
         "service_code": "",
         "addressInfo": {
             "name": "name"+ str(number),
             "address": "address" + str(number),
             "doorplate": "",
             "company_name": "",
             "postal_code": "",
             "phone": "",
             "city": "",
             "province": "",
             "country": random.choice(country)
         }
     }
    return package_info
def package_data(number):
    package_info = []
    for i in range(number):
        package_info.append(rand_package())
    return package_info
def package_data_with_box(number,box):
    package_info = []
    for i in range(number):
        package_info.append(rand_package(random.choice(box)["BoxNumber"]))
    return package_info


def lading_info(cang,bags):
    LadingInfo={
            "lading_number":"LA"+get_date("%Y%m%d%H%M%S")+str(int(time.time())),
            #"bag_count":bags,
            "bag_count": len(bags),
            "ware_house_code":cang,
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
            "bag_number":random.choice(house_code)+str(int(time.time()))+str(random.sample(l,1)[0]),
            #"rf_id":"RFID"+str(int(time.time()))+str(random.randint(1,10000)),
            "rf_id": "RFID",
            "bag_count":random.randint(1,10),
            "bag_weight":ramdom_decimal(10,3),
            "bag_volume_weight":ramdom_decimal(10,3),
            "customer_company_code":"YT"}
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

def request_ots(cang,bag,ifonline=0):
    '''
    cang是仓库代码
    bag是袋子数量
    '''
    re = requests
    ots_data["LadingInfo"]=lading_info(cang,bag)
    data_sum = ots_data["LadingInfo"]["bag_count"]
    baginfo = bag_data(bag)
    print("提单袋子数：",data_sum,"入库袋子数：",len(baginfo))
    ots_data["BagInfos"]=baginfo
    ots_data["BagProductLines"] = bag_product_line(baginfo,pline=ots_data["LadingInfo"]["ware_house_code"])

    print(str(ots_data).replace("'",'"'))
    if ifonline:
        print("当前制造线上数据，请谨慎！！！输入1确认，其他退出")
        yes = input("请输入是否线上数据制造")
        if yes == 1 :
            print(urls["Online_otsurl"])
            responese = requests.post(url=urls["Online_otsurl"],json=ots_data,headers=header_test)
        else:
            print("退出！！！")
            return 0
    else:
        print(urls["otsurl"])
        responese = re.post(url=urls["otsurl"], json=ots_data, headers=header_test)
    redata = responese.content.decode("utf-8")
    state = responese.status_code
    print("状态码：",state,"返回信息：",redata)
def bag_product_line(bags,pline):
    bag_product ={
        "bag_number":"2",
        "destinationai_house":"4",
        "sort_id":"1"}

    bag_number=[]
    for bag in bags:
        #print(bag)
        for line in range(4):
            bag_product["bag_number"] = bag["bag_number"]

            bag_product["sort_id"]=line+1
            if line==0:
                bag_product["destinationai_house"] = pline
            elif line==1:
                bag_product["destinationai_house"] = "S"
            elif line==2:
                bag_product["destinationai_house"] = "U"
            elif line==3:
                bag_product["destinationai_house"] = "T"
            bag_number.append(str(bag_product))
    #print(bag_number)
    bag_numberstr=str(bag_number).replace('"',"")
    return eval(bag_numberstr)

if __name__=="__main__":
    R=["282019001615005600001412",
       "528058940000400587C640B4",
       "313331313930303030303036",
       "528068940000400587C3A8B4",
       "313231313930303030333432",
       "313232313930303030303133",
       "313331313930303030303037",
       "313331313930303030303038"]
    R1=["E28068940000400587C5E4B3",
        "313331313930303030303130",
        "313231313930303030333437",
        "E28068940000500587C5C4B3",
        "313231313930303030333436",
        "313232313930303030303131",
        "E28068940000500587C5DCB3",
        "313231313930303030333331",
        "313232313930303030303132",
        "313231313930303030333333",
        "E28068940000400587C5D8B3",
        "313231313930303030333431"]
    R2=["313231313930303030333332",
        "E28068940000500587C5E0B3",
        "313331313930303030303039",
        "313231313930303030333335",
        "313231313930303030333336",
        "313231313930303030333434",
        "E28068940000400587C5B8B3",
        "E28068940000400587C5C0B3",
        "313231313930303030333337",
        "313231313930303030333334",
        "E28068940000500673511C51",
        "E28068940000400587C3A4B4",
        "313231313930303030333430"]
    R4 = ["313331313930303030303037",
"E28068940000500587C600B4",
"E28068940000400587C5D0B4",
"E28068940000400587C5BCB4",
"E28068940000500587C5D8B4",
"313231313930303030323934",
"E28068940000400587C594B4",
"313231313930303030323939",
"E28068940000500587C5A0B4",
"313231313930303030333032",
"E28068940000500587C5B8B4",
"313231313930303030323935",
"E28068940000500587C5CCB4",
"E28068940000400587C5C4B4",
"E28068940000400587C598B4",
"E28068940000500587C590B4",
"E28068940000400587C5F4B4",
"313231313930303030323936"]
    house_code = ["A","B","T","Z1","Z2","Z3","Z8","Z9","Z10","D","LAX","H","SZ","H001","GZ","CQ01"] #测试
#house_code = ["A", "B", "T", "Z1", "Z2", "Z3", "Z8", "Z9", "Z10", "D", "LAX", "H", "SZ", "H001", "GZ", "CQ01"] #线上
    #request_ots("C",R4,ifonline=0)
    patch = random.randint(1,1000000)
    batchdata = {
        "BatchNumber": "test_"+str(patch),
        "ShippingCode": "0",
        "ShippingService": "yif_test",
        "ShippingNumber": "100-20190827",
        "WareHouseCode": "FD",
        "ForecastPackageQuantity": 500,
        "ForecastBoxQuantity": 2,
        "DeliveryTime": "2020-06-08 12:2:1"
    }
    boxdata={
            "BatchNumber":batchdata["BatchNumber"],#"test_706028",#
            "OtsBox":box_data(batchdata["ForecastBoxQuantity"])
            }
    packgedata_without_box={
    "batch_number": batchdata["BatchNumber"],#"test_706028",
    "packageInfo": package_data(batchdata["ForecastPackageQuantity"])
}
    packgedata_with_box = {
        "batch_number": batchdata["BatchNumber"],#"test_706028",#
        "packageInfo": package_data_with_box(batchdata["ForecastPackageQuantity"],boxdata["OtsBox"])
    }
    #post_url = "http://10.168.95.149:8022"
    post_url = "http://ots.g2guat.yunexpress.com" #g2g
    get_authorizaiton("T0002","BLYuCjVv")  #如果身份验证失败，1.账号不存在，没启用 2.token不正确 3.没有缓存
    #get_authorizaiton("WT001","RWOVGNRH")
    print("批次号", batchdata)
    print("箱子号", boxdata)
    print("包裹", packgedata_with_box)
    redata = requests.post(url=post_url + "/api/OtsOpenApi/PredictionBatchNo",json=batchdata,headers=header_test)
    print("批次返回", redata.content.decode("utf-8"))
    redata1 = requests.post(url=post_url + "/api/OtsOpenApi/OtsBoxInfo", json=boxdata,headers=header_test)
    redata2 = requests.post(url=post_url + "/api/OtsOpenApi/ForecastPackageInfo", json=packgedata_with_box,headers=header_test)
    #print("批次返回",redata.content.decode("utf-8"))
    print("箱子返回",redata1.content.decode("utf-8"))
    print("包裹返回",redata2.content.decode("utf-8"))
    # print("批次号",batchdata)
    # print("箱子号", boxdata)
    # print("包裹", packgedata_with_box)

