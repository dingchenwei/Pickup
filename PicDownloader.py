#-*- coding:utf-8 -*-
import re
import requests
from StringIO import StringIO
import cv2
import numpy as np
import os
from requests.exceptions import *
import multiprocessing
import random
def getPage(url, keyword, page_index):
    # for i in range(30,30*pages+30,30):
    keyword = keyword.replace('_', ' ')
    # url = url+'q='+keyword+'#'+keyword+'||1|100|'+str(page_index)+'|2||||'
    # print url
    num = random.randint(1,99)
    headers = {
        # 'referer': 'https://www.google.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    params = {
        'key': keyword,
        'pageSize':100,
        'pageNum':page_index,
        'imageType':2,
        'sortType':1,
        'callback':'searchresult',
        '_':num
              }
    result = requests.get(url, params=params, headers=headers)
        # print requests.get(url, params=i).json().get('data')
    return result

def downloadPic(url,keyword, pages):
    if(not os.path.exists('pictures/quanjing/'+keyword)):
        os.system('mkdir pictures/quanjing/'+keyword)
    f = open('pictures/quanjing/'+keyword+'/urls.txt', 'w')
    i = 0
    print '找到关键词:'+keyword+'的图片，现在开始下载图片...'
    for page_index in range(1, pages+1, 1):
        try:
            result = getPage(url, keyword, page_index)
        except (ConnectionError, ChunkedEncodingError, BaseHTTPError,
                ContentDecodingError, HTTPError, Timeout, SSLError,
                MissingSchema, TooManyRedirects, RequestException,
                InvalidSchema, InvalidURL, URLRequired, ProxyError):
            print keyword+"下载失败，请重新下载"
            break
        pic_url = re.findall('"imgurl":"(.*?)",',result.text,re.S)
        # print result.text
        print len(pic_url)
        if len(pic_url) == 0:
            print "#####done#####"
            break
        for each in pic_url:
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
                cv2.imwrite('pictures/quanjing/'+keyword+'/'+keyword+'_'+str(i)+'.jpg', image)
                i+=1
    f.close()



if __name__ == '__main__':
    url = 'http://search.quanjing.com/search?'
    pool = multiprocessing.Pool(processes=12)
    keyword_list = ['自拍_双人', '双人', '自拍_三人', '三人', '家庭照', '家庭_自拍', '一家三口', '一家三口_自拍', '情侣', '情侣_自拍', '亲子_自拍', '亲子']
    for keyword in keyword_list:
        # downloadPic(url, keyword, 1000)
        pool.apply_async(downloadPic, (url, keyword, 1000))
    pool.close()
    pool.join()
    # keyword_list = ['女主播', '女孩', '女生', '女老师', '女运动员', '女清洁工', '女教授', '女服务员', '女医生', '女演员', '女明星']
    # # keyword_list = ['1', '2', '3', '4', '5', '6', '7']
    # pool = multiprocessing.Pool(processes=50)
    # for word in keyword_list:
    #     ori_word = word
    #     #downloadPic(url,ori_word, 30)
    #     word_zipai = '自拍_'+ ori_word
    #     pool.apply_async(downloadPic, (url, word_zipai, 1000,))
    #     # p = multiprocessing.Process(target=downloadPic, args=(url, word_zipai, 1000,))
    #     # p.start()
    #     # p.join()
    #     # downloadPic(url, ori_word, 1000)
    #     word_changfa = '自拍_'+ori_word + '_长发'
    #     pool.apply_async(downloadPic, (url, word_changfa, 1000,))
    #     # p = multiprocessing.Process(target=downloadPic, args=(url, word_changfa, 1000,))
    #     # p.start()
    #     # p.join()
    #     # downloadPic(url, word_changfa, 1000)
    #     word_duanfa = '自拍_'+ori_word + '_短发'
    #     pool.apply_async(downloadPic, (url, word_duanfa, 1000,))
    #     # p = multiprocessing.Process(target=downloadPic, args=(url, word_duanfa, 1000,))
    #     # p.start()
    #     # p.join()
    #     # downloadPic(url, word_duanfa, 1000)
    #     word_zhongfa = '自拍_' + ori_word + '_中发'
    #     pool.apply_async(downloadPic, (url, word_zhongfa, 1000,))
    #     # p = multiprocessing.Process(target=downloadPic, args=(url, word_zhongfa, 1000,))
    #     # p.start()
    #     # p.join()
    #     # downloadPic(url, word_duanfa, 1000)
    # pool.close()
    # pool.join()
    # #
    # #
    # for i in range(200):
    #     url_tmp = url+str(i+1)
    #     pool.apply_async(url_tmp, 1000)
    # pool.close()
    # pool.join()