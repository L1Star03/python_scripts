from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui as auto
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi
import cv2
import numpy as np
import seaborn as sns


class Spider():
    
    def __init__(self) -> None:
        self.url = 'https://www.nikon.com.cn/sc_CN/products/categories/f-mount.page?'
    
    @staticmethod
    def file_init():
        '''
        function:    create a json if not exist
        return type: bool
        '''
        if 'lens_json.json' in os.listdir():
            print('json文件已存在，如需要重新爬取请删除后重试')
            return True
        return False
        
    def main(self):
        '''
        function:    get values from Nikon.com and trans it into a dictionary
        return type: driver
        '''
        driver = self.driver = webdriver.Edge(r'./msedgedriver.exe')
        driver.implicitly_wait(5)  # 自适应等待
        driver.get(self.url)
        driver.maximize_window()
        def find_x(xpath):
            return driver.find_element(By.XPATH, xpath)
        
        dic_lens = {}
        max_index = 0 # 用于统计最长的列表长度 方便最后转换为表格
        for i in range(1, 88): # 这里只有87个镜头，以后也不会再出了，所以只用87次
            ls_index = []
            ls_value = []
            find_x('/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/div[3]/a').click() # 点击查看所有
            if i <= 84:
                lens_now = find_x(f'/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[{(i - 1)//12 + 1}]/div/div[{i % 12 if (i % 12 != 0) else 12}]/div/div[2]/a/h4')
                # /html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[7]/div[1]/div[12]/div/div[2]/a/h4
            else:
                lens_now = find_x(f'/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[7]/div[2]/div[{i % 12}]/div/div[2]/a/h4')
            name_lens = str(lens_now.get_attribute('textContent'))
            lens_now.click() # 进入镜头介绍页面
            try:
                JSGG = find_x(f'/html/body/div[1]/div[2]/ul/li[3]/a/p') # 进入技术规格界面
            except:
                JSGG = find_x(f'/html/body/div[1]/div[2]/ul/li[2]/a/p') # 有可能没有第三个
            if '技术规格' in JSGG.get_attribute('textContent'):
                JSGG.click()
                ls_describe = driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/div[2]/ul[1]/li')
                len_index = (len(ls_describe))
                for i in range(1, len_index + 1):
                    index = find_x(f'/html/body/div[1]/div[2]/div[2]/div[3]/div[2]/ul[1]/li[{i}]/ul/li[1]/p').get_attribute('textContent')
                    value = find_x(f'/html/body/div[1]/div[2]/div[2]/div[3]/div[2]/ul[1]/li[{i}]/ul/li[2]/p').get_attribute('textContent')
                    # if value != '\n' and index != '\n':
                    ls_index.append(index)
                    ls_value.append(value)
            else:
                find_x(f'/html/body/div[1]/div[2]/ul/li[2]/a/p').click() # 有些界面可能第二个才是技术规格
                ls_describe = driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/ul[1]/li[1]/ul/li')
                len_index = (len(ls_describe))
                for i in range(1, len_index + 1):
                    index = find_x(f'/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/ul[1]/li[{i}]/ul/li[1]/p').get_attribute('textContent')
                    value = find_x(f'/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/ul[1]/li[{i}]/ul/li[2]/p').get_attribute('textContent')
                    # if value != '\n' and index != '\n':
                    ls_index.append(index)
                    ls_value.append(value)
            self.max_index = max(max_index, len_index) # 获取最长的index
            dic_lens[name_lens] = [ls_index, ls_value]
            driver.get(self.url)
        # print(dic_lens.keys())
        with open('./lens_json.json', 'w+') as f:
            json.dump(dic_lens, f, ensure_ascii=False)

            
    def load_json(self)->dict:
        '''
        function:    load json to data
                     create xlsx if not exist
        return type: dict
        '''
        with open('./lens_json.json', 'r') as f:
            data = dict(json.load(f))
        return data

class Analyse():
    def __init__(self):
        self.data = data
        plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
        plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
        plt.style.use('ggplot')
        
    def data_to_excel(self):
        data = self.data
        index_ = [
            '名称',
            '画幅',
            '最小焦段',
            '最大焦段',
            '最大光圈',
            '结构',
            '对焦宁静波动马达',
            '滤镜尺寸',
            '减震',
            '重量',
        ]
        dic = [index_]
        for i in data.keys():
            ls = []
            names = i.split()
            # ls = [data[i][1][x] for x in [y for y in range(len(data[i][0])) for z in index_ if z in data[i][0][y]]]
            ls.append(i)
            if '增距' in i:
                ls.extend([None]*9)
                continue
            ls.append("APS-C画幅") if "DX" in names else ls.append("全画幅")
            # print(names)
            ls.append([j for j in names if 'mm' in j][0].split("-")[0])
            if len([j for j in names if 'mm' in j][0].split("-")) > 1:
                ls.append([j for j in names if 'mm' in j][0].split("-")[1])
            else:
                ls.append([j for j in names if 'mm' in j][0].split("-")[0])
            ls.append("".join([j for j in names if 'f/' in j]))
            JieGou = [j for j in data[i][1] if '组' in j and '片' in j]
            if JieGou == []:
                ls.append('官网未提供')
            else:
                ls.append(JieGou[0])
            MaDa = [j for j in data[i][1] if '马达' in j]
            if MaDa == []:
                ls.append('其他')
            else:
                ls.append(MaDa[0])
            size = [data[i][1][j] for j in range(len(data[i][1])) if '镜尺' in data[i][0][j]]
            if size == []:
                ls.append('官网未提供')
            else:
                ls.append(size[0])
            ls.append("VR防抖") if "VR" in names else ls.append('无')
            Weight = [j for j in data[i][1] if 'g' in j]
            if Weight == []:
                ls.append('官网未提供')
            else:
                ls.append(Weight[0])
            ls[2] = ls[2] + 'mm' if 'mm' not in ls[2] else ls[2]
            dic.append(ls)
        dic = pd.DataFrame(dic)
        dic.columns = dic.values.tolist()[0]
        dic.drop([0], inplace=True)
        self.dic = dic
        if 'Nikon_F_Mount.xlsx' not in os.listdir(): 
            writer = pd.ExcelWriter('Nikon_F_Mount.xlsx')
            dic.to_excel(writer)
            writer.save()
            
            
    @staticmethod
    def sign(jpg_name):
        img=cv2.imread(jpg_name) # 导入我们需要添加水印的图片
        RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        blank_img = np.zeros(shape=(RGB_img.shape[0],RGB_img.shape[1],3), dtype=np.uint8)
        font = cv2.FONT_HERSHEY_SIMPLEX
        # 添加水印的文字内容
        cv2.putText(blank_img,text='L1_Sta2',org=(img.shape[0]//2-100, img.shape[1]//2-100),
                    fontFace=font,fontScale= 2,
                    color=(255,255,255),thickness=10,lineType=cv2.LINE_4)
        blended = cv2.addWeighted(src1=RGB_img, alpha=0.7,
                                src2=blank_img, beta=1, gamma = 2)
        cv2.imwrite(f"./{jpg_name[:-4]}_sy.png", blended)
    
    
    def data_to_jpg(self):       
        if 'Nikon_F_Mount.png' not in os.listdir():
            dfi.export(self.dic, "./Nikon_F_Mount.png")
        if 'Nikon_F_Mount_sy.png' in os.listdir():
            return
        self.sign("Nikon_F_Mount.png")
        
    
    def focal_lenth__f_stop_count(self):
        if 'Nikon_F_Mount焦段光圈覆盖情况_sy.png' in os.listdir():
            return 
        dic = self.dic
        self.names = names = [i for i in dic['名称'].values]
        start = list(map(eval, [i[:-2] for i in dic['最小焦段'].values]))
        end = list(map(eval, [i[:-2] for i in dic['最大焦段'].values]))
        f_stop = ["".join([j for j in i if j.isdigit() or j == '-' or j == '.']) for i in dic['最大光圈'].values]
        f_stop_min, f_stop_max = [], []
        for i in f_stop:
            ls = list(map(float, i.split('-')))
            if len(ls) == 1:
                f_stop_max.append(ls[0])
                f_stop_min.append(ls[0])
            else:
                f_stop_max.append(ls[1])
                f_stop_min.append(ls[0]) 
        
        for i in range(len(names)):
            if start[i] != end[i]:
                plt.plot([start[i], end[i]], [f_stop_min[i], f_stop_max[i]])
            else:
                print(start[i], end[i])
                plt.plot([start[i], end[i]], [f_stop_min[i], f_stop_max[i]], marker = 'o')
        plt.xlabel("focal_lenth")
        plt.ylabel("f_stop")
        plt.xlim((0, 810))
        plt.ylim((1.2, 7))
        plt.xticks([14, 24, 35, 50, 85, 120, 150, 200, 300, 400, 500, 600, 800])
        plt.yticks([1.2, 1.4, 1.8, 2, 2.8, 3.5, 4, 4.5, 5.6, 6.3, 7])
        plt.title("Nikon_F_Mount焦段光圈覆盖情况")
        plt.legend(names)
        plt.savefig('Nikon_F_Mount焦段光圈覆盖情况.png', dpi=350)
        plt.show()     
        self.sign("Nikon_F_Mount焦段光圈覆盖情况.png")
        
        
    def clustering(self):
        ls = self.dic
        ls['画幅'] = ls['画幅'].replace('全画幅', 1.5).replace('APS-C画幅', 1)
        ls['减震'] = ls['减震'].replace('VR防抖', 1).replace('无', '0')
        ls = ls.drop(columns='重量').drop(columns='结构').drop(columns='名称').drop(columns='对焦宁静波动马达')
        ls['最小焦段'] = [eval(i[:-2]) for i in ls['最小焦段'].values]
        ls['最大焦段'] = [eval(i[:-2]) for i in ls['最大焦段'].values]
        # print(sum([1 for i in ls['滤镜尺寸'] if i == '官网未提供']))
        ls = ls.drop(columns='滤镜尺寸')
        gq = ([("".join([j for j in i if j.isdigit() or j == '.' or j == '-'])) for i in ls['最大光圈']])
        ls['最大光圈'] = [float(i) if '-' not in i else (eval(i.split('-')[0]) + eval(i.split('-')[1])) / 2 for i in gq]
        # print(ls)
        rc = {'font.sans-serif': 'SimHei',
            'axes.unicode_minus': False}
        sns.set(style='whitegrid', context='notebook', rc=rc)   #style控制默认样式,context控制着默认的画幅大小
        sns.pairplot(ls, size=2)
        plt.savefig('./pngs/相关性分析.png', dpi=350)
        plt.title('相关性分析')
        plt.show()
        corr = ls.corr()
        sns.heatmap(corr, cmap='GnBu_r', square=True, annot=True)
        plt.savefig('./pngs/相关度热力图.png', dpi=350)
        plt.title('相关热力图')
        plt.show()
                     
                        
if __name__ == '__main__':
    s = Spider()
    if not s.file_init():
        s.main()
    data = s.load_json()
    a = Analyse()
    a.data_to_excel()
    a.data_to_jpg()
    a.focal_lenth__f_stop_count()
    a.clustering()
