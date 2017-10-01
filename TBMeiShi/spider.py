from selenium import webdriver
import re
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import redis

browser = webdriver.Chrome(executable_path="C:\Program Files\Google\Chrome\Application\chromedriver.exe")
wait = WebDriverWait(browser, 10)

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
redis = redis.Redis(connection_pool=pool)


# 点击搜索框,并且输入美食关键字进行搜索
def search():
    browser.get("https://www.taobao.com/")
    try:
        input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#q")))  # 元素是否加载
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button")))  # 元素是否可以加载
        input.send_keys('美食')  # 文本框输入关键词
        submit.click()  # 点击搜索按钮
        total_page = wait.until(EC.presence_of_element_located(  # 返回的是找到的元素
            (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total")))  # 总页数是否加载完毕
        parse_page()
        return total_page.text  # 返回查找元素的文本
    except TimeoutException as e:
        print('搜索页面元素加载超时 重新加载页面')
        return search()


def next_page(index):
    try:
        input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        input.clear()  # 清楚原先的内容
        input.send_keys(index)
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))).click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(index)))
        # 页面是否显示完成
        parse_page()
        print('翻页完成 : ', index)
    except TimeoutException as e:
        print('分页元素加载超时')


def parse_page():  # 解析网页内容
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "#mainsrp-itemlist .items .item")))
    html = browser.page_source
    doc = pq(html)
    items = doc("#mainsrp-itemlist .items .item").items()
    for item in items:
        product = {
            'img': item.find('.pic-box-inner .pic .img').attr('data-src'),
            'title': item.find('.title').text(),
            'price': item.find('.price').text(),
            'number': item.find('.deal-cnt').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        save_redis(product)


def save_redis(product):
    try:
        redis.hset(product['title'], 'title', product['title'])
        redis.hset(product['title'], 'img', product['img'])
        redis.hset(product['title'], 'price', product['price'])
        redis.hset(product['title'], 'number', product['number'])
        redis.hset(product['title'], 'shop', product['shop'])
        redis.hset(product['title'], 'location', product['location'])
    except Exception as e:
        print('保存到redis出错',e)

def main():
    total = search()
    total = int(re.compile('(\d+)').search(total).group(1))
    for i in range(2,total+1):
        next_page(i)

if __name__ == '__main__':
    main()
