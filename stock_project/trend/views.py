from django.shortcuts import render,redirect
from trend.forms import trend_forms
import datetime
import requests
import pandas as pd
import plotly.express as px
import other

def trend(request):
    return render(request,'trend/trend.html',{'who':trend_forms()})
# def trend_stock(request):
#     targets=request.GET.get("trend_stock")
#     request.session['trend_stock']=targets
#     today = datetime.datetime.now() 
#     nowtime=" 更新時間:" + today.strftime('%X')[0:5]
#     have=other.sql(targets)
#     if have:
#         stock_number=have[0]
#         stock_name=have[1]
#     else:
#         return redirect('trend:trend')
#     res = requests.get('https://tw.stock.yahoo.com/_td-stock/api/resource/FinanceChartService.ApacLibraCharts;autoRefresh=1653627795519;symbols=%5B%22'+stock_number+'.TW%22%5D;type=tick?bkt=&device=desktop&ecma=modern&feature=ecmaModern%2CuseVersionSwitch%2CuseNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=a3olkn1h90moe&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.1295&returnMeta=true')
#     title_text=stock_number+' '+stock_name
#     jd = res.json()['data']
#     close = jd[0]['chart']['indicators']['quote'][0]['close']
#     volume = jd[0]['chart']['indicators']['quote'][0]['volume']
#     timestamp = jd[0]['chart']['timestamp']
#     df = pd.DataFrame({'timestamp':timestamp, '價':close, 'volume':volume,},)
#     df['日期']=(pd.to_datetime(df['timestamp'] + 3600 * 8, unit='s'))
#     df['日期']=pd.to_datetime(df['日期'],format ='%Y-%m-%d%H:%M')
#     df['時間']=df['日期'].dt.strftime("%H:%M")
#
#     fig = px.line(df,x='時間',y ='價',title=title_text+nowtime,line_shape='linear',hover_data={'量':df.volume},width=640)
#     fig.update_xaxes(title_text='時間')
#     fig.update_yaxes(title_text='價格')
#     fig.update_layout(hovermode="x")
#     fig.update_traces(connectgaps=True)
#     newfig="<div>"+fig.to_html()+"</div>"
#     return render(request,'trend/trend.html',{'who':trend_forms(),'newfig':newfig,})
def addtrend(request):
    return render(request,'trend/trend2.html',{'who2':trend_forms()})
def trend2(request):
    target=request.GET.get("ts")
    request.session['ts']=target
    today = datetime.datetime.now() 
    nowtime=" 更新時間:" + today.strftime('%X')[0:5]
    have=other.sql(target)
    stock_number=have[0]
    stock_name=have[1]
    res = requests.get('https://tw.stock.yahoo.com/_td-stock/api/resource/FinanceChartService.ApacLibraCharts;autoRefresh=1653627795519;symbols=%5B%22'+stock_number+'.TW%22%5D;type=tick?bkt=&device=desktop&ecma=modern&feature=ecmaModern%2CuseVersionSwitch%2CuseNewQuoteTabColor&intl=tw&lang=zh-Hant-TW&partner=none&prid=a3olkn1h90moe&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.1295&returnMeta=true')
    title_text=stock_number+' '+stock_name
    jd = res.json()['data']
    close = jd[0]['chart']['indicators']['quote'][0]['close']
    volume = jd[0]['chart']['indicators']['quote'][0]['volume']
    timestamp = jd[0]['chart']['timestamp']
    df = pd.DataFrame({'timestamp':timestamp, '價':close, 'volume':volume,},)
    df['日期']=(pd.to_datetime(df['timestamp'] + 3600 * 8, unit='s'))
    df['日期']=pd.to_datetime(df['日期'],format ='%Y-%m-%d%H:%M')
    df['時間']=df['日期'].dt.strftime("%H:%M")

    fig = px.line(df,x='時間',y ='價',title=title_text+nowtime,line_shape='linear',hover_data={'量':df.volume},width=640)
    fig.update_xaxes(title_text='時間')
    fig.update_yaxes(title_text='價格')
    fig.update_layout(hovermode="x")
    fig.update_traces(connectgaps=True)
    newfig=fig.to_html()
    return render(request,'trend/trend_pic.html',{'newfig':newfig,})