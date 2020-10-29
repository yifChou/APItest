import request_dts
from request_dts import *
from test1 import list_all
'''dts创建袋子'''
url = "http://10.168.95.116:5000"
waybills=5 #运单数量
#袋子数量
#bag_number=['BAG03300970424', 'BAG03300970425', 'BAG03300970426', 'BAG03300970427', 'BAG03300970428', 'BAG03300970429', 'BAG03300970430', 'BAG03300970431', 'BAG03300970432', 'BAG03300970433', 'BAG03300970434', 'BAG03300970435', 'BAG03300970436', 'BAG03300970437', 'BAG03300970438', 'BAG03300970439', 'BAG03300970440', 'BAG03300970441', 'BAG03300970442', 'BAG03300970443', 'BAG03300970444', 'BAG03300970445', 'BAG03300970446', 'BAG03300970447']
#YD_LIST = [['YT2010121266213939', 'YT2010121266184954', 'YT2010121266174667', 'YT2010121266154859', 'YT2010121266133724', 'YT2010121266110360', 'YT2010121266079247', 'YT2010121266061773', 'YT2010121263154600', 'YT2010121263129157'], ['YT2010121263061021', 'YT2010121263000926', 'YT2010121227010033', 'YT2010121222056146', 'YT2010121222016888', 'YT2010101277008670', 'YT2010101271000190', 'YT2010021298001835', 'YT2010021272131992', 'YT2010021272111734']]
bag_number = 10
bag_list =[]
number_no = 2020060210
shipping_number = "send"+str(number_no)
print(type(bag_number))
if type(bag_number) ==int:
    for i in list_all:
        data = add_bag(YD_order_exist(i),update_type="A",system_code="YT")
        print(data)
        response = requests.post(url=url + "/api/ExternalApi/AddBagInfo", json=data)
        print(response.text)
        bag_list.append(data["bag_number"])
    batch_creation_old(batch_number="BA_" + str(number_no), bag_list=bag_list
                           , system_code="YT")
    data = {
        "over_weight": random.randint(1, 20),
        "shipping_type": random.choice([1, 2]),
        "service_code": "CC",
        "loading_type": random.choice([1, 2]),
        "car_type": random.choice([1, 2]),
        "shipping_number": shipping_number,
        "shipping_location": "74",
        "departure_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "destinationai_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "car_number": "car" + time.strftime("%Y%m%d"),
        "destination": "深圳",
        "is_need": "Y",
        "bag_numbers": bag_list,
        "system_code": "YT"
    }
    print(data)
    response = requests.post(url=url + "/api/ExternalApi/CreateShipment", json=data)
print(bag_list)
for i in bag_list:
    print(i)
