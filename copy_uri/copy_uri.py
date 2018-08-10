from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
import io
import sys

# browser = webdriver.Chrome(executable_path="D:\chromedriver_win32\chromedriver.exe")  # 绝对路径
browser = webdriver.Chrome(executable_path=".\chromedriver.exe")        # 相对路径
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') # 解决cmd出现的编码问题

select_text = "医院私有服务_商保结算中心"


# 参数类
class info:
    name = ''
    code = ''
    must = ''
    note = ''

    def __init__(self, name, code, must, note):
        self.name = name
        self.code = code
        self.must = must
        self.note = note

    def __str__(self):
        return self.name + ":" + self.code + ":" + self.must + ":" + self.note + "\n"


# 模拟请求
def simRequest(title, url, id, note, api_con, inVals, outVals):
    # 访问地址
    browser.get("https://ka6108.96717120.com/add_jsp")
    # 下拉框
    f_selet = Select(browser.find_element_by_id("ks_ka_id"))
    f_selet.select_by_visible_text(select_text)

    # 填充表单
    f_id = browser.find_element_by_id("ks_ka_api_id")
    f_name = browser.find_element_by_id("ks_ka_api_name")
    f_describe = browser.find_element_by_id("api_describe")
    f_demo = browser.find_element_by_id("demo_src")
    f_note = browser.find_element_by_id("note")
    f_url = browser.find_element_by_id("s_url")
    # f_id.send_keys("f_id")
    f_id.send_keys(id)
    f_name.send_keys(title)

    f_url.send_keys(url)
    f_describe.send_keys(note)
    f_demo.send_keys(api_con)
    f_note.send_keys('hny/lyh')

    # js = "var sum=document.getElementById('demo_src'); sum.value='" + api_con + "';"
    # browser.execute_script(js)

    # 参数逻辑
    f_inAddBtn = browser.find_element_by_xpath('//*[@id="test_form"]/input[5]')
    f_outAddBtn = browser.find_element_by_xpath('//*[@id="test_form"]/input[8]')
    for i2 in range(1, len(inVals)):
        f_inAddBtn.click()
    for i3 in range(3, len(outVals)):
        f_outAddBtn.click()
    # 添加对应的行

    # 填充入参和出参Input
    f_tr = browser.find_element_by_id("input_param").find_elements_by_tag_name("p")
    for iT in range(1, len(f_tr)):
        if iT - 1 < len(inVals):
            inputs = f_tr[iT].find_elements_by_tag_name("input")
            data = inVals[iT - 1]
            for i4 in range(0, len(inputs)):
                inputs[i4].clear()
                if i4 == 0:
                    inputs[i4].send_keys(data.name)
                elif i4 == 1:
                    inputs[i4].send_keys(data.code)
                elif i4 == 2:
                    inputs[i4].send_keys(data.must)
                elif i4 == 3:
                    inputs[i4].send_keys(data.note)

    f_tr2 = browser.find_element_by_id("return_result").find_elements_by_tag_name("p")
    for iT in range(1, len(f_tr2)):
        if iT - 1 < len(outVals):
            inputs = f_tr2[iT].find_elements_by_tag_name("input")
            data = outVals[iT - 1]
            for i4 in range(0, len(inputs)):
                inputs[i4].clear()
                if i4 == 0:
                    inputs[i4].send_keys(data.name)
                elif i4 == 1:
                    inputs[i4].send_keys(data.code)
                elif i4 == 2:
                    inputs[i4].send_keys(data.must)
                elif i4 == 3:
                    inputs[i4].send_keys(data.note)

    f_submit = browser.find_element_by_xpath('//*[@id="test_form"]/input[13]')
    print(title + "是否提交数据,提交请输入1  取消提交：其他")
    isSubmit = input()
    #isSubmit = '1'
    # 停止提交
    if (isSubmit == '1'):
        print(title + "/" + id + "  提交成功");
        f_submit.click()  # 提交数据
        return 0;
    # 提交
    else:
        print(title + "/" + id + "  终止提交，请检查数据");
        return -1;


# 读取文件def
def read_file():
    f = open("C:\\Users\\Administrator\\Desktop\\api.txt", 'r', encoding='UTF-8')
    list = f.readlines()
    i = 0;
    conswitch = 0
    title = ''
    url = ''
    id = ''
    note = ''
    api_con = ''
    infos = []
    inputVals = []
    outputVals = []
    lineStr = ''
    inOrOutSwitch = 0
    spaceSwitch = False
    firstInto = True
    for line in list:
        # print(line)
        i = i + 1
        lineStr = lineStr + line
        line = line.strip('\n').strip()
        if line == "end":
            print("处理完成，程序结束**************************")
            break
        else:
            # try:
            if i == 1:
                title = line
            elif i == 2:
                url = line
                print(title + "/" + id + "  开始自动化填充数据")
            elif i == 3:
                id = line
            elif i == 4:
                note = line
            # 出现ufeff 问题
            # 如果出现空行,则提交
            # elif line.encode('utf-8').decode('utf-8-sig').strip() == "":
            elif line.encode('utf-8').decode('utf-8-sig').strip() == "eee":
                submitTag = simRequest(title, url, id, note, api_con, inputVals, outputVals)
                # 将不提交的放到另一个文件
                if submitTag == -1:
                    errorF = open("C:\\Users\\Administrator\\Desktop\\errorLine.txt", 'a', encoding='UTF-8')
                    errorF.write(lineStr)
                i = 0
                title = ''
                url = ''
                id = ''
                lineStr = ''
                note = ''
                api_con = ''
                inOrOutSwitch = 0
                inputVals = []
                outputVals = []
                conswitch = 0
                spaceSwitch = False
                firstInto = True
            # 拼接con和参数部分
            else:

                if ('请求报文' in line):
                    conswitch = 1

                if ('参数名称' in line):
                    conswitch = 0
                    continue

                # 拼接con
                if (conswitch == 1):
                    # 下面是添加对应缩进
                    api_con = api_con + line.strip() + '\r\n'

                # 拼接参数
                if (conswitch == 0):
                    items = line.split()
                    i_name = items[0].strip()
                    i_code = items[1].strip()
                    i_must = 'N'
                    i_note = ''

                    if len(items) > 2:
                        tempStr = items[2].strip()
                        if tempStr == 'Y' or tempStr == 'N':
                            i_must = tempStr
                        else:
                            i_note = tempStr

                        for i2 in range(3, len(items)):
                            i_note = i_note + items[i2].strip()

                    # 更改状态变量
                    if ("return_code" == i_code or "resultCode" == i_code or "result_code" == i_code or 'QRMessage' == i_code):
                        inOrOutSwitch = 1

                    tempInfo = info(i_name, i_code, i_must, i_note)
                    if (inOrOutSwitch == 0):

                        if i_note == 'Json格式':
                            spaceSwitch = True
                        elif spaceSwitch:
                            name2 = '&nbsp;&nbsp;&nbsp;&nbsp;' + tempInfo.name
                            tempInfo.name = name2
                        inputVals.append(tempInfo)  # 输入
                    else:
                        # 缩进问题
                        if firstInto and spaceSwitch:
                            spaceSwitch = False
                        firstInto = False

                        if i_note == 'Json格式' or i_note == 'Json数组' or i_note == 'JsonArray格式':
                            spaceSwitch = True

                        elif spaceSwitch:
                            name2 = '&nbsp;&nbsp;&nbsp;&nbsp;' + tempInfo.name
                            tempInfo.name = name2
                        outputVals.append(tempInfo)  # 输出

        # except Exception as e:
        # print(title +"/"+id+" 自动化出现异常:"+str(e))


if __name__ == '__main__':
    print("程序开始**************************")
    # select_text = input()   # 等待输入
    read_file()
