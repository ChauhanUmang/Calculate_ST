import pandas as pd
import helper

df = pd.read_excel('Test_v1.xlsx')

entry_df = pd.read_excel('Entry.xlsx')

pd.set_option('display.max_columns', None)
ATR_Period = 7
Multiplier = 3
PreviousClose = 43038.5
PreviousATR = 71.49
PreviousFUB = 43132.48
PreviousFLB = 42844.43
PreviousSupertrend = 43132.48
PreviousColor = 'Red'
NewColor = 'Red'

df['FUB'] = 0.00
df['FLB'] = 0.00
df['Supertrend'] = 0.00

for i in range(0, len(df)):
    if i == 0:
        h_l = abs(df.at[i, 'High'] - df.at[i, 'Low'])
        h_pc = abs(df.at[i, 'High'] - PreviousClose)
        l_pc = abs(df.at[i, 'Low'] - PreviousClose)
        df.at[i, 'TR'] = helper.maximum(h_l, h_pc, l_pc)

        df.at[i, 'ATR'] = ((PreviousATR * (ATR_Period - 1)) + df.at[i, 'TR']) / ATR_Period
        df.at[i, 'BUB'] = (df.at[i, 'High'] + df.at[i, 'Low']) / 2 + (Multiplier * df.at[i, 'ATR'])
        df.at[i, 'BLB'] = (df.at[i, 'High'] + df.at[i, 'Low']) / 2 - (Multiplier * df.at[i, 'ATR'])

        df.at[i, 'FUB'] = df.at[i, 'BUB'] if df.at[i, 'BUB'] < PreviousFUB or PreviousClose > PreviousFUB \
            else PreviousFUB

        df.at[i, 'FLB'] = df.at[i, 'BLB'] if df.at[i, 'BLB'] > PreviousFLB or PreviousClose < PreviousFLB \
            else PreviousFLB

        df.at[i, 'Supertrend'] = df.at[i, 'FUB'] if PreviousSupertrend == PreviousFUB and \
                                                    df.at[i, 'Close'] < df.at[i, 'FUB'] else \
            df.at[i, 'FLB'] if PreviousSupertrend == PreviousFUB and \
                               df.at[i, 'Close'] > df.at[i, 'FUB'] else \
                df.at[i, 'FLB'] if PreviousSupertrend == PreviousFLB and \
                                   df.at[i, 'Close'] > df.at[i, 'FLB'] else \
                    df.at[i, 'FUB'] if PreviousSupertrend == PreviousFLB and \
                                       df.at[i, 'Close'] < df.at[i, 'FLB'] else 0.00

        df.at[i, 'Color'] = 'Red' if df.at[i, 'Supertrend'] == df.at[i, 'FUB'] else 'Green'

        NewColor = df.at[i, 'Color']

        df.at[i, 'Signal'] = '' if df.at[i, 'Color']== 'Red' and PreviousColor == 'Red' else \
                             'CE SELL' if df.at[i, 'Color'] == 'Red' and PreviousColor == 'Green' else \
                             '' if df.at[i, 'Color'] == 'Green' and PreviousColor == 'Green' else \
                             'PE SELL' if df.at[i, 'Color'] == 'Green' and PreviousColor == 'Red' else ''

        if PreviousColor == NewColor:
            print('No Change in trend')
        else:
            # create an entry in new df
            entry_df.loc[len(df.index), 'Date'] = df.at[i, 'Date'].dt.date
            entry_df.loc[len(df.index), 'Trigger'] = df.at[i, 'Color']
            entry_df.loc[len(df.index), 'Option'] = df.at[i, 'Signal']
            entry_df.loc[len(df.index), 'Entry_Time'] = df.at[i, 'Date']
            # entry_df.loc[len(df.index), 'Supertrend_change'] =

            print('Hello')
            # update previous color value with new color
    else:
        h_l = abs(df.at[i, 'High'] - df.at[i, 'Low'])
        h_pc = abs(df.at[i, 'High'] - df.at[i - 1, 'Close'])
        l_pc = abs(df.at[i, 'Low'] - df.at[i - 1, 'Close'])
        df.at[i, 'TR'] = helper.maximum(h_l, h_pc, l_pc)

        df.at[i, 'ATR'] = ((df.at[i - 1, 'ATR'] * (ATR_Period - 1)) + df.at[i, 'TR']) / ATR_Period
        df.at[i, 'BUB'] = (df.at[i, 'High'] + df.at[i, 'Low']) / 2 + (Multiplier * df.at[i, 'ATR'])
        df.at[i, 'BLB'] = (df.at[i, 'High'] + df.at[i, 'Low']) / 2 - (Multiplier * df.at[i, 'ATR'])

        df.at[i, 'FUB'] = df.at[i, 'BUB'] if df.at[i, 'BUB'] < df.at[i - 1, 'FUB'] or df.at[i - 1, 'Close'] > \
                                             df.at[i - 1, 'FUB'] else df.at[i - 1, 'FUB']

        df.at[i, 'FLB'] = df.at[i, 'BLB'] if df.at[i, 'BLB'] > df.at[i - 1, 'FLB'] or df.at[i - 1, 'Close'] < \
                                             df.at[i - 1, 'FLB'] else df.at[i - 1, 'FLB']

        df.at[i, 'Supertrend'] = df.at[i, 'FUB'] if df.at[i - 1, 'Supertrend'] == df.at[i - 1, 'FUB'] and \
                                                    df.at[i, 'Close'] < df.at[i, 'FUB'] else \
                                 df.at[i, 'FLB'] if df.at[i - 1, 'Supertrend'] == df.at[i - 1, 'FUB'] and \
                                                    df.at[i, 'Close'] > df.at[i, 'FUB'] else \
                                 df.at[i, 'FLB'] if df.at[i - 1, 'Supertrend'] == df.at[i - 1, 'FLB'] and \
                                                    df.at[i, 'Close'] > df.at[i, 'FLB'] else \
                                 df.at[i, 'FUB'] if df.at[i - 1, 'Supertrend'] == df.at[i - 1, 'FLB'] and \
                                                    df.at[i, 'Close'] < df.at[i, 'FLB'] else 0.00

        df.at[i, 'Color'] = 'Red' if df.at[i, 'Supertrend'] == df.at[i, 'FUB'] else 'Green'

        df.at[i, 'Signal'] = '' if df.at[i, 'Color'] == 'Red' and df.at[i-1, 'Color'] == 'Red' else \
                             'CE SELL' if df.at[i, 'Color'] == 'Red' and df.at[i-1, 'Color'] == 'Green' else \
                             '' if df.at[i, 'Color'] == 'Green' and df.at[i-1, 'Color'] == 'Green' else \
                             'PE SELL' if df.at[i, 'Color'] == 'Green' and df.at[i-1, 'Color'] == 'Red' else ''

df.to_excel('Test_Result_v1.xlsx', index=False)
