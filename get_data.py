import numpy as np 
import pandas as pd
import tushare as ts 
from time import sleep

# set your tushare.pro token here 
token = "your_token"

# get all the stock code
ts.set_token(token)
pro = ts.pro_api()
stocks = pro.stock_basic()['ts_code']
dataset = pd.DataFrame()


#--------------------************************------------------#

# for each stock save the data as csv file 
# the last finance report as back-testing data
# the second last finance report as training and testing data

for i in [0,1]:
    for stock in stocks:
        print(stock)
        indicators = pro.fina_indicator(ts_code=stock)
        k = str(indicators['ann_date'].values[i])
        if i == 0:
            stock_daily = ts.pro_bar(pro_api=pro,ts_code=stock,start_date=k,adj='qfq')
            stock_daily_basic = pro.daily_basic(ts_code=stock,start_date=k)
        else:
            stock_daily = ts.pro_bar(pro_api=pro,ts_code=stock,start_date=k,end_date=str(indicators['ann_date'].values[0]),adj='qfq')
            stock_daily_basic = pro.daily_basic(ts_code=stock,start_date=k,end_date=str(indicators['ann_date'].values[0]))            
        data = pd.DataFrame()       
        try:
            data['ts_code'] = stock_daily['ts_code']
            data['float'] = stock_daily['high']-stock_daily['low']
            data['change'] = stock_daily['change']
            data['pe'] = stock_daily_basic['pe'].values
            data['ps'] = stock_daily_basic['ps'].values
            data['pb'] = stock_daily_basic['pb'].values
            data['turnover_rate_f'] = stock_daily_basic['turnover_rate_f'].values
            data['eps'] = indicators['eps'][i]
            data['dt_eps'] = indicators['dt_eps'][i]
            data['total_revenue_ps'] = indicators['total_revenue_ps'][i]
            data['revenue_ps'] = indicators['revenue_ps'][i]
            data['capital_rese_ps'] = indicators['capital_rese_ps'][i]
            data['surplus_rese_ps'] = indicators['surplus_rese_ps'][i]
            data['undist_profit_ps'] = indicators['undist_profit_ps'][i]
            data['extra_item'] = indicators['extra_item'][i]
            data['profit_dedt'] = indicators['profit_dedt'][i]
            data['gross_margin'] = indicators['gross_margin'][i]
            data['current_ratio'] = indicators['current_ratio'][i]
            data['quick_ratio'] = indicators['quick_ratio'][i]
            data['cash_ratio'] = indicators['cash_ratio'][i]
            data['ar_turn'] = indicators['ar_turn'][i]
            data['ca_turn'] = indicators['ca_turn'][i]
            data['fa_turn'] = indicators['fa_turn'][i]
            data['assets_turn'] = indicators['assets_turn'][i]
            data['op_income'] = indicators['op_income'][i]
            data['ebit'] = indicators['ebit'][i]
            data['ebitda'] = indicators['ebitda'][i]
            data['fcff'] = indicators['fcff'][i]
            data['fcfe'] = indicators['fcfe'][i]
            data['current_exint'] = indicators['current_exint'][i]
            data['noncurrent_exint'] = indicators['noncurrent_exint'][i]
            data['interestdebt'] = indicators['interestdebt'][i]
            data['netdebt'] = indicators['netdebt'][i]
            data['working_capital'] = indicators['working_capital'][i]
            data['networking_capital'] = indicators['networking_capital'][i]
            data['invest_capital'] = indicators['invest_capital'][i]
            data['retained_earnings'] = indicators['retained_earnings'][i]
            data['diluted2_eps'] = indicators['diluted2_eps'][i]
            data['bps'] = indicators['bps'][i]
            data['ocfps'] = indicators['ocfps'][i]
            data['retainedps'] = indicators['retainedps'][i]
            data['cfps'] = indicators['cfps'][i]
            data['ebit_ps'] = indicators['ebit_ps'][i]
            data['fcff_ps'] = indicators['fcff_ps'][i]
            data['fcfe_ps'] = indicators['fcfe_ps'][i]
            data['netprofit_margin'] = indicators['netprofit_margin'][i]
            data['grossprofit_margin'] = indicators['grossprofit_margin'][i]
            data['cogs_of_sales'] = indicators['cogs_of_sales'][i]
            data['expense_of_sales'] = indicators['expense_of_sales'][i]
            data['profit_to_gr'] = indicators['profit_to_gr'][i]
            data['saleexp_to_gr'] = indicators['saleexp_to_gr'][i]
            data['adminexp_of_gr'] = indicators['adminexp_of_gr'][i]
            data['finaexp_of_gr'] = indicators['finaexp_of_gr'][i]
            data['impai_ttm'] = indicators['impai_ttm'][i]
            data['gc_of_gr'] = indicators['gc_of_gr'][i]
            data['op_of_gr'] = indicators['op_of_gr'][i]
            data['ebit_of_gr'] = indicators['ebit_of_gr'][i]
            data['roe'] = indicators['roe'][i]
            data['roe_waa'] = indicators['roe_waa'][i]
            data['roe_dt'] = indicators['roe_dt'][i]
            data['roa'] = indicators['roa'][i]
            data['npta'] = indicators['npta'][i]
            data['roic'] = indicators['roic'][i]
            data['roe_yearly'] = indicators['roe_yearly'][i]
            data['roa2_yearly'] = indicators['roa2_yearly'][i]
            data['debt_to_assets'] = indicators['debt_to_assets'][i]
            data['assets_to_eqt'] = indicators['assets_to_eqt'][i]
            data['dp_assets_to_eqt'] = indicators['dp_assets_to_eqt'][i]
            data['ca_to_assets'] = indicators['ca_to_assets'][i]
            data['nca_to_assets'] = indicators['nca_to_assets'][i]
            data['tbassets_to_totalassets'] = indicators['tbassets_to_totalassets'][i]
            data['int_to_talcap'] = indicators['int_to_talcap'][i]
            data['eqt_to_talcapital'] = indicators['eqt_to_talcapital'][i]
            data['currentdebt_to_debt'] = indicators['currentdebt_to_debt'][i]
            data['longdeb_to_debt'] = indicators['longdeb_to_debt'][i]
            data['ocf_to_shortdebt'] = indicators['ocf_to_shortdebt'][i]
            data['debt_to_eqt'] = indicators['debt_to_eqt'][i]
            data['eqt_to_debt'] = indicators['eqt_to_debt'][i]
            data['eqt_to_interestdebt'] = indicators['eqt_to_interestdebt'][i]
            data['tangibleasset_to_debt'] = indicators['tangibleasset_to_debt'][i]
            data['tangasset_to_intdebt'] = indicators['tangasset_to_intdebt'][i]
            data['tangibleasset_to_netdebt'] = indicators['tangibleasset_to_netdebt'][i]
            data['ocf_to_debt'] = indicators['ocf_to_debt'][i]
            data['turn_days'] = indicators['turn_days'][i]
            data['roa_yearly'] = indicators['roa_yearly'][i]
            data['roa_dp'] = indicators['roa_dp'][i]
            data['fixed_assets'] = indicators['fixed_assets'][i]
            data['profit_to_op'] = indicators['profit_to_op'][i]
            data['basic_eps_yoy'] = indicators['basic_eps_yoy'][i]
            data['dt_eps_yoy'] = indicators['dt_eps_yoy'][i]
            data['cfps_yoy'] = indicators['cfps_yoy'][i]
            data['op_yoy'] = indicators['op_yoy'][i]
            data['ebt_yoy'] = indicators['ebt_yoy'][i]
            data['netprofit_yoy'] = indicators['netprofit_yoy'][i]
            data['dt_netprofit_yoy'] = indicators['dt_netprofit_yoy'][i]
            data['ocf_yoy'] = indicators['ocf_yoy'][i]
            data['roe_yoy'] = indicators['roe_yoy'][i]
            data['bps_yoy'] = indicators['bps_yoy'][i]
            data['assets_yoy'] = indicators['assets_yoy'][i]
            data['eqt_yoy'] = indicators['eqt_yoy'][i]
            data['tr_yoy'] = indicators['tr_yoy'][i]
            data['or_yoy'] = indicators['or_yoy'][i]
            data['equity_yoy'] = indicators['equity_yoy'][i]
            data['price'] = stock_daily['close']



            #TODO: 增加其他基本面指标
        except:
            continue
        if i == 0:
            data.to_csv('./price_data/'+str(stock)+'_back_testing.csv')
        else:
            data.to_csv('./price_data/'+str(stock)+'_training.csv')
        sleep(1)


