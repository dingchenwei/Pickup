#-*- coding:utf-8 -*-
import re
import requests
from StringIO import StringIO
import cv2
import numpy as np
import os
from requests.exceptions import *

proxies = {
    'https': 'socks5h://127.0.0.1:1080',
    'http': 'socks5h://127.0.0.1:1080'
}
headers = {
    'referer': 'https://www.google.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
def getPage(url, keyword, page_index):
    # for i in range(30,30*pages+30,30):
    keyword_bk = keyword.replace('_', ' ')
    params = {
        'ei': 'zywaWuedFoPa8QXV9IbYCA',
        'hl': 'zh-CN',
        'yv': 2,
        'tbm': 'isch',
        'q': keyword_bk,
        'vet': '10ahUKEwinwfyxntvXAhUDbbwKHVW6AYsQuT0IJCgB.zywaWuedFoPa8QXV9IbYCA.i',
        'ved': '0ahUKEwinwfyxntvXAhUDbbwKHVW6AYsQuT0IJCgB',
        'ijn': page_index/100,
        'start': page_index,
        'asearch': 'ichunk',
        'async': '_id:rg_s,_pms:s'
              }
    result = requests.get(url, headers=headers, proxies=proxies, params=params).json()[1][1]
    return result

def downloadPic(url, page_num):
    f = open('pictures/laifeng/urls.txt', 'w')
    i = 0
    for page_index in range(page_num):
        try:
            result = requests.get(url+str(page_index+1), timeout=100)
        except (ConnectionError, ChunkedEncodingError, BaseHTTPError, ContentDecodingError, HTTPError, Timeout, SSLError):
            print '没能成功获取page，请稍后重新下载'
            continue
        pic_url = re.findall('data-src="(.*?)"',result.text,re.S)
        print len(pic_url)
        if len(pic_url) == 0:
            print "#####done#####"
            break
        for each in pic_url:
            f.write(each+'\n')
            print '正在下载第'+str(i+1)+'张图片，图片地址:'+str(each)
            try:
                pic= requests.get(each, headers=headers, proxies=proxies, timeout=100, allow_redirects=False)
            except (ConnectionError, ChunkedEncodingError, BaseHTTPError, ContentDecodingError, HTTPError, Timeout, SSLError):
                print '【错误】当前图片无法下载'
                continue
            #resolve the problem of encode, make sure that chinese name could be store
            #fp = open(string.decode('utf-8').encode('cp936'),'wb')
            #fp.write(pic.content)
            #fp.close()
            image = cv2.imdecode(np.fromstring(pic.content, np.uint8), -1)
            if(image is None):
              continue
            image = cv2.resize(image, (320, 320))
            h = (image.shape)[0]
            w = (image.shape)[1]
            max_length = w if w > h else h

            if max_length >= 300:
                cv2.imwrite('pictures/laifeng/laifeng'+str(i)+'.jpg', image)
                i+=1
    f.close()



if __name__ == '__main__':

    # word = raw_input("Input key word: ")

    url_list = {'http://www.laifeng.com/center/1/1001?spm=a2h55.8996204.Search-left-menu.3!2~1~3~A&pageNo=': 11,
                'http://www.laifeng.com/center/1/1003?spm=a2h55.8996204.Search-left-menu.3!2~1~3!2~A&pageNo=': 6,
                'http://www.laifeng.com/center/1/1005?spm=a2h55.8996204.Search-left-menu.3!2~1~3!3~A&pageNo=': 10,
                'http://www.laifeng.com/center/1/1006?spm=a2h55.8996204.Search-left-menu.3!2~1~3!4~A&pageNo=': 17,
                'http://www.laifeng.com/center/1/1007?spm=a2h55.8996204.Search-left-menu.3!2~1~3!5~A&pageNo=': 4,
                'http://www.laifeng.com/center/1/1008?spm=a2h55.8996204.Search-left-menu.3!2~1~3!6~A&pageNo=': 3,
                'http://www.laifeng.com/center/1/1004?spm=a2h55.8996204.Search-left-menu.3!2~1~3!7~A&pageNo=': 7
                }
    for (key, value) in url_list.items():
        downloadPic(key, value)





