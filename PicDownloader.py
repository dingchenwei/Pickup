#-*- coding:utf-8 -*-
import re
import requests
from StringIO import StringIO
import cv2
import numpy as np
import os

def getPage(url, keyword, page_index):
    # for i in range(30,30*pages+30,30):
    params = {
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
              }
    result = requests.get(url, params=params)
        # print requests.get(url, params=i).json().get('data')
    return result

def downloadPic(url,keyword, pages):
    if(not os.path.exists('pictures/baidu/'+keyword)):
        os.system('mkdir pictures/baidu/'+keyword)
    f = open('pictures/baidu/'+keyword+'/urls.txt', 'w')
    i = 0
    print '找到关键词:'+keyword+'的图片，现在开始下载图片...'
    for page_index in range(30, 30*pages+30, 30):
        try:
            result = getPage(url, keyword, page_index)
        except reques.exceptions.ConnectionError:
            print keyword+"下载失败，请重新下载"
            break
        pic_url = re.findall('"thumbURL":"(.*?)",',result.text,re.S)
        print len(pic_url)
        if len(pic_url) == 0:
            print "#####done#####"
            break
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
                cv2.imwrite('pictures/baidu/'+keyword+'/'+keyword+str(i)+'.jpg', image)
                i+=1
    f.close()



if __name__ == '__main__':
    url = 'https://image.baidu.com/search/acjson'

    #keyword_list = ['女主播', '女孩', '女生', '女老师', '女运动员', '女清洁工', '女厨师', '女作家', '女工程师', '女缝纫工', '女教授', '女服务员', '女医生', '女演员', '女司机', '女老板', '女记者', '护士', '女教练', '女管理员', '女售货员', '女理发师', '保姆', '女警察']
    keyword_list = ['女缝纫工', '女教授', '女服务员', '女医生', '女演员', '女司机', '女老板', '女记者', '护士', '女教练', '女管理员', '女售货员', '女理发师', '保姆', '女警察']
    for word in keyword_list:
        ori_word = word
        downloadPic(url,ori_word, 30)
        word_zipai = '自拍'+ ori_word
        downloadPic(url, word_zipai, 30)
        word_changfa = ori_word + '长发'
        downloadPic(url, word_changfa, 30)
        word_duanfa = ori_word + '短发'
        downloadPic(url, word_duanfa, 30)


    keyword_list = ['男主播', '男孩', '男生', '男老师', '男运动员', '男清洁工', '男厨师', '男作家', '男工程师', '男教授', '男服务员', '男医生', '男演员', '男司机', '男记者', '男教练', '男管理员', '男售货员', '男警察']
    for word in keyword_list:
        ori_word = word
        downloadPic(url,ori_word, 30)
        word_zipai = '自拍'+ ori_word
        downloadPic(url, word_zipai, 30)
        word_changfa = ori_word + '长发'
        downloadPic(url, word_changfa, 30)
        word_duanfa = ori_word + '短发'
        downloadPic(url, word_duanfa, 30)
