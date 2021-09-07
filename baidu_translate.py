# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
info:
author:CriseLYJ
github:https://github.com/CriseLYJ/
"""

"""
请求url分析 :https://fanyi.baidu.com/basetrans
请求方式分析 :POST
请求参数分析 : {
query: hello
from: en
to: zh
token: 6f5c83b84d69ad3633abdf18abcb030d
sign: 54706.276099}
请求头分析
"""

# 代码实现流程
# 1. 实现面对对象构建爬虫对象
# 2. 爬虫流程四步骤
# 2.1 获取URl
# 2.2 发送请求获取响应
# 2.3 从响应中提取数据
# 2.4 保存数据

import requests
import js2py

context = js2py.EvalJs()

# 翻译模式
# 0:英译中 1:中译英
translating_mode = 0

class BaiDuTranslater(object):
    """
    百度翻译爬虫
    """

    def __init__(self, query):
        # 初始化
        self.url = "https://fanyi.baidu.com/v2transapi"
        self.query = query
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Referer": "https://fanyi.baidu.com/",
            "Cookie": "BIDUPSID=5A9E4138D034212244C0A4F95E3459D4; PSTM=1593503403; __yjs_duid=1_3c52c89af8ec0b7bd510e2660e2ec47d1617884117176; BAIDUID=7732E86FE9CEF0694DA367BDC7B092F6:FG=1; H_WISE_SIDS=110085_127969_128698_131862_164870_168389_175667_175756_176677_177007_177058_177406_177897_177989_178007_178328_178631_179345_179469_180276_180317_180407_180868_181207_181261_181399_181589_181709_181825_182025_182100_182178_182192_182253_182283_182320_182417_182530_182576_182596_182819_182847_182902_183002_183030_183308_183327_183400_183431_183527_183548_183569_183955_184012_184146_184246_184463_184507_184516_184575_8000091_8000100_8000118_8000131_8000135_8000145_8000159_8000175_8000177_8000182_8000185; BAIDUID_BFESS=EF125F07F3C81521B71BD34821576E9C:FG=1; ZD_ENTRY=google; BDRCVFR[FhauBQh29_R]=mbxnW11j9Dfmh7GuZR8mvqV; delPer=0; PSINO=1; BDUSS=WZBV2x1R2YxRlZudnJhNTczQjQ3ekNySEk4NXlZOTBSVTNRYkxiZGl5OXNWbGhoRVFBQUFBJCQAAAAAAAAAAAEAAAClpxJ-uf7Et7~bAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGzJMGFsyTBhZ; BDUSS_BFESS=WZBV2x1R2YxRlZudnJhNTczQjQ3ekNySEk4NXlZOTBSVTNRYkxiZGl5OXNWbGhoRVFBQUFBJCQAAAAAAAAAAAEAAAClpxJ-uf7Et7~bAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGzJMGFsyTBhZ; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_PSSID=34440_34531_34497_33848_34524_34092_34507_26350; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDU_WISE_UID=wapp_1630726238531_324; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; __yjs_st=2_MTllYmVlOWM4ZTZlYzhlMGU2NWU0NDJkZWIyODEzNTMyNWE2OTFiMGY0N2M3YWJiZWFjZDU4NTJlZTQ0ZWU1NDliMDNiNDZhMGJiNGE0ZjhhMjA4ZmZiMWFiZDk0YTY0MjM2YTdkYjdmNTEyYzk0NDQyMWNkMTI0ZGJiMDkwNmExMDkxMWQxZDBmYWE4Y2ZmZjg4YTQzNmQyNWE2ODkzOTYzMjVjNjE3MjYwNGI5NDkyMTJlNjM4NjM5YmQ3NDNiOWI3ODRkOGVlODBjM2ZlNGEwNmU4Y2ZlMDhjMzdmMDhlN2RiMjRlYWZkZWRkZTZmNTBkNzEzNzdhOGZkNTI2YmY4NzM5NWVkYjUyMTMwOTMxOTQ5YmQwYTQyNGJkMDEyXzdfOWJlMDJkNTM=; ab_sr=1.0.1_ZDIwYjk3MTlkODEyNTk5MTAwZTEwZDAxZjljOTE5NzU4ZDQ5ZGJjNGVkOTI3NDA1N2FiODdlZGJkZWIzZTZiNjdlYTI0ZjUyZWVkZDM0MGFlYmRlMDFlZGE5ZmRiZmQwMjQwMTRiMWMxZmYyNjAxNGZlM2MyNjc4ODYzNTY5M2JiMzM3Mjg1YzQ0NjY2NmQ4Y2JkNmNhMDYzOGZhYTc0ZmQ2YWI3NWY4MjI2MzM4ODg4YjNjYmU4NDE4OWZhM2Vk",
            "Host":"fanyi.baidu.com"
        }

    def make_sign(self):
        # js逆向获取sign的值
        with open("baidu_translate.js", "r", encoding="utf-8") as f:
            context.execute(f.read())

        # 调用js中的函数生成sign
        sign = context.e(self.query)
        # 将sign加入到data中
        return sign

    def make_data(self, sign):
        # 判断翻译模式,选取对应的 from 和 to 值.
        if translating_mode == 0:
            from_str = "en"
            to_str = "zh"
        else:
            from_str = "zh"
            to_str = "en"
        data = {
            "query": self.query,
            "from": from_str,
            "to": to_str,
            "token": "8b0e4886bfc69515d4a6ec2433fc562a",
            "sign": sign,
            "simple_means_flag": 3,
            "domain": "common",
            "transtype": "translang"
        }
        return data

    def get_content(self, data):
        # 发送请求获取响应
        response = requests.post(
            url=self.url,
            headers=self.headers,
            data=data
        )
        return response.json()["trans_result"]["data"][0]["dst"]

    def run(self):
        """运行程序"""
        # 获取sign的值
        sign = self.make_sign()
        # 构建参数
        data = self.make_data(sign)
        # 获取翻译内容
        content = self.get_content(data)
        print(content)


if __name__ == '__main__':
    translating_mode = int(input("请输入翻译模式(0:英译中 1:中译英):"))
    query = input("请输入您要翻译的内容:")
    translater = BaiDuTranslater(query)
    translater.run()