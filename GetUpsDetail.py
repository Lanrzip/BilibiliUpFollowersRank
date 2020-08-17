import requests
import json
import re


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "cookie": "finger=158939783; rpdid=|(k|R~|))kY)0J'ulmRm~kkYu; CURRENT_FNVAL=16; _uuid=E1401EB7-6163-5FAF-0810-6B3AF05ECB7298509infoc; buvid3=137DCCAF-2D05-49A1-8CD7-9137FF0998AA40958infoc; DedeUserID=287932745; DedeUserID__ckMd5=b7c29df8e71b0a95; SESSDATA=4ac2443a%2C1610788657%2Ce836c*71; bili_jct=43bcb09180437e0c4fbe72be83c055fa; CURRENT_QUALITY=0; LIVE_BUVID=AUTO5515958176620775; bp_t_offset_287932745=418930332671127462; bp_video_offset_287932745=422170949913891418; PVID=4; bfe_id=6f285c892d9d3c1f8f020adad8bed553",
}

detail_url = "https://api.bilibili.com/x/web-interface/card"
other_url = "https://api.bilibili.com/x/space/upstat"
main_url = "https://api.bilibili.com/x/relation/stat"

with open('name_uid.json', 'r', encoding='utf-8') as fp:
    data = json.load(fp)
    up_detail_list = []
    for v in data.values():
        params = {'vmid': v}

        response1 = requests.get(detail_url, headers=headers, params=params)
        response2 = requests.get(other_url, headers=headers, params=params)
        res1 = response1.json()
        res2 = response2.json()

        data1 = res1['data']['card']

        up_detail_dict = {}
        mid = data1['mid']
        name = data1['name']
        fans = data1['fans']
        attention = data1['attention']
        like = res2['data']['likes']
        view = res2['data']['archive']['view']

        up_detail_dict['MID'] = mid
        up_detail_dict['名称'] = name
        up_detail_dict['粉丝数'] = fans
        up_detail_dict['关注数'] = attention
        up_detail_dict['获赞数'] = like
        up_detail_dict['播放数'] = view

        up_detail_list.append(up_detail_dict)

    with open('up_detail.json', 'w', encoding='utf-8') as fp:
        json.dump(up_detail_list, fp, ensure_ascii=False)

