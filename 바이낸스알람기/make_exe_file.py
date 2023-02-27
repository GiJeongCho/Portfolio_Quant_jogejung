import time
import pandas as pd
from IPython.display import clear_output

def bin_sym_names():  # 바이낸스 심볼명들 도출
    result = requests.get('https://api.binance.com/api/v3/ticker/price')
    js = result.json()
    symbols = [x['symbol'] for x in js]
    symbols_usdt = [x for x in symbols if 'USDT' in x]  # 끝이 USDT로 끝나는 심볼들, ['BTCUSDT', 'ETHUSDT', ...]
    return symbols_usdt


def bin_get_data(start_date, end_date, symbol, interval):  # 시작일 , 종료일 , 심볼명 , 분/시간/일/주/월 데이터 선택
    URL = 'https://api.binance.com/api/v3/klines'

    COLUMNS = ['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'quote_av', 'trades',
               'tb_base_av', 'tb_quote_av', 'ignore']
    data = []

    start = int(time.mktime(datetime.strptime(start_date + ' 00:00', '%Y-%m-%d %H:%M').timetuple())) * 1000
    end = int(time.mktime(datetime.strptime(end_date + ' 23:59', '%Y-%m-%d %H:%M').timetuple())) * 1000
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': 1000,
        'startTime': start,
        'endTime': end
    }

    while start < end:
        #         print(datetime.fromtimestamp(start // 1000))
        params['startTime'] = start
        result = requests.get(URL, params=params)
        js = result.json()
        if not js:
            break
        data.extend(js)  # result에 저장
        start = js[-1][0] + 60000  # 다음 step으로
    # 전처리
    if not data:  # 해당 기간에 데이터가 없는 경우
        print('해당 기간에 일치하는 데이터가 없습니다.')
        return -1
    df = pd.DataFrame(data)
    df.columns = COLUMNS
    df['Open_time'] = df.apply(lambda x: datetime.fromtimestamp(x['Open_time'] // 1000), axis=1)
    df = df.drop(columns=['Close_time', 'ignore'])
    df['Symbol'] = symbol
    df.loc[:, 'Open':'tb_quote_av'] = df.loc[:, 'Open':'tb_quote_av'].astype(float)  # string to float
    df['trades'] = df['trades'].astype(int)

    # df['Open_time'] = pd.to_datetime(df['Open_time'], format='%Y-%m-%d %H:%M:%S', errors='raise')
    # df = df.set_index('Open_time',drop=True)
    return df

import telegram #pip install python-telegram-bot
import requests

def Telegramchat(text): # @ 병석이형
    telegram_token = '5683819516:AAHtOJwnhw3oEbtgc7fxdpHtmg6r9_pTCdc'
    telegram_chat_id = '5503730871'
    bot = telegram.Bot(token = telegram_token)

    url = 'https://api.telegram.org/bot'+telegram_token+'/sendMessage?chat_id='+telegram_chat_id+'&text='+text
    return requests.get(url)


def removeAllOccur(l, i):
    try:
        while True: l.remove(i)
    except ValueError:
        pass


from datetime import datetime
import datetime as dt


# def about_time_start(day_or_time=10):  # 뺼 날자
#     now_time = datetime.now()
#     diff_days = dt.timedelta(days=day_or_time)  # @ 일단 day로 되어 있음.
#
#     start_date = (now_time - diff_days).strftime("%Y-%m-%d")  # 오늘 부터 몇 일 전
#     now_day_time = now_time.strftime("%Y-%m-%d")  # 현재 날짜
#
#     return now_day_time, start_date  # start_date = now_time - diff_days

def about_time_start_inday_(day_or_time=4):  # 뺼 날자
    now_time = datetime.now()
    diff_days = dt.timedelta(hours=day_or_time)  # dt.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
    #     diff_days = dt.timedelta(days=day_or_time) # @ 일단 day로 되어 있음.

    start_date = (now_time - diff_days).strftime("%Y-%m-%d")  # 오늘 부터 몇 일 전
    now_day_time = now_time.strftime("%Y-%m-%d")  # 현재 날짜

    return now_day_time, start_date  # start_date = now_time - diff_days

# 단순 이동 평균(Simple Moving Average, SMA)
def SMA(data, period=30, column='Close'):
    return data[column].rolling(window=period).mean()

def Bollinger_Band(df, period=30, column='Close', multiplier=2):
    df['Bollinger_Band_' + str(period) + '_mid_' + str(multiplier)] = df['Close'].rolling(period).mean()  # 20일 이동평균
    df['stddev'] = df['Close'].rolling(period).std()  # 20일 이동표준편차
    df['Bollinger_Band_' + str(period) + 'upper_' + str(multiplier)] = df['Bollinger_Band_' + str(period) + '_mid_' + str(multiplier)] + multiplier * df['stddev']  # 상단밴드
    df['Bollinger_Band_' + str(period) + 'lower_' + str(multiplier)] = df['Bollinger_Band_' + str(period) + '_mid_' + str(multiplier)] - multiplier * df['stddev']  # 하단밴드
    del df['stddev']

    return df

def one_look_equilibrium_chart(df, one_look_equilibrium_chart_Conversion_Line_period, one_look_equilibrium_chart_base_line_period, one_look_equilibrium_chart_lagging, one_look_equilibrium_chart_displacement):  # 일목균형표
    high_prices = df['High']
    close_prices = df['Close']
    low_prices = df['Low']
    dates = df.index

    nine_period_high = df['High'].rolling(window=one_look_equilibrium_chart_Conversion_Line_period).max()
    nine_period_low = df['Low'].rolling(window=one_look_equilibrium_chart_Conversion_Line_period).min()
    df['전환선'] = (nine_period_high + nine_period_low) / 2  # 전환선

    period26_high = high_prices.rolling(window=one_look_equilibrium_chart_base_line_period).max()
    period26_low = low_prices.rolling(window=one_look_equilibrium_chart_base_line_period).min()
    df['기준선'] = (period26_high + period26_low) / 2  # 기준선

    df['BB_선행_span_a'] = ((df['전환선'] + df['기준선']) / 2).shift(one_look_equilibrium_chart_base_line_period)  # 선행스팬 1

    period52_high = high_prices.rolling(window=one_look_equilibrium_chart_lagging).max()
    period52_low = low_prices.rolling(window=one_look_equilibrium_chart_lagging).min()
    df['BB_선행_span_b'] = ((period52_high + period52_low) / 2).shift(one_look_equilibrium_chart_base_line_period)  # 선행스팬 2

    df['BB_후행_span'] = close_prices.shift(-one_look_equilibrium_chart_displacement)  # 후행스팬

    #     print('전환선: ',df['전환선'].iloc[-1])
    #     print('기준선: ',df['기준선'].iloc[-1])
    #     print('후행스팬: ',df['후행_span'].iloc[-one_look_equilibrium_chart_displacement-1])
    #     print('선행스팬1: ',df['선행_span_a'].iloc[-1])
    #     print('선행스팬2: ',df['선행_span_b'].iloc[-1])
    #     del df["기준선"]
    #     del df["전환선"]

    return df


def envelop(df, column='Close', window=40, gap=10):
    ma20 = df[column].rolling(window).mean()
    idx = ma20.index
    en_high, en_low = [], []
    for i in range(len(ma20)):
        en_high.append(ma20[i] + ((ma20[i] * gap) / 100))
        en_low.append(ma20[i] - ((ma20[i] * gap) / 100))
    df["envelop_high" + '_' + str(window) + '_' + str(gap)] = pd.Series(en_high, index=idx)
    df["envelop_low" + '_' + str(window) + '_' + str(gap)] = pd.Series(en_low, index=idx)

    return df


def close_or_open_or_mix(a):  # @시시 종 은 아직.
    if a == "시가":
        return "Open"
    elif a == "종가":
        return "Close"


# class PSAR:
#     def __init__(self, init_af=0.02, max_af=0.2, af_step=0.02):
#         self.max_af = max_af
#         self.init_af = init_af
#         self.af = init_af
#         self.af_step = af_step
#         self.extreme_point = None
#         self.high_price_trend = []
#         self.low_price_trend = []
#         self.high_price_window = deque(maxlen=2)
#         self.low_price_window = deque(maxlen=2)
#
#         # Lists to track results
#         self.psar_list = []
#         self.af_list = []
#         self.ep_list = []
#         self.high_list = []
#         self.low_list = []
#         self.trend_list = []
#         self._num_days = 0
#
#     def calcPSAR(self, high, low):
#         if self._num_days >= 3:
#             psar = self._calcPSAR()
#         else:
#             psar = self._initPSARVals(high, low)
#
#         psar = self._updateCurrentVals(psar, high, low)
#         self._num_days += 1
#
#         return psar
#
#     def _initPSARVals(self, high, low):
#         if len(self.low_price_window) <= 1:
#             self.trend = None
#             self.extreme_point = high
#             return None
#
#         if self.high_price_window[0] < self.high_price_window[1]:
#             self.trend = 1
#             psar = min(self.low_price_window)
#             self.extreme_point = max(self.high_price_window)
#         else:
#             self.trend = 0
#             psar = max(self.high_price_window)
#             self.extreme_point = min(self.low_price_window)
#
#         return psar
#
#     def _calcPSAR(self):
#         prev_psar = self.psar_list[-1]
#         if self.trend == 1:  # Up
#             psar = prev_psar + self.af * (self.extreme_point - prev_psar)
#             psar = min(psar, min(self.low_price_window))
#         else:
#             psar = prev_psar - self.af * (prev_psar - self.extreme_point)
#             psar = max(psar, max(self.high_price_window))
#
#         return psar
#
#     def _updateCurrentVals(self, psar, high, low):
#
#         if self.trend == 1:
#             self.high_price_trend.append(high)
#         elif self.trend == 0:
#             self.low_price_trend.append(low)
#
#         psar = self._trendReversal(psar, high, low)
#
#         self.psar_list.append(psar)
#         self.af_list.append(self.af)
#         self.ep_list.append(self.extreme_point)
#         self.high_list.append(high)
#         self.low_list.append(low)
#         self.high_price_window.append(high)
#         self.low_price_window.append(low)
#         self.trend_list.append(self.trend)
#
#         return psar
#
#     def _trendReversal(self, psar, high, low):
#         # Checks for reversals
#         reversal = False
#         if self.trend == 1 and psar > low:
#             self.trend = 0
#             psar = max(self.high_price_trend)
#             self.extreme_point = low
#             reversal = True
#         elif self.trend == 0 and psar < high:
#             self.trend = 1
#             psar = min(self.low_price_trend)
#             self.extreme_point = high
#             reversal = True
#
#         if reversal:
#             self.af = self.init_af
#             self.high_price_trend.clear()
#             self.low_price_trend.clear()
#         else:
#
#             if high > self.extreme_point and self.trend == 1:
#                 self.af = min(self.af + self.af_step, self.max_af)
#                 self.extreme_point = high
#             elif low < self.extreme_point and self.trend == 0:
#                 self.af = min(self.af + self.af_step, self.max_af)
#                 self.extreme_point = low
#
#         return psar
#
#
# def PSAR_SAR(data, start, increment, Maximun):
#     indic = PSAR()
#
#     data['PSAR'] = data.apply(
#         lambda x: indic.calcPSAR(x['High'], x['Low']), axis=1)
#
#     # Add supporting data
#     data['EP'] = indic.ep_list
#     data['Trend'] = indic.trend_list
#     data['AF'] = indic.af_list
#
#     data["PSAR_SAR" + '_' + str(increment) + '_' + str(Maximun)] = data['PSAR']
#     return data


import warnings
warnings.filterwarnings(action='ignore')

## 일봉기준.

# 바이낸스 상장 심볼명 (현물) 데이터 가져옮
bin_sym_name = bin_sym_names() # bin_sym_name = symbols_usdt

day_or_time = 4
# 시작~끝일 데이터 가져옮
end_date, start_date = about_time_start_inday_(day_or_time = day_or_time + 1)

start_date = str(start_date)#'2017-01-01' # 시작일 (2017 년도 부터 가능)
end_date = str(end_date)#'2022-12-31' # 종료일
interval = "30m"  #  '1d','4h',"1m"

try:
    api_limit = ((160000 / 24) / 60) / 60  # 초당 보낼 수 있는 요청 주문수. # 하루 160000
    data = {}

    while True:
        time_sleep_secend = len(bin_sym_name) / api_limit
        # for sym_i in range(len(bin_sym_name)):
        for sym_i in bin_sym_name:

            symbol = sym_i  # 숫자만 바꾸면 다른 코인 데이터 가져롬
            print(symbol)
            # close_or_open = close_or_open_or_mix(str(input()))#시가 / 종가 기준..
            close_or_open = close_or_open_or_mix("종가")  # 시가 / 종가 기준..
            data[symbol] = bin_get_data(start_date, end_date, symbol, interval)  # @@ 모든데이터 data에 저장하기 위해 딕셔너리 형태로 받음. 추후에 변경 가능

            try:
                data[symbol] = bin_get_data(start_date, end_date, symbol, interval)  # @@ 모든데이터 data에 저장하기 위해 딕셔너리 형태로 받음. 추후에 변경 가능
                ### 표 적용.
                # WINDOW = [6, 20 ,37 , 74 ,149] # 이평선 여러개 도출
                # for WINDOW_i in WINDOW:
                #     data[symbol]["단순이동평균_"+str(close_or_open)+str(WINDOW_i)] = SMA(data[symbol], period=WINDOW_i, column=close_or_open)

                # 일목균형표

                # one_look_equilibrium_chart_Conversion_Line_period = 12 # == window
                # one_look_equilibrium_chart_base_line_period = 37
                # one_look_equilibrium_chart_lagging = 74 # 선행 스팬 기간
                # one_look_equilibrium_chart_displacement = 37 #후행스팬기간?

                # one_look_equilibrium_chart(data[symbol],one_look_equilibrium_chart_Conversion_Line_period,one_look_equilibrium_chart_base_line_period,one_look_equilibrium_chart_lagging,one_look_equilibrium_chart_displacement)

                BB_period = 20  # 볼벤
                BB_multiplier = 2  # 볼벤 승수 (std * BB_multiplier)
                Bollinger_Band(data[symbol], period=BB_period, column=close_or_open, multiplier=BB_multiplier)

                window = 37
                gap = 4.7
                envelop(data[symbol], column=close_or_open, window=window, gap=gap)

                window = 37
                gap = 3.8
                envelop(data[symbol], column=close_or_open, window=window, gap=gap)

                # 파리볼릭 SAR
                start = 0.017
                increment = 0.017
                Maximun = 0.17
                # PSAR_SAR(data[symbol], start, increment, Maximun)

                # 주가데이터 .
                df = data[symbol].copy()

                BB_nearing_per_upper = 0.02  # 주가 근접할 %
                BB_nearing_per_lower = 0  # 주가 근접할 %
                envelop_nearing_per_upper = 0.02  # 주가 근접할 %

                diff_day = day_or_time  # 몇일 기준으로 볼것인지

                df_1 = df.loc[df['Open_time'].between((df.iloc[-1:, ]["Open_time"] - dt.timedelta(days=diff_day)).values[0], df.iloc[-1:, ]["Open_time"].values[0])]

                # 일봉상 기준..
                logic_1 = df_1["Bollinger_Band_20upper_2"] * (1 - BB_nearing_per_upper) > df_1["Close"]  # 볼벤 20 , 2 상한선 근접 or 돌파
                #     print(sum(logic_1))
                logic_1_1 = sum(logic_1) > 1

                logic_2 = df_1["envelop_high_37_4.7"] * (1 - envelop_nearing_per_upper) > df_1["Close"]  # 엔벨로프 37,4.7 상한선 근접 or 돌파
                #     print(sum(logic_2))
                logic_2_1 = sum(logic_2) > 1

                logic_3 = df_1["envelop_high_37_3.8"] * (1 - envelop_nearing_per_upper) > df_1["Close"]  # 엔벨로프 37, 3.8 상한선 돌파
                #     print(sum(logic_3))
                logic_3_1 = sum(logic_3) > 1

                # logic_4 = df_1["Bollinger_Band_20lower_2"] * (1-BB_nearing_per_lower) >df_1["Low"] #엔벨로프 37, 3.8 상한선 돌파
                logic_4 = df_1["Bollinger_Band_20lower_2"] * (1 - BB_nearing_per_lower) > df_1["Close"]  # 엔벨로프 37, 3.8 상한선 돌파
                #     print(sum(logic_4))
                logic_4_1 = sum(logic_4) > 1

                # logic_5 = (  # 파라볼릭.
                #         df_1["Trend"].diff().value_counts()[1] > 2 and  # 상승추세 2번
                #         df_1["Trend"].diff().value_counts()[-1] > 1 and  # 하락추세 1번
                #         1 == df_1.iloc[-1:].Trend.values[0]  # 지금은 상승중
                # )  # 하락추세 1번 # 지금은 상승중

                # if sum([logic_1_1, logic_2_1, logic_3_1, logic_4_1, logic_5]) == 4:
                if sum([logic_1_1, logic_2_1, logic_3_1, logic_4_1]) == 4:
                    send_text = str("심볼명 :" + symbol + " "
                                                       "logic_1 = " + str(sum(logic_1)) + " "
                                                                                          "logic_2 = " + str(sum(logic_2)) + " "
                                                                                                                             "logic_3 = " + str(sum(logic_3)) + " "
                                                                                                                                                                "logic_4 = " + str(sum(logic_4)) + " "
                                                                                                                                                                                                   # "logic_5 = " + str((logic_5))
                                    )
                    response = Telegramchat(send_text)
                    print(send_text)
            except:
                removeAllOccur(bin_sym_name, symbol)
                pass

        #         time.sleep(5)
        time.sleep(time_sleep_secend)
        clear_output(wait=True)

except:
    send_text = "봇 종료"
    response = Telegramchat(send_text)