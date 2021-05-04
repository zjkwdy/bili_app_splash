import requests,math,os,sys


def getimglist(uid,SESSDATA,page=0,page_size=45):
    api_url='http://api.vc.bilibili.com/link_draw/v1/doc/others'
    params={
        #全部图片
        'biz':0,
        'poster_uid':uid,
        'page_num':page,
        'page_size':page_size
    }
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74'
    }
    cookies={
        'SESSDATA':SESSDATA
    }
    req=requests.get(api_url,params=params,headers=headers,cookies=cookies)
    result={}
    grouplist=[]
    result['imgcount']=req.json()['data']['total_count']
    result['pagesize']=page_size
    for image in req.json()['data']['items']:
        imageresult={}
        srcgroup=[]
        for pic in image['pictures']:
            srcgroup.append(pic['img_src'])
        title=str(image['upload_time'].replace(':',''))
        imageresult['title']=title
        imageresult['imgs']=srcgroup
        grouplist.append(imageresult)

    result['images']=grouplist
    #print(result)
    return result

def saveimg(src,path):
    req=requests.get(src)
    if os.path.isdir(path)==False:
        os.makedirs(path)
    with open(path+'/'+src.split('/')[-1],'wb+') as fp:
        fp.write(req.content)
    with open('urls.txt','a') as fp:
        fp.write(src+'\n')
    print(path,'save',req.status_code)



#壁纸娘uid,别看了
uid=6823116
SESSDATA=sys.argv[1]
page_size=45

img_list=getimglist(uid,SESSDATA)
img_num=float(img_list['imgcount'])
page_size=float(img_list['pagesize'])
page_nums=math.ceil(img_num/page_size)

for page in range(page_nums):
    if page==0:
        for image in img_list['images']:
            title=image['title']
            print(title)
            for src in image['imgs']:
                print(src)
                saveimg(src,title)
    else:
        img_list=getimglist(uid,SESSDATA,page)
        for image in img_list['images']:
            title=image['title']
            print(title)
            for src in image['imgs']:
                print(src)
                saveimg(src,title)

print('done')
