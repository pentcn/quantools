import pandas as pd
import glob
import os

from loguru import logger

class HistoricalData:

    def __init__(self, date_data_path):
        self.date_data_path = date_data_path
        self.date_file_paths = None

    def to_symbol_files(self, dest_path, time_interval='5m'):
        symbol_csv_data_dict = self._get_symbol_file_paths(time_interval)
            
        for symbol in symbol_csv_data_dict:
            df_list = []
            for path in sorted(symbol_csv_data_dict[symbol]):
                df = pd.read_csv(path, header=1, encoding="GBK", parse_dates=['candle_begin_time'])
                df_list.append(df)
            data = pd.concat(df_list, ignore_index=True)

            # 增加两列数据
            data['symbol'] = symbol.split('_')[0].lower()  # symbol
            data['avg_price'] = data['quote_volume'] / data['volume']  # 均价

            # 排序并重新索引
            data.sort_values(by='candle_begin_time', inplace=False)
            data.reset_index(drop=True, inplace=True)
            
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            data.to_pickle(dest_path + '/%s.pkl' % symbol)
            logger.info('合并并保存文件%s.pkl' % symbol)


    def _get_symbol_file_paths(self, time_interval):
        if self.date_file_paths is None:
            self.date_file_paths = glob.glob(self.date_data_path)

        date_file_paths = list(filter(lambda x: time_interval in x, self.date_file_paths))
        symbol_list = [os.path.splitext(os.path.basename(x))[0] for x in date_file_paths]
        symbol_list = set(symbol_list)

        symbol_csv_data_dict = {symbol: [] for symbol in symbol_list}
        for path in date_file_paths:
            symbol = os.path.splitext(os.path.basename(path))[0]
            if symbol in symbol_csv_data_dict:
                symbol_csv_data_dict[symbol].append(path)
        
        return symbol_csv_data_dict




if __name__ == '__main__':
    date_data_path = r'd:\My Workspaces\2022\quant\data\binance\*\*\*.csv'
    data = HistoricalData(date_data_path)
    for time_interval in ['1m', '5m', '30m', '1h']:
        data.to_symbol_files(r'd:\temp\data\binance\spot', time_interval)

   
