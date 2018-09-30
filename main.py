# _*_ coding: utf-8 _*_
__author__ = 'lizubing1992'
__date__ = '2018/9/16 12:52'

from scrapy.cmdline import execute

import sys
import os

# 获取main文件的父目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","jobbole"])