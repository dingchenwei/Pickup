#-*- coding:utf-8 -*-
import re
import requests
from StringIO import StringIO
import cv2
import numpy as np
import os

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

def downloadPic(url,keyword, pages):
    if(not os.path.exists('pictures/google/'+keyword)):
        os.system('mkdir pictures/google/'+keyword)
    f = open('pictures/google/'+keyword+'/urls.txt', 'w')
    i = 0
    print '找到关键词:'+keyword+'的图片，现在开始下载图片...'
    for page_index in range(100, 100*pages+100, 100):
        result = getPage(url, keyword, page_index)
        pic_url = re.findall('"ou":"(.*?)",',result,re.S)
        print len(pic_url)
        if len(pic_url) == 0:
            print "#####done#####"
            break
        for each in pic_url:
            f.write(each+'\n')
            print '正在下载第'+str(i+1)+'张图片，图片地址:'+str(each)
            try:
                pic= requests.get(each, headers=headers, proxies=proxies, timeout=100, allow_redirects=False)
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
                cv2.imwrite('pictures/google/'+keyword+'/'+keyword+str(i)+'.jpg', image)
                i+=1
    f.close()



if __name__ == '__main__':

    # word = raw_input("Input key word: ")

    url = 'https://www.google.com/search'

    # keyword_list = ['girl', 'girl_student', 'female_teacher', 'sportswoman', 'cleaning_woman', 'woman_cook',
    #                 'woman_writer', 'female_engineers', 'seamstress', 'female_professor', 'waitress', 'woman_doctor',
    #                 'doctress', 'actress', 'women_driver', 'hostess', 'newspaper_woman', 'nurse', 'female_coach',
    #                 'female_administrator', 'saleswoman', 'womam_barber', 'baby-sitter', 'policewoman']
    # # url = 'https://image.baidu.com/search/acjson'
    # for word in keyword_list:
    #     ori_word = word
    #     downloadPic(url,ori_word, 1000)
    #     word_selfie = 'selfie_'+ori_word
    #     downloadPic(url, word_selfie, 1000)
    #     word_long_hair = ori_word+'_long_hair'
    #     downloadPic(url, word_long_hair, 1000)
    #     word_short_hair = ori_word+'_short_hair'
    #     downloadPic(url, word_short_hair, 1000)

    # keyword_list = ['boy', 'boy_student', 'male_teacher', 'sportsman', 'man_writer', 'male_engineers', 'male_professor', 'waiter', 'man_doctor', 'actor', 'man_driver', 'newspaper_man', 'male_coach', 'salesman', 'policeman']
    # # url = 'https://image.baidu.com/search/acjson'
    # for word in keyword_list:
    #     ori_word = word
    #     downloadPic(url, ori_word, 1000)
    #     word_selfie = 'selfie_' + ori_word
    #     downloadPic(url, word_selfie, 1000)
    #     word_long_hair = ori_word + '_long_hair'
    #     downloadPic(url, word_long_hair, 1000)
    #     word_short_hair = ori_word + '_short_hair'
    #     downloadPic(url, word_short_hair, 1000)


    keyword_list = ['长发_自拍_男', '中发_自拍_男', '短发_自拍_男', '长发_自拍_女', '中发_自拍_女', '短发_自拍_女']
    # url = 'https://image.baidu.com/search/acjson'
    for word in keyword_list:
        ori_word = word
        downloadPic(url, ori_word, 1000)






