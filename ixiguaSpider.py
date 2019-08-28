#-*- coding:utf-8 -*-

import execjs
import time
import hashlib
import requests
import os
import json
import re
import random
from zlib import crc32
from base64 import b64decode

class IxiguaSpider(object):
    def __inti__(self):
        pass

    def genearteMD5(self, str):
        # 创建md5对象
        hl = hashlib.md5()

        # Tips
        # 此处必须声明encode
        # 否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
        hl.update(str.encode(encoding='utf-8'))

        print('MD5加密前为 ：' + str)
        print('MD5加密后为 ：' + hl.hexdigest())

    def get_js(self):
        path  = os.path.abspath(os.path.dirname(__file__));
        f = open(path+"/test.js", 'r', encoding='utf-8')  # 打开JS文件
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        return htmlstr

    def get_sign(self, data):
        jsstr = self.get_js()
        ctx = execjs.compile(jsstr)  # 加载JS文件
        return (ctx.call('getsign', data))  # 调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数

    def getAsAndCp(self, t):
        ass = '479BB4B7254C150'
        cp = '7E0AC8874BB0985'
        ret = []
        # t = time.time()
        # t = 1566553203
        # t = (int(t))
        e = str.upper(hex(t))[2:]

        i = str.upper(hashlib.md5(str(t).encode("utf-8")).hexdigest())

        # print(t)
        # print("e:" + e)
        # print("i:" + i)

        if len(e) == 8:
            n = i[0:5]
            a = i[-5:]

            r = n[0:5]
            i = n[-5:]
            o = ""
            u = ""

            # print(n)
            # print(a)

            for k in range(5):
                o += n[k] + e[k:k + 1]
                u += e[k + 3:k + 4] + a[k]

            # for a in range(5):
            #     o += r[a]+e[a]
            #
            # for l in range(5):
            #     u += e[l+3]+i[l]

            # print("o:" + o)
            # print("u:" + u)

            # for r = n[0:5], i = n[-5:], o = "", a = 0; a < 5; a++
            #     o += r[a] + e[a];
            # for (var u = "", l = 0; l < 5; l++)
            #     u += e[l + 3] + i[l];

            ass = "A1" + o + e[-3:]
            cp = e[0:3] + u + "E1"

            # print("as:" + ass)
            # print("cp:" + cp)

            ret.append(ass)
            ret.append(cp)

        return ass, cp

    def get_ixigua_url(self):
        t = int(time.time())
        ass, cp = self.getAsAndCp(t)
        sign = self.get_sign(t)
        url = "https://m.ixigua.com/list/?tag=subv_game&ac=wap&count=20&format=json_raw&as={}&cp={}&max_behot_time={}&_signature={}&i={}"

        i = 1566872918
        return url.format(ass, cp, t, sign, i)

    def get_list_data(self, url):
        """获取视频列表地址"""
        headers = {
            "Sec-Fetch-Mode": "cors",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Referer": "https://m.ixigua.com/?channel=subv_game",
            'Cookie': "_ga=GA1.2.1951241709.1564126639; csrftoken=bb65a68c3838935a0811ce1ccea07df6; tt_webid=6727453654938633741; _gid=GA1.2.507751240.1566786114; _ba=BA0.2-20190826-5138e-6T09ZZQwzGIZWXYGfR1X"
        }
        resp = requests.get(url, headers=headers)

        # if (resp.status_code == requests.codes.ok):
        #     print(resp.headers['charset'])
        # j_resp = json.loads(resp.json())
        # video_url = j_resp['data']['video_list']['video_1']['main_url']
        # video_url = b64decode(video_url.encode()).decode()
        # return video_url
        # for r in j_resp['data']:
        #     print(r['media_name'], r['video_id'], r['title'], r['abstract'], r['large_image_url'], r['publish_time'],
        #           r['datetime'])

        # return j_resp['data'][0]
        return resp.text

if __name__ == '__main__':
    ixg = IxiguaSpider()
    url = ixg.get_ixigua_url()
    # print(url)
    data = ixg.get_list_data(url)
    print(data)
