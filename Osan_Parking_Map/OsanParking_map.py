from branca.element import IFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
import matplotlib
from pandas.core import frame

matplotlib.rc('font', family="appleGothic")

df = pd.read_excel('/Users/qkrdnjsrl/Desktop/공모전 준비/오산시 주차장 현황 위도경도 포함.xlsx', engine = 'openpyxl')

df.drop(columns=['구분', '주소', '면적'], inplace=True)
df.rename(columns={'Unnamed: 1':'주차장'}, inplace = True)
df.set_index('주차장', inplace=True)
print(df)

df.loc['운암공영주차장', '현재차량'] = 350
df.loc['궐동공영주차장', '현재차량'] = 124
df.loc['어울림(복개천)공영주차장', '현재차량'] = 100
df.loc['시청부설주차장', '현재차량'] = 150
df.loc['오산역환승주차장', '현재차량'] = 215
df.loc['오산역 제2환승주차장', '현재차량'] = 90
df.loc['오색시장 제1공영주차장', '현재차량'] = 108
df.loc['오산대역환승주차장', '현재차량'] = 30
df.loc['세마역환승주차장', '현재차량'] = 62
df.loc['오색시장 제2공영주차장', '현재차량'] = 160
df.loc['문화의거리 임시공영주차장', '현재차량'] = 20
df.loc['문화의거리 제2공영주차장', '현재차량'] = 5
df.loc['원동복개도로', '현재차량'] = 53
df.loc['철도변노상주차장', '현재차량'] = 30

df['비율'] = 20

df.loc[0:,'비율'] =  df.loc[:,'현재차량'] / df.loc[:,'면수']
print(df)

today_parking = folium.Map(location=[37.146351784415984, 127.07061341642824], zoom_start=15)

for name, lat, lng, radian, incar, out_car in zip(df.index, df['위도'], df['경도'], df['비율'], df['현재차량'], df['면수']):
    iframe = name + " 정보 : <br>" + "총 주차공간 : " + str(out_car) + "<br>" + '주차 가능한 공간 : ' + str(out_car - incar)[:-2]+ "대"
    popup = folium.Popup(iframe, min_width= 100, max_width= 500)
    if radian > 0.8:
        folium.CircleMarker([lat, lng],
                            radius=17,
                            fill_color = 'red',
                            color = None,
                            fill_opacity = radian,
                            popup=popup
                            ).add_to(today_parking)
    elif radian > 0.6:
        folium.CircleMarker([lat, lng],
                            radius=17,
                            fill_color = 'blue',
                            color = None,
                            fill_opacity = radian,
                            popup=popup).add_to(today_parking)
    else:
        folium.CircleMarker([lat, lng],
                            radius=17,
                            color = None,
                            fill_color = 'green',
                            fill_opacity = radian*2,
                            popup=popup).add_to(today_parking)

today_parking.save('/Users/qkrdnjsrl/Desktop/공모전 준비/today_plat1.html')

# # 분수의 값을 넣어 1에 가까울수록 혼합 1이면 포화
# # 2이면 미포화 상태