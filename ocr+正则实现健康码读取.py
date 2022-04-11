# author = 'L1Sta2'
# ver = 1.0
# name = '健康码信息提取'

import pytesseract # ocr库, 已经完成训练
from PIL import Image # 用于打开图片
import re
import os
import pandas as pd
# 提交健康码的时候需要用姓名命名
# 原因是由于健康码调整，去掉了显示自己身份证和姓名的功能(小眼睛没了)
# 功能是 将当前列表中的所有截图中信息提取 并在当前目录新建excel来保存结果

def files_get() -> list:
    '''返回当前目录下所有的截图和姓名'''
    names = os.listdir(os.getcwd())
    pics = []
    users = []
    for file in names:
        if os.path.basename(file).endswith('.png'):
            # 找到后缀名为png的截图名称并保存到新列表
            user_name = file.replace('.png', '')
            pics.append(file)
            users.append(user_name)
    return pics, users


def ocr_scaning(pics, users) -> list:
    '''主循环,把当前列表所有的图片信息读取并转化为列表返回'''
    pytesseract.pytesseract.tesseract_cmd = 'C://Program Files (x86)/Tesseract-OCR/tesseract.exe'
    # 对ocr进行初始化
    ls_of_person = []
    for x, picture in enumerate(pics):
        image = Image.open(picture)
        what = pytesseract.image_to_string(image, lang='chi_sim')
        # 开始识别 设置语言为中文
        # 训练好的库需要自己下载
        name = users[x]
        # print(name, what)
        date_feature = re.compile(r"(\d{4}-\d{1,2}-\d{1,2})")
        match_lists = date_feature.findall(what)

        try:
            screen_date, test_date, vacine_date = match_lists[:]
            # 可能有人的没有完成
        except:
            screen_date, test_date = match_lists[:]
            vacine_date = "数据同步中"
            # 获取三个日期 截图日期 上次检测时间 接种时间
            # 部分人可能只有两个日期 因为非本省接种疫苗，所以会少第三个报错

        try:
            bool_vac = re.search(
                r"(阴?)(阳?) 性( ?)[0-9]", what.replace("E", "阴 性"))
            # 这个正则用于识别当前为阴性或者阳性 并找到接种次数
            bool_test_result = bool_vac.group().replace(" ", '')
            result, times = bool_test_result[:2], bool_test_result[-1] if 1 <= int(
                bool_test_result[-1]) <= 3 else 3
        except:
            if "阴" in what:
                result = '阴性'
                times = vacine_date
                # 部分人可能识别不到阴性 这个时候直接判断是否含有串
                # 当然也可以修改面的匹配，让[0-9]? 但是就需要匹配最后一个结果了

        ls_of_person.append([name, screen_date, test_date,
                            vacine_date, result, times])
    return ls_of_person


def build_excel(ls_of_people) -> None:
    '''将数据保存到excel'''
    writer = pd.ExcelWriter('健康码.xlsx')
    # 当前文件夹新建文件
    data = pd.DataFrame(ls_of_people)
    data.columns = ['姓名', '截图日期', '核酸检测日期', '上次接种日期', '核酸结果', '疫苗接种次数']
    data.to_excel(writer, sheet_name='表格1')
    writer.save()
    print(data)


if __name__ == '__main__':
    pics, users = files_get()
    ls_of_people = ocr_scaning(pics, users)
    build_excel(ls_of_people)

