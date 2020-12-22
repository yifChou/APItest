#!/user/bin/env python
#coding:utf-8

class ExcelVarible:
    CaseId =0
    title=1
    url = 2
    data = 3
    expect = 4
    result = 5

def getCaseID():
    return ExcelVarible.CaseId
def getTitle():
    return ExcelVarible.title
def getUrl():
    return ExcelVarible.url
def getData():
    return ExcelVarible.data
def getExcept():
    return ExcelVarible.expect
def getResult():
    return ExcelVarible.result
def getTitle():
    return ExcelVarible.title
def getHeadersValue():
    '''获取请求头'''
    headers={"Content-Type":"application/json"}
    return headers
