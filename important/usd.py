from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import csv
import datetime

def word_preprocess(word):
    symbols = [" ", '\n', "\t"]  # make your own list
    for symbol in symbols:
        word = word.replace(symbol, '')
    return word

def Data_Processing(text_data):
    start_point = 0
    data_2 = []
    data_2_append = data_2.append
    for i, v in enumerate(text_data):
        try:
            float(v)
        except:
            end_point = i

            a = text_data[start_point:end_point] # 이 부분 어찌 깔끔하게..?
            try:
                int(a[0][:4])
            except:
                if len(a) >= 4:
                    data_2_append(a)

            start_point = end_point
            pass
    return data_2

def data_to_csv(data_2):
    dic_data = {}

    dic_data["time"] = now.strftime('%Y-%m-%d %H:%M:%S')
    for v in data_2:
        dic_data[v[0]] = v[1]

    try:
        save_state = []
        save_state_append = save_state.append

        key_list = list(data_2.keys())
        for i in key_list:
            save_state_append(dic_data[i])

        # save_state = list(dic_data.values())
        # ======================================== 데이터 쓰는 부분
        # csv파일로 적기 # newline 설정을 안하면 한줄마다 공백있는 줄이 생긴다.
        with open('currency_exchange_data.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(save_state)
    except:
        key_list = list(dic_data.keys())
        columns_name = key_list
        # csv파일로 적기 # newline 설정을 안하면 한줄마다 공백있는 줄이 생긴다.
        with open('currency_exchange_data.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(columns_name)

            save_state = []
        save_state_append = save_state.append
        for i in key_list:
            save_state_append(dic_data[i])
        # ======================================== 데이터 쓰는 부분
        # save_state = list(dic_data.values())

        # csv파일로 적기 # newline 설정을 안하면 한줄마다 공백있는 줄이 생긴다.
        with open('currency_exchange_data.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(save_state)

while True:
    now = datetime.datetime.now()
    html = urlopen("https://www.mibank.me/exchange/saving/index.php?currency=USD")
    bsObject = BeautifulSoup(html, "html.parser")
    # =============== 크롤링 부분
    td_data = []
    td_data_append = td_data.append
    for data in bsObject.body.find_all('td'):
        td_data_append(data.text)

    text_data = []
    for line in td_data:
        # print(line)
        word = word_preprocess(line)
        if len(word) > 2:  # ("]" in line) == False and
            text_data.append(word)
    # =============== 크롤링 부분

    del text_data[0]

    data_2 = Data_Processing(text_data) # 데이터 저장하기 쉽게 가공. @ 이 부분 속도 빠르게 개선 가능해 보임
    data_to_csv(data_2) # 데이터 csv에 저장

    time.sleep(1)