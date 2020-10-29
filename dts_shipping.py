from request_dts import shipping_order_forcar
import random
import time
import requests
def shipping_car_create(car_number,bag_list,url = "http://192.168.88.175:5000"):
    '''
    发货单创建-并绑定袋子
    :param shipping_number: 发货单号
    :param bag_list: 袋子
    :return:
    '''
    data={
        "car_number": car_number,
        "car_created_on": time.strftime("%Y-%m-%d %H:%M:%S"),
        "departure_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "destinationai_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "start_organization_code": "YW",
        "end_location": "NL2",
        "car_type": "1",
        "loading_type": "2",
        "ship_type": "2",
        "service_code": "5555555",
        "over_weight": random.randint(10,100),
        "is_end": "2",
        "BagInfos": bag_list
    }
    print(data)
    response = requests.post(url=url + "/api/ExternalApi/TmsAddDepartureinfo",json=data)
    print("批次请求地址："+url,response.text)
    return response.text
if __name__ =="__main__":
    run_select = "测试"
    number =2020091020
    car_number = 3555
    bag_number = 2
    waybills =2
    systemcode = "YT"
    online_url = "https://dts.yunexpress.com"
    uat_url = "http://dts.uat.yunexpress.com"
    if run_select == "测试":
        if type(bag_number) == int:
            for i in range(2):
                '''测试环境脚本'''
                bag_list = shipping_order_forcar(shipping_number="send_" + str(number + i), bag_number=bag_number,
                                                 waybills=waybills)
                shipping_car_create(car_number="粤B_" + str(car_number + i), bag_list=bag_list)
                print(bag_list)
        else:
            j = 1
            for bag_number in bag_number:
                if run_select == "UAT":
                    '''UAT环境脚本'''
                    bag_list = shipping_order_forcar(shipping_number="send_" + str(number + j), bag_number=bag_number,
                                                     waybills=waybills)
                    shipping_car_create(car_number="粤B_" + str(car_number + j), bag_list=bag_list)
                    print(bag_list)
                elif run_select == "测试":
                    '''测试环境脚本'''
                    bag_list = shipping_order_forcar(shipping_number="send_" + str(number + j), bag_number=bag_number,
                                                     waybills=waybills, url=uat_url)
                    shipping_car_create(car_number="粤B_" + str(car_number + j), bag_list=bag_list)
                    print(bag_list)
                j = j + 1
    elif run_select == "UAT":
        if type(bag_number) == int:
            for i in range(2):
                '''UAT环境脚本'''
                bag_list = shipping_order_forcar(shipping_number="send_" + str(number + i), bag_number=bag_number,
                                                 waybills=waybills,url=uat_url)
                shipping_car_create(car_number="粤B_" + str(car_number + i), bag_list=bag_list)
                print(bag_list)

