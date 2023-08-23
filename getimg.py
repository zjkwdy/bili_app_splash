import math
import os
import sys
import threading
import time
from datetime import datetime

import requests


def getimglist(uid, SESSDATA=None, page=0, page_size=45):
    doc_list_api = 'https://api.bilibili.com/x/dynamic/feed/draw/doc_list'
    upload_count_api = 'https://api.bilibili.com/x/dynamic/feed/draw/upload_count'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74'
    }
    result = {}
    req = requests.get(upload_count_api, params={'uid': uid}, cookies=None, headers=headers)
    result['imgcount'] = req.json()['data']['all_count']
    params = {
        'biz': 'all',
        'uid': uid,
        'page_num': page,
        'page_size': page_size,
    }
    cookies = {
        'SESSDATA': SESSDATA
    }
    req = requests.get(doc_list_api, params=params, cookies=cookies, headers=headers)
    grouplist = []
    result['pagesize'] = page_size
    for image in req.json()['data']['items']:
        imageresult = {}
        srcgroup = []
        for pic in image['pictures']:
            srcgroup.append(pic['img_src'])
        # 将时间戳转换为 datetime 对象
        dt_object = datetime.fromtimestamp(image['ctime'])
        # 将 datetime 对象格式化为指定的字符串格式
        imageresult['title'] = dt_object.strftime('%Y-%m-%d %H%M%S')
        imageresult['imgs'] = srcgroup
        grouplist.append(imageresult)

    result['images'] = grouplist
    return result


def saveimg(src, path):
    print('start download at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    req = requests.get(src)
    if os.path.isdir(path) == False:
        os.makedirs(path)
    with open(path + '/' + src.split('/')[-1], 'wb+') as fp:
        fp.write(req.content)
    with open('urls.txt', 'a') as fp:
        fp.write(src + '\n')
    print('end download at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(path, 'save', req.status_code)


# 壁纸娘uid,别看了
uid = 6823116
try:
    SESSDATA = sys.argv[1]
except IndexError:
    SESSDATA = None
page_size = 45
print('start Run at ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
img_list = getimglist(uid, SESSDATA)
img_num = float(img_list['imgcount'])
page_size = float(img_list['pagesize'])
page_nums = math.ceil(img_num / page_size)
print(f'page size:{page_size} img_num:{img_num} page_num:{page_nums}  ' + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                        time.localtime()))
for page in range(page_nums):
    if page == 0:
        for image in img_list['images']:
            title = "bizhiniang/" + image['title']
            print(title)
            for src in image['imgs']:
                print(src)
                threading.Thread(target=saveimg, args=(src, title)).start()
    else:
        img_list = getimglist(uid, SESSDATA, page)
        for image in img_list['images']:
            title = "bizhiniang/" + image['title']
            print(title)
            for src in image['imgs']:
                print(src)
                threading.Thread(target=saveimg, args=(src, title)).start()
    print(f'Now_Page:{page} Left_Pages:{page_nums - page} ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    time.sleep(20)

print('done')
