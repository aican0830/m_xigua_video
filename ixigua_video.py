# coding:utf8
import re
import requests
import random
from zlib import crc32
from base64 import b64decode
import os
import sys


def get_video_url_api(video_id):
    """获取视频地址所在包的url"""
    r = str(random.random())[2:]
    url_part = "/video/urls/v/1/toutiao/mp4/{}?r={}".format(video_id, r)
    s = crc32(url_part.encode())
    url = "https://ib.365yg.com{}&s={}".format(url_part, s)
    return url


def get_video_url(url):
    """获取视频地址"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    }
    resp = requests.get(url, headers=headers)
    j_resp = resp.json()
    video_url = j_resp['data']['video_list']['video_1']['main_url']
    video_url = b64decode(video_url.encode()).decode()
    return video_url


def get_video_id(url):
    """获取视频id"""
    headers = {
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    }
    resp = requests.get(url, headers=headers)
    # 获取video_id
    return re.search("video_id: '([^\']+)'", resp.text).group(1)


def main():
    url = "https://www.ixigua.com/i6710179386772947463/"
    url = "https://www.ixigua.com/i6562763969642103303/#mid=6602323830"
    url = "https://m.ixigua.com/i6719750385256382983/?channel=subv_game";
    #
    # video_id = get_video_id(url)
    # print(video_id)
    #
    # print(sys.argv[1:][0])
    video_id = sys.argv[1:][0]

    video_url_api = get_video_url_api(video_id)
    # print(video_url_api)
    #
    video_url = get_video_url(video_url_api)
    print(video_url)
    return


if __name__ == '__main__':
    main()