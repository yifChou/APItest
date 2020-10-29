import time,random
def now():
    return time.strftime("%Y-%m-%d %H:%M:%S")
def now_T():
    import time
    return time.strftime("%Y-%m-%dT%H:%M:%S")
def ymd():
    return time.strftime("%Y%m%d")
def y_m_d():
    return time.strftime("%Y-%m-%d")
def time_str():
    return time.strftime("%Y%m%d%H%M%S")
def rand100_999():
    return str(random.randint(100, 999))
def date_now():
    return time.strftime("%m%d")
if __name__=="__main__":
    print(date_now())
