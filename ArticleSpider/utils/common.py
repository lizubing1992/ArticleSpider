# _*_ coding: utf-8 _*_
__author__ = 'lizubing1992'
__date__ = '2018/9/26 15:28'
import hashlib


def get_md5(url):
    if isinstance(url,str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == "__main__":
    print(get_md5("http://jobbole.com".encode("utf-8")))
