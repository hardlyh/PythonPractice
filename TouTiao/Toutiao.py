import json
import os
from hashlib import md5
import redis
import requests
from urllib.parse import urlencode
from multiprocessing import Pool


'''
    简单流程
        1.因为是ajax请求,所以要通过分析页面请求的方式来找到ajax请求的页面并且模拟请求得到返回的json
        2.将返回的json字符串转换为json对象 
        3.提取关键字
        4.存储到redis
        5.将图片下载到本地

'''

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)


def get_page_index(offset, keyword):  # 主函数,获取json列表
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1
    }
    try:
        response = requests.get("http://www.toutiao.com/search_content/?" + urlencode(data))
        print("http://www.toutiao.com/search_content/?" + urlencode(data))
        if response.status_code == 200:
            print("访问 200! ok")
            return response.text
        return None
    except Exception as e:
        print('Error occurred')
        return None


def write_file(content):  # 写入到文件
    with open('Toutiao.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def parse_page_index(text):  # 解析主页面并且返回详情页网址
    try:
        data = json.loads(text)  # 转化为json对象
        if data and 'data' in data.keys():
            for item in data.get('data'):
                url = item.get('article_url')
                title = item.get('title')
                images = [de.get('url') for de in item.get('image_detail')]
                data_c = {
                    'url': url,
                    'title': title,
                    'images': images
                }
                save_in_redis(url, data_c)
                for image_url in images:
                    get_image_content(image_url)
    except Exception as e:
        print('错误 :', e)
        pass


def get_image_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            download_image(response.content)
        else:
            return None
    except Exception as e:
        print('访问图片出现错误 :  ', e)


def download_image(content):
    path = '{0}/{1}.{2}'.format(os.getcwd()+'/images', md5(content).hexdigest(), 'jpg')
    print('保存图片 : ', path)
    print(path)
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            f.write(content)
            f.close()


def save_in_redis(url, content):
    print('正在保存数据到redis 当前Url ', url)
    try:
        r.hset(url, 'title', content['title'])
        r.hset(url, 'images', content['images'])
    except Exception as e:
        print('保存出现错误 :', e)
        pass


'''

def get_page_detail(url):  # 得到详情页内容
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except:
        print('parse url :', url)
        return None


def parse_page_detail(html, url): # 解析详情页网址
    print('解析网址 :', url)
    try:
        title_pattern = re.compile('<h2 class="title">(.*?)</h2>')
        result = re.search(title_pattern, html)
        title = result.group(1) if result else ''
        images_pattern = re.compile('var gallery = (.*?);', re.S)
        result = re.search(images_pattern, html)
        if result:
            data = json.loads(result.group(1))  # 转化为json对象
            if data and 'sub_images' in data.keys():  # data不为空并且key中包括sub_images
                sub_images = data.get('sub_images')
                images = [item.get('url') for item in sub_images]  # 遍历json中的每个item, 并且取出url 放到数组中
                data = {
                    'title': title,
                    'url': url,
                    'images': images
                }

    except:
        print('错误',url)
        pass

'''


def main(offset):
    html = get_page_index(0, '街拍')
    parse_page_index(html)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 20 for i in range(2)])
    pool.close()
    pool.join()