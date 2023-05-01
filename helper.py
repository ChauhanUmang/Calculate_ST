import pandas as pd
import datetime


def maximum(a, b, c):
    lis = [a, b, c]
    return max(lis)


def check_trigger(i, df):
    if df.at[i, 'Color'] == df.at[i-1, 'Color']:
        # check time here if time is 9:24 and previous three candle have signal as '' then at
        # 9:24 send signal according to color
        istime924 = check_9_24(str(df.at[i, 'Date']))

        if istime924:
            # check previous three candles
            return check_past_3_candles(i, df)

        return ''
    else:
        if df.at[i, 'Color'] == 'Red':
            return 'CE SELL'
        else:
            return 'PE SELL'


def check_9_24(timestamp):
    dt = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    if dt.hour == 9 and dt.minute == 24:
        return True
    else:
        return False


def check_past_3_candles(i, df):
    lst = ['CE SELL', 'PE SELL']
    if df.at[i-1, 'Signal'] in lst or df.at[i-2, 'Signal'] in lst or df.at[i-3, 'Signal'] in lst:
        return ''
    else:
        if df.at[i, 'Color'] == 'Red':
            return 'CE SELL'
        else:
            return 'PE SELL'
