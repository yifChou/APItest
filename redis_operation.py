import redis
r = redis.Redis(host="10.168.95.36",port=6379,db=1,password="a135246A")
#print(r)
#r.set('name', 'junxi')
#print(r.get('sys_db:sys_language_info:1007').decode("utf-8"))
def get_doc_data(file):
    keys = r.keys()
    for key in keys:
        key_str = key.decode()
        path = key_str.replace(key_str.split(':')[-1],"") #去掉末尾编号
        print(path)
        txt_name = path.replace(":","_")[:-1]
        txt = "C:\\Users\\Administrator\\PycharmProjects\\APItest\\redis_txt\\"+txt_name+".txt"
        if file == path :
            value = r.get(key).decode("utf-8")
            print(value)
            with open(txt,"a+") as f:
                f.writelines(value)
                f.write("\n")
get_doc_data("tms_db:csi_server")