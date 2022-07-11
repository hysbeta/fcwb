'''
cron: 7 7 7 7 7
new Env('发财挖宝助力');
'''
import json
import os
import sys
from time import sleep

import requests

requests.packages.urllib3.disable_warnings()

if __name__ == '__main__':
    print("发财挖宝助力开始！")
    try:
        max_invite = 111
        max_retry = 32
        sleep_time = 1
        if len(sys.argv) >= 2 and sys.argv[1][:21] == "https://api.m.jd.com/":
            fcwb_api = str(sys.argv[1])
        elif "fcwb_api" in os.environ is not None and os.environ["fcwb_api"][:21] == "https://api.m.jd.com/":
            fcwb_api = str(os.environ["fcwb_api"])
        else:
            raise Exception("No API link!")
        if ";" in fcwb_api:
            if fcwb_api.split(";")[1].isnumeric():
                max_invite = int(fcwb_api.split(";")[1])
        env_cookies = os.environ["JD_COOKIE"].split('&')
        if len(env_cookies) == 0:
            raise Exception("No available Cookies!")
        else:
            print(str(len(env_cookies)) + " 个 Cookies")
        print("目标助力次数 ： " + str(max_invite))
        print("最大重试次数 ： " + str(max_retry))
        print("重试等待时间 ： " + str(sleep_time)+"s")
        success_pin = []
        no_chance_pin = []
        failed_pin = []
        for cookies in env_cookies:
            print("========================================")
            for info in str(cookies).split(";"):
                if "pt_pin" in info:
                    currentPin = info.split("=")[1]
            print("当前Pin : " + str(currentPin))
            headers = {
                'Host': 'api.m.jd.com',
                'Accept': 'application/json, text/plain, */*',
                'Origin': 'https://bnzf.jd.com',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-cn',
                "User-Agent": 'jdapp;iPhone;9.4.4;14.3;network/4g;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
                'cookie': cookies
            }
            index = 0
            while index < max_retry:
                index += 1
                res = requests.get(fcwb_api, headers=headers, verify=False, timeout=10)
                print("第" + str(index) + "次尝试 : " + res.text)
                if "已经邀请过" in res.text or "\"errMsg\":\"success\"" in res.text:
                    success_pin.append(currentPin)
                    break
                elif "参与者参与次数达到上限" in res.text or "不能给自己助力" in res.text:
                    no_chance_pin.append(currentPin)
                    break
                else:
                    pass
                sleep(sleep_time)
            if currentPin not in success_pin and currentPin not in no_chance_pin:
                failed_pin.append(currentPin)
            if len(success_pin) >= max_invite:
                break
        print("========================================")
        print(str(len(success_pin)) + "个Pin成功助力")
        print(str(success_pin))
    except Exception as e:
        print(str(e))
