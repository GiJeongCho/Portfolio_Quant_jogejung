import os
import pandas as pd
from datetime import datetime, timedelta
import mpl_finance
import matplotlib.pyplot as plt
import math

def set_index(df):
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d', errors='raise')
    df = df.set_index('time',drop=False)
    return df

os.getcwd()
path = os.getcwd() #주피터 노트북 파일 경로
os_file_list = os.listdir(path) # 내 경로 읽어서 파일 리스트 읽음

All_data_syn = pd.read_csv("All_data_syn.csv")
All_data_syn.sort_values(['time'],ascending= True).reset_index(drop = True) # 시간컬럼으로 맞추기
All_data_syn = set_index(All_data_syn) # 날자 컬럼만 남기기
All_data_syn["time"] = pd.to_datetime(All_data_syn.index)

data_x = pd.read_csv("올랐는지 내렸는지 판단.csv")
data_x['time'] = pd.to_datetime(data_x['time'], format='%Y-%m-%d', errors='raise') # 시간으로 맞추기

All_data_syn = All_data_syn.dropna()
All_data_syn.info()

use_col = list(set(All_data_syn.columns) - {"time"})# 사용할 컬럼들
a = math.floor(len(All_data_syn)*0.2)
b = math.floor(len(All_data_syn)*0.3)

train_all = All_data_syn[:-a]
test_all = All_data_syn[-a:]
validation_all = All_data_syn[-b:-a]

# 9시 05 분 시작이여야함.
train_all = All_data_syn[:-a]
test_all = All_data_syn[All_data_syn["time"].between("2019-05-07","2023-03-07")]
validation_all = All_data_syn[All_data_syn["time"].between("2017-05-24","2019-05-07")]


import mpl_finance
import matplotlib.pyplot as plt
import time

import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import mpl_finance
import math
import seaborn as sns
# import set_matplotlib_hangul
# %matplotlib inline

import tensorflow as tf
import os
import PIL
import shutil

from matplotlib import gridspec

min_data = min(min(All_data_syn["시가 데이터"]),min(All_data_syn["고가데이터"]),min(All_data_syn["저가데이터"]),min(All_data_syn["종가 데이터"]))
max_data = max(max(All_data_syn["시가 데이터"]),max(All_data_syn["고가데이터"]),max(All_data_syn["저가데이터"]),max(All_data_syn["종가 데이터"]))

min_data_abroad = min(All_data_syn["외국인 순매수 수량"])
max_data_abroad = max(All_data_syn["외국인 순매수 수량"])

min_data_volume = min(All_data_syn["거래량 데이터"])
max_data_volume = max(All_data_syn["거래량 데이터"])

def save_png(data_Frame, train_test, data_x, min_data, max_data , min_data_abroad, max_data_abroad, min_data_volume, max_data_volume):
    start_date = data_Frame["time"][0]
    now_data = start_date + timedelta(days=1) - timedelta(hours=1)
    pariod_max = data_Frame["time"].index.max()  # 최종 기간 while 문 끝내기 위함.

    # 기간에 맞는 새 데이터 프레임

    i = 0
    # 1번 돌때마다
    while True:

        df_1 = data_Frame[data_Frame["time"].between(start_date, now_data)]
        try:
            data_1 = df_1[df_1["time"] == df_1["time"].index.max()]
            data_2 = data_x[data_x["time"].between(start_date, now_data)]

        except:
            print("일별 데이터가 없는 경우 ", start_date, now_data, len(df_1[use_col]), len(data_2))
            pass

        if len(df_1[use_col]) == 13 and len(data_2) != 0:  # 실행
            # print("돌고 있는지 확인", i, start_date, now_data, len(df_1[use_col]), len(data_2))

            if float(data_1["종가 데이터"].values) <= float(data_2["종가데이터"]):  # 종가에 상승

                ## 봉차트 / 거래량 차트 구분
                fig = plt.figure(figsize=(15, 8))
                gs = gridspec.GridSpec(nrows=3, ncols=1, height_ratios=[3, 1, 1])

                ## 봉차트 그리기
                ax0 = plt.subplot(gs[0])
                mpl_finance.candlestick2_ohlc(ax0, df_1['시가 데이터'], df_1['고가데이터'], df_1['저가데이터'], df_1['종가 데이터'], width=0.5, colorup='r', colordown='b')
                plt.ylim([min_data, max_data])
                ax0.get_xaxis().set_visible(False)

                ## 거래량차트 그리기
                ax1 = plt.subplot(gs[1])
                plt.ylim([min_data_volume, max_data_volume])
                ax1.bar(df_1["time"], df_1['거래량 데이터'], color='k', width=0.001, align='center')

                ## 거래량차트 그리기
                ax2 = plt.subplot(gs[2])
                plt.ylim([min_data_abroad, max_data_abroad])
                ax2.bar(df_1["time"], df_1['외국인 순매수 수량'], color='k', width=0.001, align='center')

                plt.savefig(path + "\\CNN\\" + train_test + '\\' + train_test + 'O\\cnndata' + str(i) + '.png')
                plt.close(fig)

                print("되고 있는 경유", i, start_date, now_data, len(df_1[use_col]), len(data_2),"O")

            elif float(data_1["종가 데이터"].values) > float(data_2["종가데이터"]):  # 종가에 하락

                ## 봉차트 / 거래량 차트 구분
                fig = plt.figure(figsize=(15, 8))
                gs = gridspec.GridSpec(nrows=3, ncols=1, height_ratios=[3, 1, 1])

                ## 봉차트 그리기
                ax0 = plt.subplot(gs[0])
                mpl_finance.candlestick2_ohlc(ax0, df_1['시가 데이터'], df_1['고가데이터'], df_1['저가데이터'], df_1['종가 데이터'], width=0.5, colorup='r', colordown='b')
                plt.ylim([min_data, max_data])
                ax0.get_xaxis().set_visible(False)

                ## 거래량차트 그리기
                ax1 = plt.subplot(gs[1])
                plt.ylim([min_data_volume, max_data_volume])
                ax1.bar(df_1["time"], df_1['거래량 데이터'], color='k', width=0.001, align='center')

                ## 거래량차트 그리기
                ax2 = plt.subplot(gs[2])
                plt.ylim([min_data_abroad, max_data_abroad])
                ax2.bar(df_1["time"], df_1['외국인 순매수 수량'], color='k', width=0.001, align='center')

                plt.savefig(path + "\\CNN\\" + train_test + '\\' + train_test + 'X\\cnndata' + str(i) + '.png')
                plt.close(fig)

                print("되고 있는 경유", i, start_date, now_data, len(df_1[use_col]), len(data_2),"X")

            else:
                print("놓친 경유", i, start_date, now_data, len(df_1[use_col]), len(data_2), "이미지 파일 저장을 못한 경우?..")

        #         else:  # 실행안함
        #             print(start_date, now_data, "해당 날짜는 데이터가 조금 비어있음.",len(df_1[use_col]), len(data_2))
        #             pass

        start_date = start_date + timedelta(days=1)
        now_data = now_data + timedelta(days=1)
        i = i + 1
        #         time.sleep(0.1)
        # print(pariod_max,now_data)
        if (pariod_max < now_data):  # whlie문 탈출
            break



save_png(train_all,'train',data_x, min_data, max_data , min_data_abroad, max_data_abroad, min_data_volume, max_data_volume)
# 아래 두갠 학습 x
save_png(test_all,'test',data_x, min_data, max_data , min_data_abroad, max_data_abroad, min_data_volume, max_data_volume)
save_png(validation_all ,'validation',data_x, min_data, max_data , min_data_abroad, max_data_abroad, min_data_volume, max_data_volume)


import os
import mpl_finance
import matplotlib.pyplot as plt
import time

# 기본 경로
base_dir = 'C:\\Users\\Happy\\desktop\\professor_kim\\CNN\\CNN'

validation_dir = os.path.join(base_dir+'\\validation')
train_dir = os.path.join(base_dir+'\\train')
test_dir = os.path.join(base_dir+'\\test')

# 훈련용 O/X 이미지 경로
train_o_dir = os.path.join(train_dir+ '\\trainO')
train_x_dir = os.path.join(train_dir+ '\\trainX')
print(train_o_dir, train_x_dir)

# 테스트용 O/X 이미지 경로
test_o_dir = os.path.join(test_dir+ '\\testO')
test_x_dir = os.path.join(test_dir+ '\\testX')
print(test_o_dir, test_x_dir)

# 검증용 O/X 이미지 경로
validation_o_dir = os.path.join(validation_dir+'\\validationO')
validation_x_dir = os.path.join(validation_dir+'\\validationX')
print(validation_o_dir, validation_x_dir)

# 이미지 데이터 전처리
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Image augmentation
# train셋에만 적용
train_datagen = ImageDataGenerator(rescale = 1./255, # 모든 이미지 원소값들을 255로 나누기
                                   # rotation_range=0, # 0~25도 사이에서 임의의 각도로 원본이미지를 회전
                                   # width_shift_range=0, # 0.05범위 내에서 임의의 값만큼 임의의 방향으로 좌우 이동
                                   # height_shift_range=0, # 0.05범위 내에서 임의의 값만큼 임의의 방향으로 상하 이동
                                   # zoom_range=0, # (1-0.2)~(1+0.2) => 0.8~1.2 사이에서 임의의 수치만큼 확대/축소
                                   horizontal_flip=False, # 좌우로 뒤집기
                                   vertical_flip=False,
                                   fill_mode='nearest'
                                  )
# validation 및 test 이미지는 augmentation을 적용하지 않는다.
# augmentation이란 이미지가 부족할 경우 이미지를 위, 아래로 움직이며 데이터 양을 늘리는 과정.
# 모델 성능을 평가할 때에는 이미지 원본을 사용 (rescale만 진행)
validation_datagen = ImageDataGenerator(rescale = 1./255)
test_datagen = ImageDataGenerator(rescale = 1./255)