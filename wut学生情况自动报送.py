# -*- encoding=utf8 -*-
__author__ = "L1STAR"

from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["Android:///",])


# script content
print("start...")


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)

flag = [1] * 11

def my_touch(nums_of_flag, location):
    ''' 找到并点击图像
        并修改对应监测点值为0
        未找到会返回false 
        找到返回true
    '''
    while flag[nums_of_flag]:
        if location:
            touch(location)
            flag[nums_of_flag] = 0
            return True
            print(f"已经完成flag{nums_of_flag}")
            sleep(1.5)
            
        else:
            return False
            print(f"未找到flag{nums_of_flag}")
    return False # 未找到直接返回False



while flag[0]:
    my_touch(1, exists(Template(r"tpl1649407498908.png", record_pos=(-0.232, -0.112), resolution=(2560, 1600))))
#     my_touch(2, exists(Template(r"tpl1649408551480.png", record_pos=(0.182, -0.264), resolution=(2560, 1600))))
    if flag[1] == 0 and flag[2] == 1:
        swipe(Template(r"tpl1649409203869.png", record_pos=(0.006, -0.235), resolution=(2560, 1600)), vector=[-0.033, 0.8574])
        flag[2] = 0
    my_touch(3, exists(Template(r"tpl1649409306673.png", record_pos=(-0.187, -0.103), resolution=(2560, 1600))))
    my_touch(4, exists(Template(r"tpl1649466585419.png", record_pos=(0.147, -0.027), resolution=(2560, 1600))))
    my_touch(5, exists(Template(r"tpl1649466724888.png", record_pos=(0.116, -0.009), resolution=(2560, 1600))))
    my_touch(6, exists(Template(r"tpl1649466813736.png", record_pos=(0.052, 0.283), resolution=(2560, 1600))))
    my_touch(7, exists(Template(r"tpl1649466847689.png", record_pos=(0.143, 0.125), resolution=(2560, 1600))))
    my_touch(8, exists(Template(r"tpl1649466897267.png", record_pos=(0.054, 0.285), resolution=(2560, 1600))))
    if flag[6] == 0 and flag[7] == 0 and flag[8] == 0 and flag[9]:
        swipe(Template(r"tpl1649467011798.png", record_pos=(0.137, 0.048), resolution=(2560, 1600)), vector=[-0.0086, -0.3325])
        flag[9] == 0
    my_touch(10, touch(Template(r"tpl1649467065853.png", record_pos=(0.0, 0.265), resolution=(2560, 1600))))
    if flag[10] == 0:
        break

print("执行完毕")
            
