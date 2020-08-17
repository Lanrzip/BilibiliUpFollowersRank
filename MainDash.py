import json
import time
from threading import Thread

import requests
import plotly_express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output


external_stylesheets = [
    # Dash CSS
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Loading screen CSS
    'https://codepen.io/chriddyp/pen/brPBPO.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "cookie": "rpdid=|(k|R~|))kY)0J'ulmRm~kkYu; CURRENT_FNVAL=16; _uuid=E1401EB7-6163-5FAF-0810-6B3AF05ECB7298509infoc; buvid3=137DCCAF-2D05-49A1-8CD7-9137FF0998AA40958infoc; DedeUserID=287932745; DedeUserID__ckMd5=b7c29df8e71b0a95; SESSDATA=4ac2443a%2C1610788657%2Ce836c*71; bili_jct=43bcb09180437e0c4fbe72be83c055fa; CURRENT_QUALITY=0; LIVE_BUVID=AUTO5515958176620775; bp_t_offset_287932745=418930332671127462; PVID=4; bp_video_offset_287932745=422854322163518803; bfe_id=5db70a86bd1cbe8a88817507134f7bb5",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"

}
main_url = "https://api.bilibili.com/x/relation/stat"

with open('name_uid.json', 'r', encoding='utf-8') as fp:
    name_uid = json.load(fp)



app.layout = html.Div([
    dcc.Graph(
        id='graph',
    ),
    dcc.Interval(
        id='update',
        interval=86400000,
        n_intervals=0
    )
])


@app.callback(Output('graph','figure'), [Input('update','n_intervals')])
def update_graph(n):
    up_detail_list = []

    def parse_main_url(name, mid):
        params = {'vmid': mid}

        response = requests.get(main_url, headers=headers, params=params)
        res = response.json()

        mid = res['data']['mid']
        follower = res['data']['follower']

        up_detail_dict = {}
        up_detail_dict['VMID'] = mid
        up_detail_dict['名称'] = name
        up_detail_dict['粉丝数'] = follower
        up_detail_list.append(up_detail_dict)

    for k, v in name_uid.items():
        t = Thread(target=parse_main_url, args=(k, v), daemon=True)
        t.start()

    time.sleep(2)

    data = pd.DataFrame(up_detail_list)

    df = data.sort_values(by='粉丝数', ascending=False).iloc[:25, :]
    fig = px.bar(df, '粉丝数', '名称', color='名称',
                 text='粉丝数', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(width=1450, height=800)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
