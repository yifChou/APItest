# -*- coding;utf-8 -*-
from flask import Flask,render_template,request,jsonify,send_from_directory,abort
import request_order
import  os
import aio_request
import time
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")
@app.route('/order_ramdom_page')
def random_page():
    return render_template("ramdom_order.html")
@app.route('/order_async_page')
def async_page():
    return render_template("async_order.html")
@app.route("/download",methods=["GET"])
def download():
    filename = request.args.get("filename")
    print(filename)
    if request.method == "GET":
        if os.path.isfile(os.path.join('doc',"批量签入签出"+ filename + ".xlsx")):
            return send_from_directory('doc', "批量签入签出"+ filename + ".xlsx", as_attachment=True)
        abort(404)

@app.route("/order",methods=["POST","GET"])
def order():
    length = request.form.get("length")
    wide = request.form.get("wide")
    height = request.form.get("height")
    weight = request.form.get("weight")
    total = request.form.get("total")

    order = request.form.get("orderno")
    order_list = []
    print("长:",length,"宽:",wide,"高:",height,"重量:",weight,"批量下单数量:",total,"订单号:",order)
    try:
        orderidall = request_order.order(orderno=order,length=length,wide=wide,height=height,weight=weight,total=total)
        orderid = orderidall[0]
        order_fail = orderidall[1]
        print(order_fail)
        ordernum = len(orderid)
        orderfail = int(total) - ordernum
        print(order_fail,ordernum,orderfail)
        return render_template("test.html", a = "批量下单成功",result = [ordernum,orderfail,"【未开发】"],orderid =  [order_fail,orderid])
    except Exception as e:
        return render_template("test.html", a="批量下单异常", result = e,orderid =[])
@app.route("/order_ramdom",methods=["POST","GET"])
def order_ramdom():
    total = request.form.get("total")

    order = request.form.get("orderno")
    filename = request.form.get("filename")
    order_list = []
    print("批量下单数量:",total,"订单号:",order)
    try:
        orderidall = request_order.order_random(orderno=order,total=total,filename=filename)
        orderid = orderidall[0]
        order_fail = orderidall[1]
        print(order_fail)
        ordernum = len(orderid)
        orderfail = int(total) - ordernum
        return render_template("test.html", a = "批量下单成功",result = [ordernum,orderfail,"【未开发】"],orderid = [order_fail,orderid],filename = filename)
    except Exception as e:
        return render_template("test.html", a="批量下单异常", result = e,orderid =[])
@app.route("/order_async",methods=["POST","GET"])
def order_async():

    total = request.form.get("total")
    order = request.form.get("orderno")
    filename = request.form.get("filename")
    semaphore = request.form.get("semaphore")
    order_list = []
    print("批量下单数量:",total,"订单号:",order,"文件名：",filename,"并发数：",semaphore)
    try:
        orderidall = aio_request.async_order(ordernum=order,count=total,filename=filename)
        orderid = orderidall[0]
        order_fail = orderidall[1]
        run_time = orderidall[2]
        print(order_fail)
        ordernum = len(orderid)
        orderfail = int(total) - ordernum
        return render_template("test.html", a = "批量下单成功",result = [ordernum,orderfail,run_time],orderid = [order_fail,orderid],filename = filename)
    except Exception as e:
        print(e)
        return render_template("test.html", a="批量下单异常", result = e,orderid =[])


def getTimeOClockOfToday():
    t = time.localtime(time.time())
    time1 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t),'%Y-%m-%d %H:%M:%S'))
    return int(time1)
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000,threaded=True)

