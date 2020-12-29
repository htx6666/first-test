import pyquery as pq,requests
import os,re,threading,time
#设置请求头
headers={
    'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

#第一次爬取网页，获取要下载的内容
def get_html(url):
    doc = pq.PyQuery(url=url,headers=headers,encoding='utf-8')
    urls=[]
    titles=[]
    print(' ')
    for i,x in  enumerate(doc('#main > div.main-nav.mt10 > div.sub-nav.cl > div.subnav-l.z a').items()):
        u='https://www.woyaogexing.com'+x.attr('href')
        urls.append(u)
        titles.append(x.text())
        print(x.text(),end=f'{i}')
    return urls,titles

#获取第二次要爬取的网页
def get_next_html(url,ti,p):
    doc = pq.PyQuery(url=url, headers=headers, encoding='utf-8')
    print(' ')
    for i, x in enumerate(doc('.pMain .img').items()):
        u = 'https://www.woyaogexing.com' + x.attr('href')
        t=re.sub(r'[\/？、／]+','_',x.attr('title'))
        path=os.path.join(p,t)
        if not os.path.exists(path):
            os.makedirs(path)

        t1=threading.Thread(target=get_end_html,args=(u,t,path))
        t1.start()
        t1.join()
    else:
        print(f'{ti} is ok!')

#获取最终图片链接
def get_end_html(url,t,p):
    # time.sleep(1)
    doc = pq.PyQuery(url=url, headers=headers, encoding='utf-8')
    for i, x in enumerate(doc('#main > div.contMain.mt10 > div.contLeft.z > div.contLeftA > ul > li > a > img').items()):
        u = 'https:' + x.attr('src')
        # time.sleep(1)
        t2=threading.Thread(target=download_pic,args=(u, t, p, i))
        t2.start()

#下载图片，保存到本地
def download_pic(u,t,p,i):
    with open(os.path.join(p,f'{t}_{i+1}.jpeg'),'wb')as fp:
        fp.write(requests.get(u,headers=headers).content)

#解析网页地址
def html_page(b,url,ti):
    for x in range(1,b+1):
        if x>1:
            u=url+f'index_{x}.html'
        else:
            u=url

        path = os.path.join(ti,f'Page{x}_{ti}')
        if not os.path.exists(path):
            os.makedirs(path)

        t3=threading.Thread(target=get_next_html,args=(u,ti,path))
        t3.start()
        t3.join()

#设置主函数，防止报错。缓慢下载。防止下载失败
if __name__ == '__main__':
    url='https://www.woyaogexing.com/touxiang/'
    ur,ti=get_html(url)
    a=int(input('\nshu ru :'))
    b=int(input('shu ru page:'))
    try:
        html_page(b, ur[a], ti[a])
    except:
        pass
