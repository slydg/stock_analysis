import pandas as pd 
import numpy as np 
import tushare as ts 
from sklearn.metrics import r2_score
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor

# set your tushare.pro token here 
token = "your_token"

# get all the stock code
ts.set_token(token)
pro = ts.pro_api()
stocks = pro.stock_basic()['ts_code']


#-------------*************--------------#
# pricing model back testing

total_input = 0
total_return = 0
each_return = {}
stocks_chosen = []

total_stocks = 0
total_rised_stocks = 0

price_model = joblib.load('./price_model.model')

for stock in stocks:
    
    try:
        data = pd.read_csv('./price_data/'+str(stock)+'_back_testing.csv')
        dataset = data.drop(['trade_date','ts_code','price','float','change',],axis=1).fillna(data.mean()).fillna(0)  
        X = dataset.values
        k = price_model.predict(X[-1].reshape(1,-1)) 
    except:
        continue
    if data['price'].values[-1]/k < 0.9:
        try:
            out_price = data['price'].values[0]
            total_input += 10000 
            total_return += 10000 * (out_price / data['price'].values[-1])
            each_return[stock] = out_price / data['price'].values[-1]
            stocks_chosen.append(stock)
            total_stocks += 1
            if (out_price / data['price'].values[-1]) > 1:
                total_rised_stocks += 1
        except:
            continue

print('total input: ')
print(total_input)
print('total return: ')
print(total_return)
print('total return rate: ')
print(total_return / total_input)
print('ratio of the rised stocks')
print(total_rised_stocks / total_stocks)


#----------------**********************---------------#
# predicting model back testing on the stocks chosen by the model above

total_input = 0
total_return = 0
predict_model = joblib.load('./predict_model.model')
for stock in stocks_chosen:
    try:
        test_stockdata = pd.read_csv('./predict_data/'+str(stock)+'_back_testing.csv').drop(['Unnamed: 0'],axis=1).fillna(0)
        test_stockdata['predict'] = predict_model.predict(test_stockdata.drop(['trade_date','ts_code'],axis=1))
    except:
        continue

    total_input += 10000
    stock_fund = 10000
    stock_input = 0
    stock_amount = 0
    stock_asset = 10000
    input_each_time = 0
    for day in list(test_stockdata['trade_date'].values)[::-1]:
        stock_data = test_stockdata[test_stockdata['trade_date']==day]
        
        # try:
        #     train_data1 = pd.read_csv('d:/code/stock_data_analysis/predict_data/'+str(stock)+'_training.csv').drop(['Unnamed: 0','ts_code'],axis=1)
        #     train_data1 = train_data1.fillna(train_data1.mean()).fillna(0)
        #     train_data2 = test_stockdata[test_stockdata['trade_date'] <= day].drop(['ts_code'],axis=1)
        #     train_data2 = train_data2.fillna(train_data2.mean()).fillna(0)
        #     train_data = pd.concat([train_data2,train_data1])
        #     pre = train_data[:-1]['close']
        #     train_data = train_data[1:]
        #     train_data['predict'] = pre.values
        # except:
        #     continue

        # for stock in stocks_chosen:
        #     try:
        #         train_data3 = pd.read_csv('d:/code/stock_data_analysis/predict_data/'+str(stock)+'_training.csv').drop(['Unnamed: 0','ts_code'],axis=1)
        #         train_data3 = train_data3.fillna(train_data3.mean()).fillna(0)
        #         train_data4 = test_stockdata[test_stockdata['trade_date'] <= day].drop(['ts_code'],axis=1)
        #         train_data4 = train_data4.fillna(train_data4.mean()).fillna(0)
        #         train_data5 = pd.concat([train_data3,train_data4])
        #         pre1 = train_data5[:-1]['close']
        #         train_data5 = train_data5[1:]
        #         train_data5['predict'] = pre1.values
        #         train_data = pd.concat([train_data,train_data5])
        #     except:
        #         continue
        # print(train_data)

        # X = train_data.drop(['predict'],axis=1)
        # Y = train_data['predict']

        # predict_model = GradientBoostingRegressor().fit(X,Y)

        # stock_data_predict = predict_model.predict(stock_data.drop(['ts_code'],axis=1).values.reshape(1,-1))

        
        if test_stockdata['predict'].values[0] / stock_data['close'].values[0] > 1.01:
            stock_input += stock_fund
            stock_amount += stock_fund / stock_data['close'].values[0]
            input_each_time += stock_fund            
            stock_fund = 0
        elif test_stockdata['predict'].values[0] / stock_data['close'].values[0] < 0.99 and stock_fund == 0:
            stock_input = 0
            stock_fund = stock_data['close'].values[0] * stock_amount
            stock_amount = 0
            input_each_time = 0

        stock_input = stock_amount * stock_data['close'].values[0]
        if stock_input != 0:
            # cut loss
            if stock_input / input_each_time < 0.95:
                stock_input = 0
                stock_fund = stock_data['close'].values[0] * stock_amount
                stock_amount = 0
                input_each_time = 0
            # stop profit
            elif stock_input / input_each_time > 1.5:
                stock_input = 0
                stock_fund = stock_data['close'].values[0] * stock_amount
                stock_amount = 0
                input_each_time = 0


        stock_input = stock_amount * stock_data['close'].values[0]
        stock_asset = stock_input + stock_fund
    total_return += stock_asset

print('total input: ')
print(total_input)
print('total return: ')
print(total_return)
print('total return rate: ')
print(total_return / total_input)

