# coding=utf-8

import os
import sys
import re
import urllib
import urllib.request

URL_REG = re.compile(r'(http://[^/\\]+)', re.I)
IMG_REG = re.compile(r'<img[^>]*?src=([\'"])([^\1]*?)\1', re.I)
#<iframe width="100%" height="495" src="https://yun.qf-dalian.com/m3u8/index.php?url=https://video.letv-cdn.com/20180219/TJJG8I3k/index.m3u8" frameborder="0" border="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>
QIUXIA_MEDIA_REG = re.compile(r'<iframe[^>]*?src=([\'"])([^\1]*?)\1', re.I)
JUMP_URL_REG = re.compile(r'<a[^>]*?href=([\'"])([^\1]*?)\1', re.I)

count = 0


def download(dir, url):
    '''''下载网页中的图片

    dir 保存到本地的路径
    url 网页url
www.iplaypy.com
    '''
    global URL_REG, IMG_REG, count

    m = URL_REG.match(url)
    if not m:
        print('[Error]Invalid URL: ', url)
        return
    host = m.group(1)

    if not os.path.isdir(dir):
        os.mkdir(dir)

        # 获取html,提取图片url,url大小写会导致404
    html = urllib.urlopen(url).read()
    imgs = [item[1] for item in IMG_REG.findall(html)]
    f = lambda path: path if path.startswith('http://') else \
        host + path if path.startswith('/') else url + '/' + path
    imgs = list(set(map(f, imgs)))
    size = len(imgs)
    count += size
    print('[Info]Find %d images.').format(size)

    # 下载图片
    for idx, img in enumerate(imgs):
        name = img.split('/')[-1]
        path = os.path.join(dir, name)
        try:
            print('[Info]Download(%d): %s').format(idx + 1, img)
            urllib.urlretrieve(img, path)
        except:
            print("[Error]Cant't download(%d): %s").format(idx + 1, img)


urlSet = {1, 2}


def getUrl(dir, baseUrl):
    m = URL_REG.match(baseUrl)
    if not m:
        print('[Error]Invalid URL: ', baseUrl)
        return
    host = m.group(1)

    if not os.path.isdir(dir):
        os.mkdir(dir)

        # 获取html,提取图片url,url大小写会导致404
    html = urllib.urlopen(baseUrl).read()
    jumpurl = [item[1] for item in JUMP_URL_REG.findall(html)]
    f = lambda path: path if path.startswith('http://') or path.startswith("https://") \
        else "" \
        if path.startswith("/#") or path.startswith("/javascript") or path.startswith("javascript") or path.startswith(
        "#") \
        else host + path \
        if path.startswith('/') \
        else baseUrl + '/' + path

    download(dir, baseUrl)

    jumpurls = list(set(map(f, jumpurl)))
    print('[Info]jump url size %d .' % len(jumpurls))
    # 跳转
    for idx, img in enumerate(jumpurls):
        if (img in urlSet):
            continue
        print("[info] jump url(%d):%s").format(idx + 1, img)
        urlSet.add(img)
        getUrl(dir, img)


    # def main():
    #     if len(sys.argv) != 3:
    #         print 'Invalid argument count.'
    #         return
    #     dir, url = sys.argv[1:]
    #     download(dir, url)


    # if __name__ == '__main__':
    #     getUrl('D:\\Imgs', 'http://www.zhlzw.com/sj/List_1967.html')
    #     print "一共download %d 张图片" % count
    # download('D:\\Imgs', 'http://www.4493.com/motemeinv/21606/1.htm')
    # main()


import os
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"}

def do_load_media(url, path):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.3.2.1000 Chrome/30.0.1599.101 Safari/537.36"}
        pre_content_length = 0
        # 循环接收视频数据
        while True:
            # 若文件已经存在，则断点续传，设置接收来需接收数据的位置
            if os.path.exists(path):
                headers['Range'] = 'bytes=%d-' % os.path.getsize(path)
            res = requests.get(url, stream=True, headers=headers)

            content_length = int(res.headers['content-length'])
            # 若当前报文长度小于前次报文长度，或者已接收文件等于当前报文长度，则可以认为视频接收完成
            if content_length < pre_content_length or (
                        os.path.exists(path) and os.path.getsize(path) == content_length):
                break
            pre_content_length = content_length

            # 写入收到的视频数据
            with open(path, 'ab') as file:
                file.write(res.content)
                file.flush()
                print('receive data，file size : %d   total size:%d' % (os.path.getsize(path), content_length))
    except Exception as e:
        print(e)


def load_media():
    url = 'http://127.0.0.1:8080/a.mp4'
    path = r'E:/test.mp4'
    do_load_media(url, path)
    pass


def main():
    load_media()
    pass


def getQUrl(dir, baseUrl):
    m = URL_REG.match(baseUrl)
    if not m:
        print('[Error]Invalid URL: ', baseUrl)
        return
    host = m.group(1)

    # if not os.path.isdir(dir):
    #     os.mkdir(dir)

        # 获取html,提取图片url,url大小写会导致404
    req=urllib.request.Request(baseUrl)
    req.add_header("User-Agent","Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36")
    html = urllib.request.urlopen(req).read()
    print(html.decode("utf-8"))
    # jumpurl = [item[1] for item in JUMP_URL_REG.findall(html)]
    # print(jumpurl)

if __name__ == '__main__':
    getQUrl("","http://www.qiuxia64.com/videos/22348/play.html?22348-1-1")
    # getQUrl("","http://www.baidu.com")
    # main()
