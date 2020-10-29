rabbit_data={
    "account":"leike",
    "password": "a135246A",
    "ip": "10.168.95.36",
    "port": 5672,
    "virtual_host": "/Charge/",
    "queue":"PQM/YT/Cost/CalcChargeIncome"
}
body ="YIF4916402007312002"
def connect_rb(rabbit_data,body):
    import pika
    #建立连接
    userx = pika.PlainCredentials(rabbit_data["account"],rabbit_data["password"])
    conn = pika.BlockingConnection(pika.ConnectionParameters(rabbit_data["ip"],rabbit_data["port"],rabbit_data["virtual_host"],credentials=userx))
    # 开辟管道
    channelx = conn.channel()
    #声明队列，参数为队列名
    channelx.queue_declare(queue=rabbit_data["queue"],durable=True)

    channelx.basic_publish(exchange="",routing_key=rabbit_data["queue"],body=body)
    print("--------发送数据完成-----------")
    #关闭连接
    conn.close()
    print("推送rabbit成功")
    return 1


def connect_rb_text():
    import pika
    # 建立连接
    userx = pika.PlainCredentials("FMS", "a135246A")
    conn = pika.BlockingConnection(pika.ConnectionParameters("10.168.95.43", 5672, "/FMS/", credentials=userx))
    # 开辟管道
    channelx = conn.channel()
    # 声明队列，参数为队列名
    channelx.queue_declare(queue="FMS/Sync/TmsBussiness", durable=True)

    channelx.basic_publish(exchange="", routing_key="FMS/Sync/TmsBussiness", body="YIF4916402007312002")
    print("--------发送数据完成-----------")
    # 关闭连接
    conn.close()
    print("yyyyy")
    return 1
for i in range(1000):
    connect_rb(rabbit_data,body)
    connect_rb_text()