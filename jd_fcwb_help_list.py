import datetime
import json
import os
import time

import requests

requests.packages.urllib3.disable_warnings()

'''
cron: 7 7 7 7 7
new Env('发财挖宝助力链接');
'''


def get_cookies(vip_select=True):
    cookies_arr = []
    env_cookies = os.environ["JD_COOKIE"].split('&')
    vip_pins = os.environ["JDLITE_VIP"].split("&")
    if len(vip_pins) != 0 and vip_select:
        print("VIP Pins:" + str(vip_pins))
        for env_cookie in env_cookies:
            for vip_pin in vip_pins:
                if str(vip_pin) in str(env_cookie):
                    cookies_arr.append(env_cookie)
                    break
    else:
        cookies_arr = env_cookies
    if len(cookies_arr) == 0:
        if not vip_select:
            raise Exception("无有效Cookies，请检查。")
        else:
            cookies_arr = get_cookies(False)
    return cookies_arr


def get_help_link(cookies):
    for cookie in cookies:
        try:
            res_code = 0
            for text in cookie.split(";"):
                if "pin" in str(text):
                    JDPin=str(text).split("=")[1]
                    # print("账号：" + JDPin)
            url = "https://api.m.jd.com/?functionId=happyDigHome&body={\"linkId\":\""+activityID+"\"}&t="+str(int(time.mktime(datetime.datetime.now().timetuple()) * 1000))+"&appid=activities_platform&client=H5&clientVersion=1.0.0&h5st=" + h5st
            headers = {
                "Host": "api.m.jd.com",
                "user-agent": "jdltapp;android;3.8.20;;;appBuild/2324;ef/1;ep/%7B%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22ts%22%3A1654268870802%2C%22ridx%22%3A-1%2C%22cipher%22%3A%7B%22sv%22%3A%22CJS%3D%22%2C%22ad%22%3A%22ZwU1YzCnEQO5CWO0ZWY0ZK%3D%3D%22%2C%22od%22%3A%22YWZtDtrvCzc0EJDvDwDrYq%3D%3D%22%2C%22ov%22%3A%22CzO%3D%22%2C%22ud%22%3A%22ZwU1YzCnEQO5CWO0ZWY0ZK%3D%3D%22%7D%2C%22ciphertype%22%3A5%2C%22version%22%3A%221.2.0%22%2C%22appname%22%3A%22com.jd.jdlite%22%7D;Mozilla/5.0 (Linux; Android 12; 2201122C Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/101.0.4951.61 Mobile Safari/537.36",
                'accept': '*/*',
                "origin": "https://bnzf.jd.com",
                'referer': 'https://bnzf.jd.com/',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'cookie': cookie
            }
            while res_code != 200:
                res = requests.get(url=url, headers=headers, verify=False, timeout=10)
                res_code = res.status_code
            inviteCode = str(json.loads(res.text)["data"]["inviteCode"])
            inviterID = str(json.loads(res.text)["data"]["markedPin"])
            help_url = "https://bnzf.jd.com/?activityId="+activityID+"&inviterId="+inviterID+"&inviterCode="+inviteCode
            #+"&ad_od=share&utm_source=androidapp&utm_medium=appshare&utm_campaign=t_335139774&utm_term=Wxfriends"
            print(JDPin)
            print(help_url)
        except:
            print("[Error]"+str(cookie))


if __name__ == '__main__':
    print("开始获取发财挖宝助力链接！")
    activityID = "pTTvJeSTrpthgk9ASBVGsw"
    h5st = "20220603230754081%3B7899561328096576%3Bce6c2%3Btk02w7e611afd18nG2JPwUy5YPXg65Nk1kKsePlZ%2BfR%2FrckPXRA5oVBTSmCWMmAr6q2HOO4GQAWN8OC3XL%2FrmDt1oolH%3B9715d61d1c8952e2fa78a1c9c54e619a955a5a3f2d5e202311c61047a02aa0bc%3B3.0%3B1654268874081"
    get_help_link(get_cookies())
