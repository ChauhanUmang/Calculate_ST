import pandas as pd

df = pd.read_excel('Test.xlsx')
pd.set_option('display.max_columns', None)
ATR_Period = 7
# print(df.head())

# Calculation of TR
df['h-l'] = (df['High'] - (df['Low']).abs())
df['h-pc'] = (df['High'] - df['Close'].shift()).abs()
df['l-pc'] = (df['Low'] - df['Close'].shift()).abs()
df['TR'] = df[["h-l", "h-pc", "l-pc"]].max(axis=1)
df.drop(["h-l", "h-pc", "l-pc"], inplace=True, axis=1)

# Manual Values of ATR
df.at[0, 'ATR'] = 80.39
df.at[1, 'ATR'] = 73.66
df.at[2, 'ATR'] = 69.73
df.at[3, 'ATR'] = 63.65
df.at[4, 'ATR'] = 75.31
df.at[5, 'ATR'] = 71.38
df.at[6, 'ATR'] = 71.49

# Automatic calculation of ATR
for i in range(7, len(df)):
    df.loc[i, 'ATR'] = ((df.loc[i - 1, 'ATR'] * (ATR_Period - 1)) + df.loc[i, 'TR']) / ATR_Period

df['BUB'] = (df['High'] + df['Low']) / 2 + (3 * df['ATR'])
df['BLB'] = (df['High'] + df['Low']) / 2 - (3 * df['ATR'])

df['FUB'] = 0.00
df['FLB'] = 0.00
df['Supertrend'] = 0.00

for i in range(1, len(df)):
    df.at[i, 'FUB'] = df.at[i, 'BUB'] if df.at[i, 'BUB'] < df.at[i - 1, 'FUB'] or df.at[i - 1, 'Close'] > \
                                         df.at[i - 1, 'FUB'] else df.at[i - 1, 'FUB']

    df.at[i, 'FLB'] = df.at[i, 'BLB'] if df.at[i, 'BLB'] > df.at[i - 1, 'FLB'] or df.at[i - 1, 'Close'] < \
                                         df.at[i - 1, 'FLB'] else df.at[i - 1, 'FLB']

for i in range(1, len(df)):
    df.at[i, 'Supertrend'] = df.at[i, 'FUB'] if df.at[i-1, 'Supertrend'] == df.at[i-1, 'FUB'] and df.at[i, 'Close'] < \
                                                df.at[i, 'FUB'] else \
                             df.at[i, 'FLB'] if df.at[i-1, 'Supertrend'] == df.at[i-1, 'FUB'] and df.at[i, 'Close'] > \
                                                df.at[i, 'FUB'] else \
                             df.at[i, 'FLB'] if df.at[i-1, 'Supertrend'] == df.at[i-1, 'FLB'] and df.at[i, 'Close'] > \
                                                df.at[i, 'FLB'] else \
                             df.at[i, 'FUB'] if df.at[i-1, 'Supertrend'] == df.at[i-1, 'FLB'] and df.at[i, 'Close'] < \
                                                df.at[i, 'FLB'] else 0.00

for i in range(6, len(df)):
    df.at[i, 'Color'] = 'Red' if df.at[i, 'Supertrend'] == df.at[i, 'FUB'] else 'Green'

df.to_excel('Test_Result.xlsx', index=False)
