import datetime
import re
import urllib.request as req
from bs4 import BeautifulSoup

import time

# url="https://udn.com/news/story/6656/4065517?from=udn-ch1_breaknews-1-0-news"
# request =req.Request(url, headers={
#     "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36"
# })
# with req.urlopen(url) as response:
#     data=response.read().decode("utf-8")
# root = BeautifulSoup(data, "html.parser")
# print(root.title.string)
# titles=root.find_all("div", class_ ="title")
# def homepage():
#     titles=root.find_all("h2")
#     for title in titles:
#         if title.a != None:
#             print("標題: " + title.a.string)
#     # print(type(titles))
#     print(len(titles))
from DateUtil import to_epoch, strtodate_yyyymmdd_ws, strtodate_yyyymmddhhmi_wd
from Model import LowiDoc

start_urls = ["https://udn.com/news/breaknews/1",  # 即時
              # "https://udn.com/news/cate/2/6638",   #要聞
              # "https://udn.com/news/cate/2/7227",   #運動
              # "https://udn.com/news/cate/2/7225",   #全球
              # "https://udn.com/news/cate/2/6639",   #社會
              ]
post_urls = []
lowidocs = []


def article(url):
    with req.urlopen(url) as response:
        data = response.read().decode("utf-8")
    root = BeautifulSoup(data, "html.parser")
    tags = root.find_all("div", id="story_tags")
    photos = root.find_all("img", {'title': True, 'src': re.compile('.*photo.*.')})
    title = root.select('.story_art_title')[0]
    contents = root.select('#story_body_content')
    post_time = root.select('#story_bady_info span')[0]
    author = root.select('#story_bady_info a')[0]
    test = root.select_one('#area_body.dl')
    # channel = root.select_one('#menu a')
    for tag in tags:
        # print("tag: " + tag.a.string)
        # s_tag = str(tag).strip('<div id="story_tags"><a href="/search/tagging/2/" rel="144129">')

        print(test.text)
        print('標題: ' + title.text)
        print('發布時間:' + post_time.text)
        print('記者:' + author.text)
        # print('分類: ' + channel.text)
        print("內文:")
        for content in contents:
            print(content.text.strip())
            # doc.drecontent = ''.join(s.string or "" for s in content.text.strip())

        print("網址: " + url)

        print("圖片:")
        for photo in photos:
            print(photo['src'])
        print("tag: " + tag.text)
        print()
        # print(type(tag.a.string))

        # doc = LowiDoc()
        # doc.drereference = url
        # doc.glbdis_linkurl = url
        # doc.dretitle = title.text
        # doc.dredate = to_epoch(strtodate_yyyymmddhhmi_wd(post_time.text))
        # # doc.glb_channel_lv1 = soup.select_one("a.active").string
        # # doc.glb_author = author.split(" ")[1] or author
        # doc.glb_posttype = "P"
        # doc.glb_maintopic = "主文"
        # # doc = finalize_lowidoc(doc, "NEWS", "新聞", "聯合新聞網", "ZH-TW")
        # # lowidocs.append(doc)


# homepage()


def extract_post_list(url):  # 此url為homepage
    # url = "https://udn.com/news/breaknews/1"

    with req.urlopen(url) as response:
        data = response.read().decode("utf-8")
    root = BeautifulSoup(data, "html.parser")

    a_tags = root.find_all("a")
    # print(a_tags)
    start_time = datetime.datetime.now()

    for a_tag in a_tags:
        # print(str(a_tag.get("href")))

        # print(re.search(".*/story/[0-9]*/[0-9]*.*", str(a_tag.get("href"))))
        if re.search(".*/news/story/[0-9]+/[0-9]+.*", str(a_tag.get("href"))):
            if str(a_tag.get("href")).find("https") == -1:
                post_urls.append("https://udn.com" + a_tag.get("href"))
            elif str(a_tag.get("href")).find("https") == 0:
                print("快訊!!", a_tag.get("href"))  # 無添加到post_url
                print()
            # print(a_tag.get("href").find("https"))
    uni_urls = set()
    for post_url in post_urls:
        if post_url not in uni_urls:
            uni_urls.add(post_url)
            try:
                article(post_url)
                # print("ggg")

            except Exception as err:
                print(err)
                print("Extracting Error : " + post_url)

    end_time = datetime.datetime.now()
    print()
    print("蒐集到的新聞數: " + str(len(post_urls)))
    print("Using %d secs" % (end_time - start_time).seconds)


def go():
    for url in start_urls:
        extract_post_list(url)


go()
