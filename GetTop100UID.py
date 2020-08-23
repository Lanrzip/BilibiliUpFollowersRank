"""
此代码利用爬取的名称获得与之对应的UID
"""

import requests
import re
import json
from lxml import etree


with open('top_100_up_list.txt', 'r', encoding='utf-8') as fp:
    up_list = fp.readlines()

up_dict = {}
for up in up_list:
    up = up.strip()
    response = requests.get(f"https://search.bilibili.com/all?keyword={up}")
    content = response.content.decode('utf-8')
    html = etree.HTML(content)
    up_url = html.xpath("//div[@class='up-face']/a/@href")[0]
    ret = re.search(r"\d+", up_url)
    uid = ret.group()
    up_dict[up] = uid


with open('name_uid.json', 'w', encoding='utf-8') as fp:
    json.dump(up_dict, fp, ensure_ascii=False)
