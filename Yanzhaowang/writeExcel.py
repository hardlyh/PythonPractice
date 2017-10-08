from xlwt import *
import xlwt
import redis
from queue import Queue
import json
import types
import  re

q = Queue(maxsize=-1)
result = Queue(maxsize=-1)
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)
i=0
row=1
def get_redis():
    global  i
    num = r.llen("schoolInfo")
    print(num)
    for i in range(num):
        try:
            q.put(r.lindex("schoolInfo",i).decode('utf-8'))
        except Exception as e:
            print('保存redis出错  : '+e)
#row0 = [u'城市',u'学校', u'专业方向', u'是否211', u'预招收人数', u'政治', u'外语', u'业务课1', u'业务课2',u'招生网址']
def svae_excel():

    global row
    row0 = [u'城市', u'学校', u'专业方向', u'是否211', u'预招收人数', u'政治', u'外语', u'业务课1', u'业务课2', u'招生网址']
    f = xlwt.Workbook()  # 创建工作簿
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i])
    while not q.empty():
        data = q.get()
        data2 = re.sub(r";", r"", data)
        data3 = re.sub(r"\\n", r"", data2)
        data3 = re.sub(r"'", r'"', data3)
        sss= data3.index("count")-3
        oneStr = data3[0:sss]
        twoStr = data3[sss:-1]
        twoStr = re.findall(r'\d+\.?\d*', twoStr)
        oneStr = oneStr + "}";
        resultStr = json.loads(oneStr)
        sheet1.write(row, 0, resultStr['city'])
        sheet1.write(row, 1, resultStr['schoolName'])
        sheet1.write(row, 2, resultStr['direction'])
        sheet1.write(row, 3, resultStr['code'])
        if len(twoStr)>2:
            sheet1.write(row, 4, "总:"+twoStr[0]+"   推免: "+twoStr[1])
        else:
            sheet1.write(row, 4, "数据未知")
        sheet1.write(row, 5, resultStr['range_one'])
        sheet1.write(row, 6, resultStr['range_two'])
        sheet1.write(row, 7, resultStr['range_three'])
        sheet1.write(row, 8, resultStr['range_four'])
        sheet1.write(row, 9, resultStr['href'])
        row=row+1
        print(row)
    f.save('d://demo1.xlsx')  # 保存文件

if __name__ == '__main__':
    get_redis()
    svae_excel()