import pandas as pd 
import numpy as np 
from sklearn.ensemble import GradientBoostingRegressor
import tushare as ts 
from sklearn.metrics import r2_score
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split

# set your tushare.pro token here 
token = "your_token"

# get all the stock code
ts.set_token(token)
pro = ts.pro_api()
stocks = pro.stock_basic()['ts_code']
dataset = pd.DataFrame()

for stock in stocks:
    try:
        data = pd.read_csv('./predict_data/'+str(stock)+'_training.csv')    
    except:
        continue

    pre = data[:-1]['close'].values
    data = data[1:]
    data['predict'] = pre
    dataset = pd.concat([dataset,data])


data = dataset
data = data.fillna(data.mean())


#-------------*****************------------
# construct the predict model

X = data.drop(['Unnamed: 0','trade_date','ts_code','predict'],axis=1)
X = X.dropna(axis=1, how='all').astype(float)

Y = data['predict']

trX, teX, trY, teY = train_test_split(X, Y, test_size=0.3)

model = GradientBoostingRegressor().fit(trX,trY)

print('training_r2')
print(model.score(trX, trY))

prY = model.predict(teX)
r2 = r2_score(teY,prY)
print('testing-r2: ')
print(r2)

joblib.dump(model,'./predict_model.model')