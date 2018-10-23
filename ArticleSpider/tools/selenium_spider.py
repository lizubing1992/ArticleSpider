# _*_ coding: utf-8 _*_
__author__ = 'lizubing1992'
__date__ = '2018/10/22 20:59'

from selenium import webdriver

browser = webdriver.PhantomJS(executable_path = "E:/phantomjs-2.1.1-windows/bin/phantomjs.exe")


browser.get("https://sz.58.com/zufang/35842542054969x.shtml?fzbref=0&from=1-list-1&psid=129720401201878837198634063&iuType=gz_2&ClickID=1&apptype=0&key=&entinfo=35842542054969_0&params=rankbusitime0099^desc&cookie=||https://www.baidu.com/link?url=x26wJ9cA7wKz4juOV3WtTNFklE5XKSzcKUyAKgzelKq&wd=&eqid=ad5c698c0000022b000000065bcdca27|FjuJDFsU0Ip/4JNB4t3cWw==&PGTID=0d3090a7-0000-44e6-12ec-f7e6075f19db&local=4&pubid=46447700&trackkey=35842542054969_f2d8a8c2-5bb4-4363-88de-326b18a270af_20181022210140_1540213300555&fcinfotype=gz")

print(browser.page_source)