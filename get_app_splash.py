import requests,os,json,time

if os.path.isdir('app_splash')==False:
    os.makedirs('app_splash')

api='http://app.bilibili.com/x/v2/splash/brand/list?appkey=1d8b6e7d45233436&ts=0&sign=78a89e153cd6231a4a4d55013aa063ce'

req=requests.get(api)

json_req=req.json()

result={}
result['lastSync']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
img_list=[]
for img in json_req['data']['list']:
    img_id,img_url=img['id'],img['thumb']
    img_format=img_url.split('.')[-1]
    img_list.append({'id':img_id,'url':f'{str(img_id)}.{img_format}'})
    imgreq=requests.get(img_url)
    try:
        with open(f'app_splash/{str(img_id)}.{img_format}','wb+') as image:
            print(f'start download:{img_url}')
            image.write(imgreq.content)
    except:
        print(f'{img_url} 下载出错。')

result['list']=img_list
with open('app_splash/images.json','w+') as fp:
    json.dump(result,fp)
