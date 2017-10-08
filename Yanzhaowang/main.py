
import time
from bs4 import BeautifulSoup
import requests
import redis
from queue import Queue
'''
browser = webdriver.Chrome(executable_path="C:\Program Files\Google\Chrome\Application\chromedriver.exe")
wait = WebDriverWait(browser, 10)

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
redis = redis.Redis(connection_pool=pool)
'''
q = Queue(maxsize=-1)
result = Queue(maxsize=-1)
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)
i=0
def getAllSchool(num):
    url = 'http://yz.chsi.com.cn/zsml/queryAction.do'
    data = {
        'mldm': 'zyxw',
        'yjxkdm': '0852',
        'zymc': '计算机技术',
        'xxfs': 1,
        'pageno': num
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Content-Type':'application/x-www-form-urlencoded',
        'Cookie':'JSESSIONID=4CEF73907E98E2CCBE18ED4A9E1167E5; __utma=65168252.1916083962.1503371206.1505813699.1506299342.3; __utmz=65168252.1506299342.3.2.utmcsr=yz.chsi.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; JSESSIONID=190C5C5B5753FA58C691BE7C49B20157; __utmt=1; __utma=229973332.1458172645.1506299336.1506299336.1507438745.2; __utmb=229973332.119.10.1507438745; __utmc=229973332; __utmz=229973332.1507438745.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        'Host':'yz.chsi.com.cn'
    }

    try:
        response = requests.post(url , data=data,headers=headers)
        if response.status_code == 200:
            print("访问 200! ok")
            return response.text
        return None
    except Exception as e:
        print('Error occurred')
        return None

def getSchoolUrl(text):
    soup = BeautifulSoup(text,"html5lib")
    table = soup.find("table",class_="ch-table")
    tbody = table.find("tbody")
    trs = tbody.find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        a=tds[0].find('a')
        href = a['href']
        schoolName=a.get_text()
        city=tds[1].get_text()
        code = tds[2].get_text()
        data = {
            'href':'http://yz.chsi.com.cn'+href,
            'schoolName':schoolName,
            'city':city,
            'code':code
        }
        q.put(data)

def parseSchoolUrl():  # 拼接完成 解析专业 - 人数 - 考试范围
    while not q.empty():
        schoolInfo = q.get()
        print(schoolInfo)
        try:
            response = requests.get(schoolInfo['href'])
            if response.status_code == 200:
                print("访问 200! ok")
                text = response.text
                soup = BeautifulSoup(text, "html5lib")
                table = soup.find("table",class_="ch-table")
                tbody = table.find("tbody")
                trs = tbody.find_all("tr")
                for tr in trs:
                    tds = tr.find_all("td")
                    direction = tds[2].get_text()
                    count = tds[5].get_text()[36:-5]
                    range = tds[6].find("a")['href']
                    data2 = parseRange(range)
                    data = {
                        'direction':direction,
                        'count': count
                    }
                    dictMerged2 = dict(data2, **data)
                    resultDict = dict(schoolInfo, **dictMerged2)
                    result.put(resultDict)
                    print("提取成功")
                time.sleep(1)
        except Exception as e:
            print(str(e))


def parseRange(url):   # 解析考试范围
    try:
        response = requests.get('http://yz.chsi.com.cn'+url)
        if response.status_code == 200:
            print("访问 200! ok")
            text = response.text
            soup = BeautifulSoup(text, "html5lib")
            tbody = soup.find("tbody",class_='zsml-res-items')
            tr = tbody.find("tr")
            tds = tr.find_all("td")
            range_one = tds[0].get_text().replace(' ', '')
            range_two = tds[1].get_text().replace(' ', '')
            range_three = tds[2].get_text().replace(' ', '')
            range_four = tds[3].get_text().replace(' ', '')
            data = {
                'range_one':range_one,
                'range_two': range_two,
                'range_three': range_three,
                'range_four': range_four
            }
            return data
    except Exception as e:
        print(repr(e))

def saveRedis():
    global i
    while not result.empty():
        print('数据保存到redis , 当前序号 : ', i + 1)
        try:
            r.lpush('schoolInfo',result.get())
            i = i + 1
        except Exception as e:
            print('保存到redis出错,错误信息 :', e)
            pass

if __name__ == '__main__':

    text = getAllSchool(8)
    getSchoolUrl(text)
    parseSchoolUrl()
    saveRedis()