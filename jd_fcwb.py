#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
cron: 35 2-14/1 * * *
new Env('发财挖宝');
活动入口: 京东极速版>我的>发财挖宝
脚本功能为: 一挖到底！
'''
import os,json,random,time,re,string,functools,asyncio
import sys
sys.path.append('../../tmp')
print('\n运行本脚本之前请手动进入游戏点击一个方块\n')
print('\n挖的如果都是0.01红包就是黑了，别挣扎了！\n')
try:
    import requests
except Exception as e:
    print(str(e) + "\n缺少requests模块, 请执行命令：pip3 install requests\n")
requests.packages.urllib3.disable_warnings()


linkId="pTTvJeSTrpthgk9ASBVGsw"


# 获取pin
cookie_findall=re.compile(r'pt_pin=(.+?);')
def get_pin(cookie):
    try:
        return cookie_findall.findall(cookie)[0]
    except:
        print('ck格式不正确，请检查')

# 读取环境变量
def get_env(env):
    try:
        if env in os.environ:
            a=os.environ[env]
        elif '/ql' in os.path.abspath(os.path.dirname(__file__)):
            try:
                a=v4_env(env,'/ql/config/config.sh')
            except:
                a=eval(env)
        elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
            try:
                a=v4_env(env,'/jd/config/config.sh')
            except:
                a=eval(env)
        else:
            a=eval(env)
    except:
        a=''
    return a

# v4
def v4_env(env,paths):
    b=re.compile(r'(?:export )?'+env+r' ?= ?[\"\'](.*?)[\"\']', re.I)
    with open(paths, 'r') as f:
        for line in f.readlines():
            try:
                c=b.match(line).group(1)
                break
            except:
                pass
    return c 


# 随机ua
def ua():
    sys.path.append(os.path.abspath('.'))
    try:
        from jdEnv import USER_AGENTS as a
    except:
        a='jdpingou;android;5.5.0;11;network/wifi;model/M2102K1C;appBuild/18299;partner/lcjx11;session/110;pap/JA2019_3111789;brand/Xiaomi;Mozilla/5.0 (Linux; Android 11; M2102K1C Build/RKQ1.201112.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36'
    return a

# 13位时间戳
def gettimestamp():
    return str(int(time.time() * 1000))

## 获取cooie
class Judge_env(object):
    def main_run(self):
        if '/jd' in os.path.abspath(os.path.dirname(__file__)):
            cookie_list=self.v4_cookie()
        else:
            cookie_list=os.environ["JD_COOKIE"].split('&')       # 获取cookie_list的合集
        if len(cookie_list)<1:
            print('请填写环境变量JD_COOKIE\n')    
        return cookie_list

    def v4_cookie(self):
        a=[]
        b=re.compile(r'Cookie'+'.*?=\"(.*?)\"', re.I)
        with open('/jd/config/config.sh', 'r') as f:
            for line in f.readlines():
                try:
                    regular=b.match(line).group(1)
                    a.append(regular)
                except:
                    pass
        return a
cookie_list=Judge_env().main_run()   


def taskGetUrl(functionId, body, cookie):
    res_code = 0
    url=f'https://api.m.jd.com/?functionId={functionId}&body={json.dumps(body)}&t={gettimestamp()}&appid=activities_platform&client=H5&clientVersion=1.0.0'
    headers={
        'Cookie': cookie,
        'Host': 'api.m.jd.com',
        'Connection': 'keep-alive',
        'origin': 'https://bnzf.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'accept': 'application/json, text/plain, */*',
        "User-Agent": ua(),
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    try_time = 0
    while res_code != 200 or try_time > 2:
        try_time = try_time + 1
        try:
            res=requests.get(url,headers=headers, timeout=10)
            res_code = res.status_code
        except:
            res_code = 0
    return res.json()


# 剩余血量
def xueliang(cookie):
    body={"linkId":linkId}
    res=taskGetUrl("happyDigHome", body, cookie)
    if not res:
        return
    if res['code']==0:
        if res['success']:
            curRound=res['data']['curRound']                        # 未知
            blood=res['data']['blood']                              # 剩余血量
            return blood      

def jinge(cookie,i):
    body={"linkId":linkId}
    res=taskGetUrl("happyDigHome", body, cookie)
    if not res:
        return
    if res['code']==0:
        if res['success']:
            curRound=res['data']['curRound']                        # 未知
            blood=res['data']['blood']                              # 剩余血量
            roundList=res['data']['roundList']                      # 3个总池子
            roundList_n=roundList[0]
            redAmount=roundList_n['redAmount']                  # 当前池已得京东红包
            cashAmount=roundList_n['cashAmount']                # 当前池已得微信红包

            return [blood,redAmount,cashAmount]   

# 页面数据
def happyDigHome(cookie):
    body={"linkId":linkId}
    res=taskGetUrl("happyDigHome", body, cookie)
    if not res:
        return
    if res['code']==0:
        if res['success']:
            curRound=res['data']['curRound']                        # 未知
            incep_blood=res['data']['blood']                        # 剩余血量
            roundList=res['data']['roundList']                      # 3个总池子
            for e,roundList_n in enumerate(roundList):              # 迭代每个池子
                roundid=roundList_n['round']                        # 池序号
                state=roundList_n['state'] 
                rows=roundList_n['rows']                            # 池规模，rows*rows
                redAmount=roundList_n['redAmount']                  # 当前池已得京东红包
                cashAmount=roundList_n['cashAmount']                # 当前池已得微信红包
                leftAmount=roundList_n['leftAmount']                # 剩余红包？
                chunks=roundList_n['chunks']                        # 当前池详情list

                a=jinge(cookie,roundid)
                print(f'当前池序号为 {roundid} \n当前池规模为 {rows}*{rows}')
                print(f'剩余血量 {a[0]}')
                print(f'当前池已得京东红包 {a[2]}\n当前池已得微信红包 {a[1]}\n')
                _blood=xueliang(cookie)
                if _blood>0:
                    happyDigDo(cookie,roundid,0,0)
                    if e==0 or e==1:
                        roundid_n=4
                    else:
                        roundid_n=5
                    for n in range(roundid_n):
                        for i in range(roundid_n):
                            _blood=xueliang(cookie)
                            if _blood>0:
                                print(f'本次挖取坐标为 ({n},{i})')
                                happyDigDo(cookie,roundid,n,i)
        else:
            print(f'获取数据失败\n{res}\n')
    else:
        print(f'获取数据失败\n{res}\n')
    

# 挖宝
def happyDigDo(cookie,roundid,rowIdx,colIdx):
    body={"round":roundid,"rowIdx":rowIdx,"colIdx":colIdx,"linkId":linkId}
    res=taskGetUrl("happyDigDo", body, cookie)
    if not res:
        return
    if res['code']==0:
        if res['success']:
            typeid=res['data']['chunk']['type']
            if typeid==2:
                print(f"挖到京东红包 {res['data']['chunk']['value']}\n")
            elif typeid==3:
                print(f"挖到微信红包 {res['data']['chunk']['value']}\n")
            elif typeid==4:
                print(f"挖到炸弹\n")
            elif typeid==1:
                print(f"挖到优惠券\n")
            else:
                print(f'挖到外星物品\n')
        else:
            print(f'挖取失败\n{res}\n')
    else:
        print(f'挖取失败\n{res}\n')


def main():
    print('🔔发财挖宝，开始！\n')
    print(f'====================共{len(cookie_list)}京东个账号Cookie=========\n')

    for e,cookie in enumerate(cookie_list,start=1):
        print(f'******开始【账号 {e}】 {get_pin(cookie)} *********\n')
        happyDigHome(cookie)


if __name__ == '__main__':
    main()
