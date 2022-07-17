from lib2to3.pgen2 import driver
from selenium import webdriver
from bs4 import BeautifulSoup
import re 
import pyautogui as auto
import webbrowser


class Spider:


    def __init__(self) -> None:
        """初始化"""
        self.driver = webdriver.Edge(r'./msedgedriver.exe')
        self.driver.implicitly_wait(10)
        self.driver.minimize_window()
        self.keyword = auto.prompt(text='请输入关键词', title='元搜索引擎 by L1_Sta2', default='哈哈哈')
        self.baidu = 'https://www.baidu.com/s?wd=' + self.keyword + '&pn='
        self.bing = 'https://cn.bing.com/search?q=' + self.keyword + '&first='


    def html_start(self):
        with open(r'new.html', 'w', encoding='utf-8') as file:
            file.write("""<!DOCTYPE html
            <head>
                <meta charset="utf-8">
                <style type="text/css">
                    div{s
                            height:4200px;
                            width:1000px;
                            background-color: #dea46b;
                            text-align: center;
                            line-height: 30px;
                            margin: auto;
                        }
                </style>
            </head>
            <body>
                <div class="box3">""")
    
    def html_end(self):
        with open(r'new.html', 'a', encoding='utf-8') as file:
            file.write(f'</div>\n<title>{self.keyword}的搜索结果</title>\n</body>\n</html>')

    
    def baidu_res(self):
        text = ''
        for page in range(0, 60, 10):
            if page == 0:
                page = '00'
            print(f'当前是百度page{page}')
            baidu = self.baidu + str(page)
            self.driver.get(baidu)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            text += "".join(map(str, soup.find_all("h3")))
        href_ls = re.findall(r'href=.{5,200}</a>', text)
        for i in range(len(href_ls)):
            href_ls[i] = '<a ' + href_ls[i] + '\n<br>\n'
        with open(r'new.html', 'a', encoding='utf-8') as file:
            file.write('<h1>以下为百度搜索</h1>')
            file.writelines(href_ls)

    
    def bing_res(self):
        text = ''
        for page in range(1, 6):
            print(f'当前是必应page{page}')
            page = str(page) + '1'
            bing = self.bing + (page)
            self.driver.get(bing)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            text += "".join(map(str, soup.find_all("h2")))
        href_ls = re.findall(r'href=.{5,200}</a>', text)
        for i in range(len(href_ls)):
            href_ls[i] = '<a ' + href_ls[i] + '\n<br>\n'
        with open(r'new.html', 'a', encoding='utf-8') as file:
            file.write('<h1>以下为必应搜索</h1>')
            file.writelines(href_ls)
        
    
    def quit(self):
        self.driver.quit()

    
    def show_html(self):
        self.quit()
        webbrowser.open_new_tab(r'.\new.html')


if __name__ == '__main__':
    S = Spider()
    S.html_start()
    S.baidu_res()
    S.bing_res()
    S.html_end()
    S.show_html()