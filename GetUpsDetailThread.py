"""
GetUpsDetail的多线程版
"""

import requests
import json
import time
from threading import Thread
import pandas as pd


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "cookie": "rpdid=|(k|R~|))kY)0J'ulmRm~kkYu; CURRENT_FNVAL=16; _uuid=E1401EB7-6163-5FAF-0810-6B3AF05ECB7298509infoc; buvid3=137DCCAF-2D05-49A1-8CD7-9137FF0998AA40958infoc; DedeUserID=287932745; DedeUserID__ckMd5=b7c29df8e71b0a95; SESSDATA=4ac2443a%2C1610788657%2Ce836c*71; bili_jct=43bcb09180437e0c4fbe72be83c055fa; CURRENT_QUALITY=0; LIVE_BUVID=AUTO5515958176620775; bp_t_offset_287932745=418930332671127462; PVID=4; bp_video_offset_287932745=422854322163518803; bfe_id=5db70a86bd1cbe8a88817507134f7bb5",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"

}

detail_url = "https://api.bilibili.com/x/web-interface/card"
other_url = "https://api.bilibili.com/x/space/upstat"
main_url = "https://api.bilibili.com/x/relation/stat"

with open('name_uid.json', 'r', encoding='utf-8') as fp:
    data = json.load(fp)

up_detail_list = []


def parse_main_url(name, vmid):
    params = {'vmid': vmid}

    response = requests.get(main_url, headers=headers, params=params)
    res = response.json()

    mid = res['data']['mid']
    follower = res['data']['follower']

    up_detail_dict = {}
    up_detail_dict['VMID'] = mid
    up_detail_dict['名称'] = name
    up_detail_dict['粉丝数'] = follower
    up_detail_list.append(up_detail_dict)


for k, v in data.items():
    t = Thread(target=parse_main_url, args=(k, v), daemon=True)
    t.start()

time.sleep(1.2)

# with open('up_detail.json', 'w', encoding='utf-8') as fp:
#     json.dump(up_detail_list, fp, ensure_ascii=False)
data = pd.read_json(json.dumps(up_detail_list, ensure_ascii=False))
print(data)
# def parse_url(vmid):
#     params = {'mid': vmid}
#
#     response1 = requests.get(detail_url, headers=headers, params=params)
#     response2 = requests.get(other_url, headers=headers, params=params)
#     res1 = response1.json()
#     res2 = response2.json()
#
#     data1 = res1['data']['card']
#
#     up_detail_dict = {}
#     mid = data1['mid']
#     name = data1['name']
#     fans = data1['fans']
#     attention = data1['attention']
#     like = res2['data']['likes']
#     view = res2['data']['archive']['view']
#
#     up_detail_dict['MID'] = mid
#     up_detail_dict['名称'] = name
#     up_detail_dict['粉丝数'] = fans
#     up_detail_dict['关注数'] = attention
#     up_detail_dict['获赞数'] = like
#     up_detail_dict['播放数'] = view
#
#     up_detail_list.append(up_detail_dict)

# for v in data.values():
#     t = Thread(target=parse_url, args=(v,))
#     t.start()


