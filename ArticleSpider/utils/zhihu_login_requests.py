# _*_ coding: utf-8 _*_
__author__ = 'lizubing1992'
__date__ = '2018/10/4 16:04'
import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": agent
}


def get_xsrf():
    response = requests.get("https://www.zhihu.com", headers=header)
    match_obj = re.match("")
    return ""


def zhihu_login(account, password):
    # 知乎登录
    if re.match("^1\d{10}", account):
        print("手机号码登录")
        post_url = "https://www.zhihu.com/api/v3/oauth/sign_in"
        post_data = {
            "-xsrf": get_xsrf,
            "phone_num": account,
            "password": password
        }

get_xsrf()