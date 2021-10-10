#验证当前的ip地址是否已经开启代理
import requests

targetUrl = 'http://httpbin.org/get'

proxies = {
   'http':'http://118.118.200.240:4220'
}
headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
resp = requests.get(targetUrl, headers=headers)
print(resp.status_code)
print(resp.text)

