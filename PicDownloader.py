#-*- coding:utf-8 -*-
import re
import requests
from StringIO import StringIO
import cv2
import numpy as np
import os
from requests.exceptions import *
import multiprocessing
import json
def getPage(url, keyword, page_index, person_num, sex):
    # for i in range(30,30*pages+30,30):
    keyword = keyword.replace('_', ' ')
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    params = {
        'limit':50,
        'line':page_index
              }
    payload = json.dumps({"keyword":keyword,"color":"0","category_id":"","line":"2550","type":"6","image_url":"","dp_search_sort":"","dp_search_orientation":"","dp_search_editorial":"","dp_search_race":"","dp_search_quantity":person_num,"dp_search_gender":sex,"dp_search_age":"","dp_search_color":""})
    result = requests.post(url, params=params, data=payload, headers=headers)
        # print requests.get(url, params=i).json().get('data')
    return result

def downloadPic(url,keyword, pages, person_num, sex=""):
    if(not os.path.exists('pictures/paixin/'+keyword+'_'+str(person_num)+sex+str(pages))):
        os.system('mkdir pictures/paixin/'+keyword+'_'+str(person_num)+sex+str(pages))
    f = open('pictures/paixin/'+keyword+'_'+str(person_num)+sex+str(pages)+'/urls.txt', 'w')
    i = 0
    print '找到关键词:'+keyword+'的图片，现在开始下载图片...'
    for page_index in range(pages-10000+50, pages+50, 50):
        try:
            result = getPage(url, keyword, page_index, person_num, sex)
        except (ConnectionError, ChunkedEncodingError, BaseHTTPError,
                ContentDecodingError, HTTPError, Timeout, SSLError,
                MissingSchema, TooManyRedirects, RequestException,
                InvalidSchema, InvalidURL, URLRequired, ProxyError):
            print keyword+"下载失败，请重新下载"
            break
        pic_url = re.findall('"image":"(.*?)",',result.text,re.S)
        print len(pic_url)
        if len(pic_url) == 0:
            print "#####done#####"
            break
        for each in pic_url:
            # each.replace('\\', '')
            each = each.encode('utf-8')
            each = each.replace('\\', '')
            f.write(each+'\n')
            print '正在下载第'+str(i+1)+'张图片，图片地址:'+str(each)
            try:
                pic= requests.get(each, timeout=100)
            except (ConnectionError, ChunkedEncodingError, BaseHTTPError,
                ContentDecodingError, HTTPError, Timeout, SSLError,
                MissingSchema, TooManyRedirects, RequestException,
                    InvalidSchema, InvalidURL, URLRequired, ProxyError):
                print '【错误】当前图片无法下载'
                continue
            #resolve the problem of encode, make sure that chinese name could be store
            #fp = open(string.decode('utf-8').encode('cp936'),'wb')
            #fp.write(pic.content)
            #fp.close()
            image = cv2.imdecode(np.fromstring(pic.content, np.uint8), -1)
            if(image is None):
              continue
            h = (image.shape)[0]
            w = (image.shape)[1]
            max_length = w if w > h else h
            if max_length >= 300:
                cv2.imwrite('pictures/paixin/'+keyword+'_'+str(person_num)+sex+str(pages)+'/'+keyword+'_'+str(i)+'.jpg', image)
                i+=1
    f.close()



if __name__ == '__main__':
    url = 'http://api.paixin.com/dp_media/search_list?'

    keyword_list = ['自拍']
    # downloadPic(url, keyword_list[0], 10000, 1, "male")
    pool = multiprocessing.Pool(processes=40)
    for word in keyword_list:
        for index in range(10000, 110000, 10000):
            pool.apply_async(downloadPic, (url, word, index, 2,))
    for word in keyword_list:
        for index in range(10000, 110000, 10000):
            pool.apply_async(downloadPic, (url, word, index, 3,))
    for word in keyword_list:
        for index in range(10000, 110000, 10000):
            pool.apply_async(downloadPic, (url, word, index, 1, "male",))##male
            pool.apply_async(downloadPic, (url, word, index, 1, "female",))##female



    pool.close()
    pool.join()