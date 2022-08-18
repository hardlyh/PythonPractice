import pdfkit
import requests

config = pdfkit.configuration(wkhtmltopdf=r'D:\\wkhtmltox-0.12.6-1.mxe-cross-win64\\wkhtmltox\\bin\\wkhtmltopdf.exe')
options = {
    'no-outline': None,
    'encoding': "UTF-8"
}
url = 'http://mp.weixin.qq.com/s?__biz=MzU3MzEzOTI2OA==&mid=2247487072&idx=1&sn=c3c6d3481eb3fd97deca572dd837cae6&chksm=fcc77e4bcbb0f75dc9e5f68c2c7b6a8650dc1ba3a5b7a1a6cf6f7b297dcd22578b31a8158d4a#rd'

#response = requests.get(url)
pdfkit.from_url(url, 'test.pdf', options=options,configuration=config)