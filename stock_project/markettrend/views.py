from django.shortcuts import render
import time
import requests as r
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.offline as opy

def markettrend(request):
    dtime = int(float(time.time())*1000)
    url = 'https://mis.twse.com.tw/stock/data/mis_ohlc_TSE.txt?_='+str(dtime)
    res = r.get(url)
    jd = res.json()['ohlcArray']
    columns = ['c','s','ts','t']
    df = pd.DataFrame(jd, columns=columns)
    df.columns =['加權指數','成交金額','時間','日期']
    df['加權指數'] = pd.to_numeric(df['加權指數'])
    df['成交金額'] = df['成交金額'].astype(float)
    df['時間']=df['時間'].replace(np.nan,'133000')
    yesterday =res.json()['infoArray']
    df2=pd.DataFrame([yesterday[0]['y'], 0 , '0900' ,np.nan]).T
    #df.loc[0]=[yesterday[0]['y'], 0 , '0900' ,np.nan]
    df2.columns =df.columns
    df=pd.concat([df2,df],axis=0,ignore_index=True)
    allMoney=0
    for i in range(len(df['加權指數'])):#注意
            df['時間'][i]=df['時間'][i][0:2]+':'+df['時間'][i][2:4] 
            df['成交金額'][i]=df['成交金額'][i]/100 
            allMoney+=df['成交金額'][i]
            allMoney=round(allMoney,2)
    abc=str(df['加權指數'][len(df['加權指數'])-1])
    
    trace1 = go.Bar(
        name='成交金額(億)',
        x=df['時間'],
        y=df['成交金額'],
    )
    trace2 = go.Scatter(
        name='加權指數',
        x=df['時間'],
        y=df['加權指數'],
        yaxis="y2"
    )
    
    data = [trace1, trace2,]
    layout = go.Layout(
        yaxis=dict(
            domain=[0, 0.5]
        ),
        legend=dict(
            traceorder="reversed"
        ),
        yaxis2=dict(
            domain=[0.5, 1]
        ),
        title='加權指數:'+abc,
    )
    fig =go.Figure(data=data, layout=layout)
    fig.update_xaxes(tick0='0900',dtick=5)
    fig.update_yaxes(exponentformat="none")
    fig.update_layout(hovermode="x unified",height=600)
    div = opy.plot(fig, auto_open=False, output_type='div')
    efg=float(abc)-float(df['加權指數'][0])
    hij=str(round(efg/float(abc),2))+'%'
    stock_data=[]
    stock_data_2=[]
    stock_data.append(abc)
    stock_data.append('%.2f' %efg)
    stock_data.append(hij)
    stock_data_2.append(allMoney)
    return render(request,'markettrend/markettrend.html',{'fig':div,'stock_data':stock_data,'stock_data_2':stock_data_2})