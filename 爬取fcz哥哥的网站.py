from bs4 import BeautifulSoup
import requests
import jieba.analyse
import re
import collections
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import time
from googletrans import Translator
import json
import os


start_time = time.time()
translater = Translator()
# out = translater.translate("你好", dest='en', src='zh-CN').text
# print(out)
fake_header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                    'AppleWebKit/537.36 (KHTML, like Gecko)'
                    'Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39'
    }


def json_is_exist():
    '''检查当前目录下词频库是否存在'''
    now_list_dir = os.listdir()
    if 'eng_frequency.json' in now_list_dir and 'frequency.json' in now_list_dir:
        if input('是否需要更新数据y/n') == 'y':
            return False
        return True
    return False

def get_url_lists():
    # 爬取fczgg的网站并做云图
    url = 'https://18062706139fcz.github.io/learn-javas/handbook/hey.html'
    r = requests.get(url, headers=fake_header)
    # print(r.text)
    soup = BeautifulSoup(r.text, 'lxml')
    # 他所有的侧边栏都放在了sidebar-links 类当中
    sider = soup.find_all('a', class_ ='sidebar-link')
    # print(sider)
    # 所有的里面的子类中装有链接的都取出来 可以继续用soup 也可以用正则
    # 装有链接的侧边栏class中都有相同的字符串 sidebar-link
    # 数据量还是有点大，正则可能比较慢？
    # 最后十个是右边栏的 可以去掉([:-10])

    href_list = []
    for each in sider[:-10]:
        # print(each)
        # print()
        each = str(each)
        # 要先转化 否则为nonetype 这一步折磨了我十分钟
        compiler = re.compile(r'href="\S{3,50}"')
        match_list = compiler.findall(each)
        # print(match_lists)
        match_res = ''.join(match_list).replace('href="', 'https://18062706139fcz.github.io/').replace('"', '')
        # print(match_res)
        href_list.append(match_res)
    # print(href_list)
    # 获得所有侧边栏的网址
    return href_list


def href_list_to_frequency(href_list):
    words = ''
    for urls in href_list:
        r = requests.get(urls, headers=fake_header)
        soup = BeautifulSoup(r.text, 'lxml')
        all_text = soup.find_all('div', class_ = 'theme-reco-content content__default')
        # 所有的中文都在这个里面
        Chinese = re.compile( r'[\u4e00-\u9fa5]')
        all_chinese = Chinese.findall(str(all_text))
        words += ''.join(all_chinese)
    frequency = jieba.lcut(words)
    # 记得去掉停用词
    stop_ls = {'一个', '可以', '就是','什么', '我们', '没有', '这个', '两个'} # 用哈希结构  快一点
    # for i in frequency:
    #     if len(i) == 1 or i in stop_ls:
    #         frequency.remove(i)
    # 在字典里面去重不更快嘛
    frequency = collections.Counter(frequency)
    for i in frequency.keys():
        if len(i) == 1 or i in stop_ls:
            frequency[i] = -1
    # print(frequency.most_common(100))
    frequency = dict(frequency.most_common(100))

    # 添加一个英文版本的字典
    eng_frequency = {}
    for k, v in frequency.items():
        # print(k, v)
        eng_frequency[translater.translate(k, dest='en', src='zh-CN').text] = v
    # print(eng_frequency)
    with open("frequency.json", "w") as f:
        f.write(json.dumps(frequency, ensure_ascii=True, indent=4, separators=(',', ':')))

    with open("eng_frequency.json", "w") as f:
        f.write(json.dumps(eng_frequency, ensure_ascii=False, indent=4, separators=(',', ':')))
    return frequency, eng_frequency


def to_wordcloud(frequency, eng_frequency):
    # 词云部分
    mask = np.array(Image.open('fcz.jpg'))
    # 用数组传入背景
    wc = WordCloud(
            font_path="C:\Windows\Fonts\STHUPO.TTF", # 这里要注意啦
            max_words=100,
            width=2000,
            height=1200,
            mask=mask,
            background_color='white',
        )
    word_cloud = wc.generate_from_frequencies(frequency)
    # 图一
    word_cloud.to_file("wordcloud1.jpg")
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()


    #图二
    word_cloud = wc.generate_from_frequencies(eng_frequency)
    word_cloud.to_file("wordcloud_new.jpg")
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()

    
if __name__ == '__main__':
    if not json_is_exist():
        # 不存在或需要更新
        href_list = get_url_lists()
        frequency, eng_frequency = href_list_to_frequency(href_list)
    else:
        # 存在且不需要更新
        with open("eng_frequency.json",'r') as f:
            eng_frequency = json.load(f)
        with open("frequency.json", "r") as f:
            frequency = json.load(f)
    # print(frequency, eng_frequency)
    
    to_wordcloud(frequency, eng_frequency)
    print(f'run time{time.time()-start_time:.3f}s')