# douban_post
爬取豆瓣电影海报url
# 豆瓣电影海报爬取

## 目的

已有数据为2w8k条的豆瓣电影id，需要爬取的内容为对应电影的海报url地址，讲爬取的内容写入到excel文件中

## 环境准备

本文讲的是使用Anaconda进行环境的配置

![image-20211010100935633](https://i.loli.net/2021/10/10/12MLhgzZFwIeP9R.png)

### 1.创建一个conda虚拟环境

```shell
conda create -n 环境名称 python=[python版本]
```

### 2.安装需要的环境依赖

需要安装的依赖有requests、openpyxl、xlrd、bs4

```shell
conda install requests
conda install openpyxl
conda install xlrd=1.2.0[安装最新版本会出错]
conda install bs4
```

## 编写爬虫

### 1.从原xlsx文件中读取到movid

```python
def read_excel(file, begin, n):
    #打开文件名为file的xlsx文件
    wb = xlrd.open_workbook(filename=file)
    #打开第一个工作簿
    sheet1 = wb.sheet_by_index(0)
    #创建空数组用户存储读取的movid
    rows = []
    #从begin开始读取n条movid
    for i in range(n):
        row = sheet1.row_values(begin + i)
        rows.append(row[0])
    return rows
```

### 2.发起请求获取数据

在这之前我们先确定我们的数据需要在哪个网址下能爬取到。

https://movie.douban.com/subject/[movid]/

在这个地址下存有我们需要的数据

![image-20211010101814170](https://i.loli.net/2021/10/10/rEM4PLw3szRhdNk.png)

打开网页的开发者工具之后，查看网页的源代码我们可以很轻松找到我们需要爬取的的信息位置。

```python
def getimgpath(movid):
    url = 'https://movie.douban.com/subject/' + movid + '/'
    #这里暂时省略headers的代码
    #向url地址发送http请求
    res = requests.get(url, headers=headers)
    #如果响应的状态码为200说明访问是成功的
    if(res.status_code == 200):
        ans = ''
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            #ans是我们需要的信息，通过如下路径可以获取
            ans = soup.find(attrs={'id': 'mainpic'}).find('img').get('src')
        except BaseException:
            print('Error: ', num)
            return 'Error'
        else:
            print('(', num, '/', 28603, ')', '[ url:', ans, ']')
            return ans
    else:
        print('状态码：',res.status_code)
        return 'none'
```

### 3.写入xlsx文件保存

```python
def write_excel(file, line, id, url):
    #文件读取
    workbook = openpyxl.load_workbook(file)
    worksheet = workbook.worksheets[0]
    #修改数据
    for i in range(len(id)):
        worksheet.cell(line + i, 1, id[i])
        worksheet.cell(line + i, 2, url[i])
    #保存
    workbook.save(filename=file)
```

## 需要注意的几个重要问题

### 1.headers中设置User-agent可以模拟浏览器访问

```python
headerlist = [
        {'User-agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'},
        {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'},
        {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'},
        {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14'},
        {'User-agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)'},
        {'User-agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'},
        {'User-agent':'Opera/9.25 (Windows NT 5.1; U; en)'},
        {'User-agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
        {'User-agent':'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)'},
        {'User-agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12'},
        {'User-agent':'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'},
        {'User-agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7'},
        {'User-agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 '}
    ]
headers = random.choice(headerlist)
```

### 2.大部分网站都有反爬机制，短时间内连续大量向服务器发送的http请求，会被网站服务器认定为恶意攻击，将会屏蔽ip

解决方法可以是使用多个ip代理地址，随机使用代理的ip地址进行访问。ip地址需要自己去更换，以下ip地址应该已经失效。

```python
proxieslist = [
        {
            'http': 'http://106.110.156.183:4247'
        },
        {
            'http': 'http://60.184.97.235:4245'
        },

        {
            'http': 'http://114.96.218.79:4281'
        },
        {
            'http': 'http://36.6.68.102:4245'
        },
        {
            'http': 'http://115.207.17.37:4245'
        },
        {
            'http': 'http://114.239.106.70:4245'
        },
        {
            'http': 'http://183.166.7.38:4231'
        },
        {
            'http': 'http://115.198.59.150:4286'
        },
        {
            'http': 'http://61.188.26.16:4210'
        },
        {
            'http': 'http://117.70.35.33:4210'
        }
    ]
    proxies = random.choice(proxieslist)
```

但就算使用代理ip，如果访问速度过快依旧会被ip屏蔽。**所以需要设置时间间隔，不同的网站的时间间隔可能不同，一般来说可以设置一个2~5秒的时间间隔，这样的时间间隔一般来说是安全的。**

完整的代码

```python
# coding=utf-8
import random

import requests
from xlutils.copy import copy
import xlwt
import time
import openpyxl
import xlrd
from bs4 import BeautifulSoup

def getimgpath(movid, num):
    url = 'https://movie.douban.com/subject/' + movid + '/'
    proxieslist = [
        {
            'http': 'http://106.110.156.183:4247'
        },
        {
            'http': 'http://60.184.97.235:4245'
        },

        {
            'http': 'http://114.96.218.79:4281'
        },
        {
            'http': 'http://36.6.68.102:4245'
        },
        {
            'http': 'http://115.207.17.37:4245'
        },
        {
            'http': 'http://114.239.106.70:4245'
        },
        {
            'http': 'http://183.166.7.38:4231'
        },
        {
            'http': 'http://115.198.59.150:4286'
        },
        {
            'http': 'http://61.188.26.16:4210'
        },
        {
            'http': 'http://117.70.35.33:4210'
        }
    ]

    # proxy = random.choice(proxies)
    headerlist = [
        {'User-agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'},
        {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'},
        {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'},
        {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14'},
        {'User-agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)'},
        {'User-agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'},
        {'User-agent':'Opera/9.25 (Windows NT 5.1; U; en)'},
        {'User-agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
        {'User-agent':'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)'},
        {'User-agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12'},
        {'User-agent':'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'},
        {'User-agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7'},
        {'User-agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 '}
    ]
    headers = random.choice(headerlist)
    proxies = random.choice(proxieslist)
    res = requests.get(url, headers=headers， proxies=proxies)
    if(res.status_code == 200):
        ans = ''
        try:
            soup = BeautifulSoup(res.text, 'lxml')
            ans = soup.find(attrs={'id': 'mainpic'}).find('img').get('src')
        except BaseException:
            print('Error: ', num)
            return 'Error'
        else:
            print('(', num, '/', 28603, ')', '[ url:', ans, ']')
            return ans
    else:
        print('状态码：',res.status_code)
        return 'none'

def write_excel(file, line, id, url):
    #文件读取
    workbook = openpyxl.load_workbook(file)
    worksheet = workbook.worksheets[0]
    #修改数据
    for i in range(len(id)):
        worksheet.cell(line + i, 1, id[i])
        worksheet.cell(line + i, 2, url[i])
    #保存
    workbook.save(filename=file)

def read_excel(file, begin, n):
    wb = xlrd.open_workbook(filename=file)
    sheet1 = wb.sheet_by_index(0)
    rows = []
    for i in range(n):
        row = sheet1.row_values(begin + i)
        rows.append(row[0])
    return rows

#开始行数
beginline = 716
#一批次访问规模
n = 10
failnum = 0
#截止行数设置
while (beginline < 20000):
    # 读取n条id到idlist
    idlist = read_excel('testdb_MovieInfo.xlsx', beginline, n)
    # 爬取n条url到imglist
    imglist = []
    for i in range(n):
        img = getimgpath(idlist[i], beginline + i)
        if(img == 'none'):
            failnum += 1
            print('失败数：', failnum)
        imglist.append(img)
        time.sleep(2)
    write_excel('movurl.xlsx', beginline + 1, idlist, imglist)
    beginline += n
    print('Nowline_input: ',beginline)
```

## ip地址验证

http://httpbin.org/get向这个网站发送请求可以得到当前访问使用的ip地址。

```python
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
```

