'''
                  江城子 . 程序员之歌

              十年生死两茫茫，写程序，到天亮。
                  千行代码，Bug何处藏。
              纵使上线又怎样，朝令改，夕断肠。

              领导每天新想法，天天改，日日忙。
                  相顾无言，惟有泪千行。
              每晚灯火阑珊处，夜难寐，加班狂。

'''
# -*- coding:utf-8 -*-
'''
Author: RuoWangC
Date: 2021-09-05 15:15:35
LastEditTime: 2021-09-05 21:17:53
LastEditors: your name
Description: 下载bilibli上的视频
FilePath: \spider\bilibili.py
'''
import requests, hashlib, sys, click, re, base64, binascii, json, os
from tqdm import tqdm
from http import cookiejar
from bs4 import BeautifulSoup
import subprocess


class BiliVideoLoader:
    def __init__(self):
        self.init_header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
        self.headers = {
            'authority': 'cn-hbwh-fx-bcache-06.bilivideo.com',
            'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'accept': '*/*',
            'origin': 'https://www.bilibili.com',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.bilibili.com/video/',
            'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6'
        }
        self.session = requests.session()

    def get_video_studio_urls(self):
        '''
        description: 初始请求htmnl 视频和音频的url在html中有
        param {*}
        return {*}
        '''        
        html = self.session.get(self.init_url, headers=self.init_header).content
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        head_str = "window.__playinfo__"
        name = soup.title.text
        for item in soup.find_all('script'):
            jsonstr = str(item.contents)

            if(head_str != jsonstr[2:len(head_str)+2]):
                continue
            jsonstr = jsonstr[jsonstr.find("{"):(jsonstr.rfind("}")+1)]
            # with open('test.json', 'w') as f:
            #     f.write(jsonstr)
            # f.close()
            playinfo = json.loads(jsonstr)

            video_url = playinfo['data']['dash']['video'][0]['baseUrl']
            audio_url = playinfo['data']['dash']['audio'][0]['baseUrl']
        return video_url, audio_url, name

    def download_data(self, url, name):
        '''
        description: 下载文件 
        param: 
            视频的 url 或者 音频的url 
            name中应该包含后缀
        return {*}
        '''        
        self.headers['range'] = 'bytes=0-1048576'
        mb = 1024*1024
        with open(name, 'wb') as f:
            response = self.session.get(url, headers=self.headers)
            max_len = int(response.headers['Content-Range'][16:])
            f.write(response.content)
            
            pack_no = range(1, int(max_len / mb + 1))

            for idx in tqdm(pack_no, total=(len(pack_no)), desc='正在下载 %s'%name):
                if(idx*mb > max_len):    
                    break
                self.headers['range'] = 'bytes=' + str(idx*mb+1) + '-' + str(min((idx+1)*mb, max_len))
               
                response = self.session.get(url, headers=self.headers)
                f.write(response.content)

        f.close()
    
    def merge_video_and_audio(self, name):
        """
        音视频合并函数，利用ffmpeg合并音视频
        :param video_name: 传入标题
        :return:
        """
        print('正在合并...')
        command = f'ffmpeg -i "{name}.m4a" -i "{name}.mp3" -c copy "{name}.mp4" -loglevel quiet'
        subprocess.Popen(command, shell=True)
        
    def run(self, id):
        '''
        description: 下载一个视频 三步走 分别下载视频，音频，然后合并二者
        param : id 为视频的id号 例如 BV1Zt411P7cD
        return {*}
        '''        
        self.init_url = 'https://www.bilibili.com/video/' + id +'/'

        vid_url, aud_url, name = self.get_video_studio_urls()
        self.download_data(vid_url, '%s.m4a' % name)
        self.download_data(aud_url, '%s.mp3' % name)
        self.merge_video_and_audio(name)
        print(f'下载完成！！！')


if __name__ == '__main__':
    spd = BiliVideoLoader()
    spd.run('BV1Zt411P7cD')

