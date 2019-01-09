import requests
import base64
from global_setting import *
header_test = {
"Host": "120.76.102.19:8034",
"Content-Type": "application/json;charset=UTF-8",
"Content-Length": "1940",
}
def get():
    pass
def get_authorizaiton():
    author = base64.b64encode(str.encode(username + "&" + password))
    au = author.decode()
    print(au,type(au))
    return au
def post_basic(u,d,authorizaiton = None):
    re = requests.session()
    if authorizaiton is not None:
        header_test["Authorization"] = "Basic {}".format(get_authorizaiton())
    print(header_test)
    redata = re.post(url = u,json = d,headers = header_test).content.decode("utf-8")
    print(redata)
    return redata
get_authorizaiton()
post_basic(u = urls["orderurl"],d= data,authorizaiton=1)