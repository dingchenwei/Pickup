#-*- coding:utf-8 -*-
import re
import requests
from StringIO import StringIO
import cv2
import numpy as np
import os

def getPage(url, keyword, page_index):
    params=[]
    # for i in range(30,30*pages+30,30):
    params.append({
                  'tn': 'resultjson_com',
                  'ipn': 'rj',
                  'ct': 201326592,
                  'is': '',
                  'fp': 'result',
                  'queryWord': keyword,
                  'cl': 2,
                  'lm': -1,
                  'ie': 'utf-8',
                  'oe': 'utf-8',
                  'adpicid': '',
                  'st': -1,
                  'z': '',
                  'ic': 0,
                  'word': keyword,
                  's': '',
                  'se': '',
                  'tab': '',
                  'width': '',
                  'height': '',
                  'face': 0,
                  'istype': 2,
                  'qc': '',
                  'nc': 1,
                  'fr': '',
                  'pn': page_index,
                  'rn': 30,
                  'gsm': '1e',
                  '1488942260214': ''
              })
    urls = []
    for i in params:
        # urls.append(requests.get(url,params=i).json().get('data'))
        urls.append(requests.get(url, params=i))
        # print requests.get(url, params=i).json().get('data')
    return urls

def downloadPic(url,keyword, pages):
    if(not os.path.exists('pictures/'+keyword)):
        os.system('mkdir pictures/'+keyword)
    f = open('pictures/'+keyword+'/urls.txt', 'w')
    i = 0
    print '找到关键词:'+keyword+'的图片，现在开始下载图片...'
    for page_index in range(30, 30*pages+30, 30):
        urls = getPage(url, keyword, page_index)
        for html in urls:
            pic_url = re.findall('"thumbURL":"(.*?)",',html.text,re.S)
            print len(pic_url)
            for each in pic_url:
                f.write(each+'\n')
                print '正在下载第'+str(i+1)+'张图片，图片地址:'+str(each)
                try:
                    pic= requests.get(each, timeout=100)
                except requests.exceptions.ConnectionError:
                    print '【错误】当前图片无法下载'
                    continue
                string = 'pictures/'+keyword+'_'+str(i) + '.jpg'
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
                    cv2.imwrite('pictures/'+keyword+'/'+keyword+str(i)+'.jpg', image)
                    i+=1
    f.close()



if __name__ == '__main__':
    word = raw_input("Input key word: ")
    url = 'https://image.baidu.com/search/acjson'
    downloadPic(url,word, 1000)

