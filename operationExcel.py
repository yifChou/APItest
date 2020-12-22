#!/user/bin/env python
#coding:utf-8


import xlrd
from config import *
from excel_data import *

class OperationExcel:
    '''获取excel文件中的内容'''
    def getExcel(self):
        db = xlrd.open_workbook(DATA_PATH+'\data.xls')
        sheet = db.sheet_by_index(0)
        return sheet

    def get_rows(self):
        '''获取excel的行数'''
        return self.getExcel().nrows

    def get_row_cel(self,row,col):
        '''获取单元格的内容'''
        return self.getExcel().cell_value(row,col)

    def getCaseID(self,row):
        '''获取CaseID'''
        return self.get_row_cel(row, getCaseID())

    def getTitle(self,row):
        '''获取title'''
        return self.get_row_cel(row, getTitle())

    def getUrl(self,row):
        '''获取url'''
        return self.get_row_cel(row,getUrl())

    def get_request_data(self,row):
        '''获取请求参数'''
        return self.get_row_cel(row,getData())

    def getExcept(self,row):
        '''获取期望结果'''
        return self.get_row_cel(row,getExcept())

    def getResult(self,row):
        '''获取实际结果'''
        return self.get_row_cel(row,getResult())







