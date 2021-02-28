'''
钱坤袋 修改成普通定投回测

程序修改自：邢不行 | 量化小讲堂文章《BTC涨这么多，还能买吗？要卖吗？| 量化定投策略告诉你答案【附代码】》微信号 xbx3642
'''
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 读取数据
filename = 'BTC-USDT-1d_2021.csv'
# filename = 'BTC-USDT-1d_2021_归零.csv'
df = pd.read_csv(filename, encoding='gbk', parse_dates=['candle_time'])

# 设置参数
invest_cash = 100  # 每次的基准定投金额
week = 3  # 每周几定投。0代表周一，1代表周二，以此类推
trade_rate = 0.15 / 100  # 手续费

# starttime = '20171215'
starttime = '20210225'  # 开始时间
endtime = '20290116'  # 结束时间
df = df[df['candle_time'] >= pd.to_datetime(starttime)]
df = df[df['candle_time'] <= pd.to_datetime(endtime)]

df['week'] = df['candle_time'].dt.dayofweek

df.reset_index(drop=True, inplace=True)
df.loc[(df['week'] == week), 'normal_invest'] = invest_cash

# 计算买入份额
df['ni_share'] = df['normal_invest'] / (df['close'] * (1 + trade_rate))
df['normal_share'] = df['ni_share'].cumsum()
df['normal_share'].fillna(method='ffill', inplace=True)
df['normal_capital'] = df['normal_share'] * df['close']
df['normal_invest_all'] = df['normal_invest'].cumsum()
df['normal_rate'] = df['normal_capital'] / df['normal_invest_all']
ni_invest_all = round(df['normal_invest'].sum(), 2)

ni_capital = round(df['normal_capital'].iloc[-1], 2)

info = '%s - %s 总投入：%s  总资产：%s  资产/投入：%s' % (starttime, endtime, ni_invest_all, ni_capital, ni_capital / ni_invest_all)
print(info)

# 绘制资金曲线
title = 'BTC定投回测 文件：%s（%s）' % (filename, info)

plt.rcParams["font.family"] = 'Arial Unicode MS'
df['normal_invest_all'].fillna(method='ffill', inplace=True)
df['normal_capital'].fillna(method='ffill', inplace=True)
df['close'].fillna(method='ffill', inplace=True)
plt.figure(figsize=(8.64, 4.8))
plt.title(title)
plt.plot(df['candle_time'], df['normal_invest_all'], label='累计投入资金')
plt.plot(df['candle_time'], df['normal_capital'], label='持有市值')
plt.plot(df['candle_time'], df['close'], label='当天BTC收盘价格')
plt.legend(loc='best')
plt.show()

# df.to_csv(title + '.csv', encoding='gbk', index=False)
print(df.tail(5))
