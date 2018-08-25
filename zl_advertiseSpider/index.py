#-*- coding: utf-8 -*-
import re
import csv
import requests
import searchProxy
import random
import brotli
import json
import time
import math
from tqdm import tqdm
from urllib.parse import urlencode
from requests.exceptions import RequestException

citys ={"691":"南昌","695":"新余"}
proxies = []
def get_one_page(city,start):
    '''
    获取网页html内容并返回
    '''
    paras = {
        'start':start,
        'pageSize': '60',
        'cityId': city,
        'workExperience': '-1',
        'education': '-1',
        'companyType': '-1',
        'employmentType': '-1',
        'jobWelfareTag': '-1',
        'kw': '江西',
        'kt': '3',
        'lastUrlQuery': '{"jl": "691", "kw": "江西", "kt": "3"}'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Host': 'fe-api.zhaopin.com',
        'Referer': 'https://sou.zhaopin.com/?p=2&jl=691&kw=%E6%B1%9F%E8%A5%BF&kt=3',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Origin':'https://sou.zhaopin.com'
    }

    url = 'https://fe-api.zhaopin.com/c/i/sou?' + urlencode(paras)
    try:
        proxy = random.choice(proxies)
        # 获取网页内容，返回html数据
        response = requests.get(url, headers=headers,proxies=proxy)
        # 通过状态码判断是否获取成功，注意content-encoding的格式，这里是br格式，然后转成utf-8
        if response.status_code == 200:
            data = brotli.decompress(response.content).decode('utf-8')
            return data
        return None
    except RequestException as e:
        return None

def parse_one_page(jsonStr):
    hjson = json.loads(jsonStr)
    result = hjson["data"]["results"]
    for item in result:
        jobName = item["jobName"]
        companyName = item["company"]["name"]
        companySize = item["company"]["size"]["name"]
        companyType = item["company"]["type"]["name"]
        salary = item["salary"]
        city = item["city"]["display"]
        workingExp = item["workingExp"]["name"]
        eduLevel = item["eduLevel"]["name"]
        welfare = item["welfare"]
        positionURL = item["positionURL"]
        yield {
            'jobName':jobName,
            'companyName':companyName,
            'companySize':companySize,
            'companyType':companyType,
            'salary':salary,
            'city':city,
            'workingExp':workingExp,
            'eduLevel':eduLevel,
            'welfare':welfare,
            'positionURL': positionURL
        }

def parse_one_page_count(jsonStr):
    hjson = json.loads(jsonStr)
    number = hjson["data"]["numFound"];
    return number


def write_csv_file(path, headers, rows):
    '''
    将表头和行写入csv文件
    '''
    # 加入encoding防止中文写入报错
    # newline参数防止每写入一行都多一个空行
    with open(path, 'a', encoding='gb18030', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)

def write_csv_headers(path, headers):
    '''
    写入表头
    '''
    with open(path, 'a', encoding='gb18030', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()

def write_csv_rows(path, headers, rows):
    '''
    写入行
    '''
    with open(path, 'a', encoding='gb18030', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writerows(rows)

def aaa(city, pages):
    '''
    主函数
    '''
    filename = '智联招聘_'+ citys[city] + '.csv';
    # headers = ['职位名', '公司名','公司规模','公司性质', '工资','城市','经验要求','学历要求','福利','链接']
    headers = ['jobName', 'companyName','companySize','companyType', 'salary','city','workingExp','eduLevel','welfare','positionURL']
    write_csv_headers(filename, headers)
    # countJson = get_one_page(city,0)
    # totalNumber = parse_one_page_count(countJson)
    # totalPage = math.ceil(totalNumber / 60)
    # time.sleep(30)
    for i in tqdm(range(pages)):
        try:
            '''
            获取该页中所有职位信息，写入csv文件
            '''
            jobs = []
            jsonData = get_one_page(city,i*60)
            items = parse_one_page(jsonData)
            for item in items:
                jobs.append(item)
            write_csv_rows(filename, headers, jobs)
            time.sleep(30)
        except Exception as err:
            break

def testProxys(proxys):
    """ Test the proxys. """
    validProxys = []
    for proxy in proxys:
        try:
            validProxys.append({"http":proxy})
        except Exception as e:
            print("%s\t%s" % (proxy, "invalid"))
            continue

    return validProxys

if __name__ == '__main__':
    allProxies = searchProxy.getProxys()
    proxies = testProxys(allProxies)
    aaa('691', 10)
    aaa('695', 10)