# _*_ coding: utf-8 _*_
__author__ = 'lizubing1992'
__date__ = '2018/9/26 15:28'
import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def remove_start(url):
    return url.replace("\"", "")


if __name__ == "__main__":
    print(remove_start("\"http://5b0988e595225.cdn.sohucs.com/images/20180517/c50cbf0d0cc248bb8127ddd962aa7df2.png\""))
