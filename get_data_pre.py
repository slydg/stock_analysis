import numpy as np 
import pandas as pd
import tushare as ts 
from time import sleep
import datetime

# set your tushare.pro token here 
token = "your_token"

# get all the stock code
ts.set_token(token)
pro = ts.pro_api()
stocks = pro.stock_basic()['ts_code']
dataset = pd.DataFrame()


#-----------------------********************--------------------#

# for each stock save the technological daily indicators data as csv file
# the last finance report as back-testing data
# the second last finance report as training and testing data

for i in [0,1]:
    for stock in stocks:
        indicators = pro.fina_indicator(ts_code=stock)
        k = datetime.datetime.strptime(indicators['ann_date'].values[i],'%Y%m%d')
        k = datetime.datetime.strftime(k-datetime.timedelta(days=70),'%Y%m%d')
        
        try:
            if i == 0:
                stock_daily = ts.pro_bar(pro_api=pro,ts_code=stock,start_date=k,adj='qfq',ma=[5,10,15,20,50])[:-50]
                stock_daily_basic = pro.daily_basic(ts_code=stock,start_date=k)[:-50]
            else:
                stock_daily = ts.pro_bar(pro_api=pro,ts_code=stock,start_date=k,end_date=str(indicators['ann_date'].values[0]),adj='qfq',ma=[5,10,15,20,50])[:-50]
                stock_daily_basic = pro.daily_basic(ts_code=stock,start_date=k,end_date=str(indicators['ann_date'].values[0]))[:-50]              
        except:
            continue
        ###############################################################   
        # construct features here 
        # ma := moving average
        # [5,10,15,20,50]
        """
        stock_daily_basic factors:
        ts_code--------------TS股票代码  
        trade_date-----------交易日期
        close----------------当日收盘价
        turnover_rate--------换手率（%）
        turnover_rate_f------换手率（自由流通股）
        volume_ratio---------量比 
        pe-------------------市盈率（总市值/净利润）
        pe_ttm---------------市盈率（TTM）
        pb-------------------市净率（总市值/净资产）
        ps-------------------市销率
        ps_ttm---------------市销率（TTM）
        total_share----------总股本 （万）
        float_share----------流通股本 （万）
        free_share-----------自由流通股本 （万）
        total_mv-------------总市值 （万元）
        circ_mv--------------流通市值（万元）
        """
        ###############################################################
        try:
            data = stock_daily_basic 
            data['change'] = stock_daily['change'].values
            data['float'] = (stock_daily['high']-stock_daily['low']).values
            data['open'] = stock_daily['open'].values
            data['low'] = stock_daily['low'].values
            data['close'] = stock_daily['close'].values
            data['pct_chg'] = stock_daily['pct_chg'].values # 涨跌幅
            data['pre_close'] = stock_daily['pre_close'].values # 前一日收盘价
            # moving average of price [5,10,15,20,50]
            data['ma5'] = stock_daily['ma5'].values
            data['ma10'] = stock_daily['ma10'].values
            data['ma15'] = stock_daily['ma15'].values
            data['ma20'] = stock_daily['ma20'].values
            data['ma50'] = stock_daily['ma50'].values
            # moving average of volumn [5,10,15,20,50]
            data['ma_v_5'] = stock_daily['ma_v_5'].values
            data['ma_v_10'] = stock_daily['ma_v_10'].values
            data['ma_v_15'] = stock_daily['ma_v_15'].values
            data['ma_v_20'] = stock_daily['ma_v_20'].values
            data['ma_v_50'] = stock_daily['ma_v_50'].values
        except:
            continue
        print(stock)

        if i == 0:
            data.to_csv('./predict_data/'+str(stock)+'_back_testing.csv')
        else:
            data.to_csv('./predict_data/'+str(stock)+'_training.csv')
        sleep(1)


