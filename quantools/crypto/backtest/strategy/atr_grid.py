import pandas as pd

class AtrGrid():

    def __init__(self, data_file_path, begin_date):
        self.data = pd.read_pickle(data_file_path)
        self.data = self.data.loc[self.data['candle_begin_time']>pd.to_datetime(begin_date)]
        self.data.reset_index(inplace=True, drop=True)
        self.factor = ''

    def create_backtest_data(self, n):
        """
        N=20
        TR=MAX(HIGH-LOW,ABS(HIGH-REF(CLOSE,1)),ABS(LOW-REF(CLOSE,1)))
        ATR=MA(TR,N)
        MIDDLE=MA(CLOSE,N)
        """
        self.data['c1'] = self.data['high'] - self.data['low'] # HIGH-LOW
        self.data['c2'] = abs(self.data['high'] - self.data['close'].shift(1)) # ABS(HIGH-REF(CLOSE,1)
        self.data['c3'] = abs(self.data['low'] - self.data['close'].shift(1)) # ABS(LOW-REF(CLOSE,1))
        self.data['TR'] = self.data[['c1', 'c2', 'c3']].max(axis=1) # TR=MAX(HIGH-LOW,ABS(HIGH-REF(CLOSE,1)),ABS(LOW-REF(CLOSE,1)))
        self.data['ATR'] = self.data['TR'].rolling(n, min_periods=1).mean() # ATR=MA(TR,N)

        # ATR指标去量纲
        self.factor = '前%dhATR' % n
        self.data[self.factor] = self.data['ATR']
        self.data[self.factor] = self.data[self.factor].shift(1)

        # 删除中间数据
        del self.data['c1']
        del self.data['c2']
        del self.data['c3']
        del self.data['TR']
        del self.data['ATR']

    def run(self, init_amount, miner_amount, trade_amount, ratio):
        # 初始化数据值
        base_row = 0
        self.data['base_row'] = -1
        self.data[['base_row']] = self.data[['base_row']].astype('int64')
        self.data.loc[0,'base_row'] = base_row

        # 根据Atr的倍数，计算交易信号
        self.data['trade_count'] = 0
        for index, row_item in self.data.iterrows():
            if index == 0:
                continue
            if row_item['avg_price'] >= self.data.loc[base_row, 'avg_price'] + self.data.loc[index, self.factor] * ratio:
                self.data.loc[index, 'trade_count'] = -trade_amount
                base_row = index
            if row_item['avg_price'] < self.data.loc[base_row, 'avg_price'] - self.data.loc[index, self.factor] * ratio:
                self.data.loc[index, 'trade_count'] = trade_amount
                base_row = index
                
            self.data.loc[index, 'base_row'] = base_row
            
        # 设置挖矿入金值
        self.data['miner'] = 0
        self.data.loc[0, 'miner'] = init_amount
        self.data.loc[(self.data.index + 1)%48==0 ,'miner'] = miner_amount
        self.data['miner'] = self.data['miner'].cumsum()

    def get_return(self):
        df_data = self.data.loc[self.data['trade_count']!=0].copy()
        df_data.reset_index(drop=True, inplace=True)
        df_data['pos'] = 0 

        for index, row_item in df_data.iterrows():
            if index == 0:
                df_data.loc[index, 'pos'] = row_item['trade_count'] + row_item['miner']
            else:
                cond = df_data.loc[index-1, 'pos'] + row_item['trade_count'] + (row_item['miner'] - df_data.loc[index-1, 'miner'])
                if cond >= 0:
                    df_data.loc[index, 'pos'] = cond

        df_data['cash'] = -df_data['avg_price'] * df_data['trade_count']
        df_data['cash'] = df_data['cash'].cumsum()
        df_data['maket_value'] = df_data['pos']*df_data['avg_price'] + df_data['cash']
        df_data['base'] = df_data['avg_price'] * df_data['miner']
        df_data['return'] = (df_data['maket_value'] - df_data['base'])

        del df_data['open']
        del df_data['low']
        del df_data['close']
        del df_data['high']
        del df_data['volume']
        del df_data['quote_volume']
        del df_data['trade_num']
        del df_data['taker_buy_quote_asset_volume']
        del df_data['taker_buy_base_asset_volume']
        del df_data['trade_count']

        return df_data


if __name__ == '__main__':
    data_path = r'd:\Temp\data\binance\spot\ETH-USDT_1h.pkl'
    begin_date = '2021-05-01'
    trade_amount = 0.1
    init_amount = 1  # 策略开始币的数量
    miner_amount = 0.1  # 挖矿入金数量
    miner_period = 48 # 挖矿入金周期

    n = 144
    ratio = 0.382
    grid = AtrGrid(data_path, begin_date)
    grid.create_backtest_data(n)
    grid.run(init_amount, miner_amount, trade_amount, ratio)
    df = grid.get_return()

    df[['maket_value','base','cash']].plot()
    print(df)
    pass