import requests
import re
import time
import os

# url = "http://s1.dwstatic.com/group1/M00/CF/D3/081427a594b2bed8d104c4a510426464.jpg"
# response = requests.get(url)
# img_data = response.content
# print(img_data)
# #持久化
# with open('meinv.jpg','wb') as f:
#     f.write(img_data)

# class spider
def strip(path):
    """
    :param path: 需要清晰的文件夹名称
    :return: 清洗掉windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[? \\*|“<>:/]', '', str(path))
    return path
def download(url):
    try:
        return requests.get(url)
    except Exception as e:
        print(e,'下载错误')

# id
def get_img_item_ids(html):
    img_item_ids = re.findall(r'http://tu.duowan\.com/gallery/(\d+)\.html', html)
    if img_item_ids:
        return set (img_item_ids)


def save_img_by_info(img_item_info):
    item_title = img_item_info['gallery_title']
    item_title = strip(item_title)
    imgs_info = img_item_info['picInfo']
    # print(item_title)
    # exit()
    # 新建文件夹
    # 必须有not 然后否则文件下载到本地文件夹就会出错  如果没有not会报错 因为没有这个文件夹
    if not os.path.exists(item_title):    #如果没有文件 则创建
        os.makedirs(item_title)
    for img_info in imgs_info:
        title = img_info['title']
        title = strip(title)
        url = img_info['url']
        img_file_name = "%s/%s.%s" % (item_title, title, url.split('.')[-1])
        if not os.path.exists(img_file_name):
            print(url)
            img_data = download(url)
            if img_data:
                with open(img_file_name, 'wb') as f:
                    f.write(img_data.content)
def spider(first_url):
    html_response = download(first_url)
    if html_response:
        # 字符集编码更改
        html_response.encoding = 'utf-8'
        html = html_response.text
        # print(html)
        # exit()
        img_item_ids = get_img_item_ids(html)
        # 获取a标签
        print(img_item_ids)
        # exit()
        if img_item_ids:
            for img_item_id in img_item_ids:
                img_item_info_url = \
                    "http://tu.duowan.com/index.php?r=show/getByGallery/&gid=%s&_=%s" % \
                    (img_item_id, int(time.time()*1000))
                # 下载
                img_item_info_response = download(img_item_info_url)
                if img_item_info_response:
                    img_item_info = img_item_info_response.json()
                    # print(type(img_item_info),img_item_info)
                    save_img_by_info(img_item_info)
if __name__ == '__main__':
    first_url = "http://tu.duowan.com/m/meinv"
    spider(first_url)