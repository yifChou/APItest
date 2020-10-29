'''在toms库的customer_api_external表'''
import base64
username = "100010"  #customer_code #"C88888"#
password = "rRr1X9zFe2U=" #cae_token #"NMt9f54gz9M="#
def get_authorizaiton():
    author = base64.b64encode(str.encode(username + "&" + password))
    au = author.decode()
    print(author)
    return au
#get_authorizaiton()
urls = {
    #客户下单url
    "orderurl" : "http://10.168.95.103:8080/LMS.API/api/WayBill/BatchAdd",
    "neworderurl":"http://10.168.95.33:9090/api/Waybill/CreateOrder",
    "geturl":"http://10.168.92.138:5000",
    "otsurl":"http://10.168.95.149:8022/api/OtsOpen/AddLadingBagInfo",
    "Online_otsurl":"http://ots.yunexpress.com/api/OtsOpen/AddLadingBagInfo", #
    "G2G_OTSURL":"http://ots.g2guat.yunexpress.com/api/OtsOpen/AddLadingBagInfo",
    "G2G_OTSURL_online":"http://ots.webapi.yunexpresseu.com/api/OtsOpen/AddLadingBagInfo",
}
#客户下单数据
data = [
{
"WayBillNumber":"",
"TrackingNumber":"123456789",
"OrderNumber":"test20190109000003",
"TransactionNumber":"123456789",
"ShippingMethodCode":"PK0357",#"PK0351",#
"Weight":10,
"TotalFee":None,
"TotalQty":None,
"SettleWeight":None,
"PackageVolume":1,
"PackageNumber":1,
"Length":1,
"Height":1,
"SourceCode":"API",
"ShippingInfo":{
"ShippingTaxId":"cn",
"CountryCode":"AF",
"ShippingFirstName":"xing",
"ShippingLastName":"ming",
"ShippingCompany":"company",
"ShippingAddress":"adress",
"ShippingAddress1":"adress1",
"ShippingAddress2":"adress2",
"ShippingCity":"city",
"ShippingState":"guangdong",
"ShippingZip":"123456",
"ShippingPhone":"12345678456"
},
"SenderInfo":{
"CountryCode":"CN",
"SenderFirstName":"xing",
"SenderLastName":"ming",
"SenderCompany":"company",
"SenderAddress":"adress",
"SenderCity":"city",
"SenderState":"guangdong",
"SenderZip":"123456",
"SenderPhone":"12345678456"
},
"IsReturn":True,
"ApplicationType":1,
"InsuranceType":1,
"InsureAmount":1000,
"SensitiveTypeID":1,
"ApplicationInfos":[
{
"ApplicationName":"INCHH A",
"HSCode":"",
"Qty":1,
"UnitPrice":10,
"UnitWeight":1,
"PickingName":"SARA-4.5",
"Remark":"",
"Sku":"",
"CurrencyCode":"USD"
}
]
}
]


ots_data={
    "LadingInfo":
        {
            "lading_number": "TK2008020043",
            "transport_type": "C",
            "bag_count": 16,
            "ware_house_code": "MX",
            "airline_company": "",
            "originai_rport": "",
            "destinationai_rport": "",
            "est_originai_time": "",
            "est_destinationai_time": "2020-08-01T15:00:00",
            "tur_originai_time": "",
            "tur_destinationai_time": "",
            "lading_weight": 0.000,
            "lading_volume_weight": 0.0,
            "customer_company_name": "沃德太客",
            "customer_company_code": "YT"
        },
    "BagInfos":[{
            "bag_number": "GD2007300010",
            "rf_id": "",
            "bag_count": 98,
            "bag_weight": 62.313,
            "bag_volume_weight": 1.0,
            "customer_company_code": "YT",
            "line_code": "AMS-IT-CP1"}
    ],
}