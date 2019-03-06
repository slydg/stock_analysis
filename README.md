
# Data Resources

All the data used in this project is provided by tushare.pro, which is an open resource dataset for Chinese stock market.
 A token is needed to use all the data used in this project. It can be gotten by registering in [tushare.pro](https://tushare.pro/) 

* Read the [introduction of tushare](https://tushare.pro/document/1) for more information about tushare.
* ./get_data.py is used to get the financial indicators (the last and the secon last quarterly financial report) and the price data (from the day when the second last quarterly financial report was published to today) for all (possible) listed companies in China  
* ./get_data_pre.py is used to get all daily basic market information of each stock(from the day when the second last quarterly financial report was published to today).

# Models 
The models can be separated into two parts: A model for estimating the price based on the financial information published and a model for predicting the price of the next day based on the daily basic market information.

* The training and testing samples are the data from the day when the second last quarterly report was published to the day when the last quarterly report was published
* The back testing samples are the data from the day when the last quarterly report was published to today
* ./price_model.py is used to construct and test the price estimation model 
* ./price_model.py is used to construct and test the price prediction model 
* Both models are saved for the back testing 

# Assumptions 
There are two assumptions for the models 

* The price of the stock is somehow dependent on the financial state of the target company
* The float of the stock price is somehow influenced by the daily basic market information of the last day

# Back testing
This project estimated the price based on the last quarter information with the models. 

* If we had bought in all the stocks that the prices are lower than the estimated prices, it should calculate the return rate if hold all these stocks till today.
* If we had chosen all the stocks that the prices are lower than the estimated prices, and used the prediction model to buy in and sell out several times, it should calculate the total returns after all the operations.

The results of the back testing are excellent. If we had just held all the chosen stocks, it should get a return rate of 25% for just 12 days.
And if we had operated several times based on the prediction model, the return rate should rise to 25.6%.  

