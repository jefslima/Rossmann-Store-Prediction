# Rossmann Store Prediction

<img src="https://bbj.hu/uploads/banners/201409/rossmanjpg_2014090414295134.webp"/> <br>

This repository contains an end-to-end project for forecasting drugstore sales applying linear and non-linear regression.<br>

### Disclaimer 1

This is a fictional context created for portfolio. All characters were created as well as the business problem.
### Disclaimer 2

The data were published in [kaggle](https://www.kaggle.com/c/rossmann-store-sales/overview).

### Disclaimer 3

The project is part of [Comunidade DS](https://sejaumdatascientist.com/inscricao-lives-comunidade-ds).

## Machine Learning Project on Regression for Drugstore Sales Forecasting

The aim of this project is:
* Perform a forecasting drugstore sales for the next six weeks
* Get an overview of the dataset and handle null values
* Create a mind map hypothesis to determine which one is true
* Determine which variables are most relevant
* Apply transformations on features to behave close to a normal distribution
* Apply Boruta as a feature selector
* Apply Linear and Non-linear algorithms to understand the model complexity.
* Compare algorithms for machine learning modeling considering: 
  * Average,
  * Linear Regression,
  * Linear Regression Regularized (Lasso), 
  * Random Forest Regressor
   *XGBoost Regressor
   
* Apply hyperparameter fine tunning using random search
* Perform error interpretation considering business and machine learning performance
* Deploy model to production on telegram

## 1. Business Problem

Drugstore managers request sales forecasts for the next six weeks.<br>
Looking for the main issue, CFO told more details about the request.<br>
He explained that he needs to set a budget for carrying out the drugstores' repairs.<br>
Through Sales Forecasting, the CFO can determine the percentage of money each drugstore can use to make repairs.<br>

## 2. Business Results

The solution has main point to create a machine learning model that uses the drugstores' characteristics to forecast sales in the next 6 weeks.<br>
Information about the drugstore sales forecasting is displayed on a Telegram Bot.<br>

## 3. Business hypothesis

* Only the days on which the drugstores were open were considered.
* Only drugstores with sales values bigger than 0 were considered.
* The day, month, year, and week information were based on the date.
* For drugstores that did't have the Competition Distance information, it was considered should have a distance equal as 200000.
* For drugstores that did't have "Promo_Since" and "Promo_time_week" information considered the date as the initial parameter.
* For drugstores that did't have CompetitionOpenSince [month/year] information considered the date as the initial parameter.


<br>

* The variables on the dataset are:<br>

|Variable | Definition|
|-------- | -------------|
|Assortment| describes an assortment level: a = basic, b = extra, c = extended |
|CompetitionDistance| distance in meters to the nearest competitor store|
|CompetitionOpenSince[month/year]| gives the approximate year and month of the time the nearest competitor was opened |
|Customers | the number of customers on a given day |
|Date| represents the date the drugstore information began to be collected |
|Id | represents a (Store, Date) duple within the test set |
|Is_promo | indicates whether a store is running a promo on that month |
|Open | an indicator for whether the store was open: 0 = closed, 1 = open |
|Promo | indicates whether a store is running a promo on that day |
|Promo2 | is a continuing and consecutive promotion for some stores: 0 = store is not participating, 1 = store is participating |
|Promo2Since[year/week] | describes the year and calendar week when the store started participating in Promo2 |
|PromoInterval | describes the consecutive intervals Promo2 is started, naming the months the promotion is started anew. E.g. "Feb,May,Aug,Nov" means each round starts in February, May, August, November of any given year for that store |
|Sales | the turnover for any given day |
|SchoolHoliday | indicates if the (Store, Date) was affected by the closure of public schools|
|StateHoliday | indicates a state holiday. Normally all stores, with few exceptions, are closed on state holidays. Note that all schools are closed on public holidays and weekends. a = public holiday, b = Easter holiday, c = Christmas, 0 = None|
|Store | a unique Id for each store |
|StoreType | differentiates between 4 different store models: a, b, c, d|<br>

## 4. Solution Strategy

The Strategy to solve this challenge was applying CRISP-DM methodology considering the following steps:<br>

**Phase 01. Data Description:** Get an overview of the dataset, handle null values, and get descriptive statistics for the numeric and categorical attributes.<br>
**Phase 02. Feature Engineering:** Create a mind map hypothesis to determine which one is true and create new features<br>
**Phase 03. Data Cleaning:** Filter variables ​​considering business bias based on data constraints.<br>
**Phase 04. Exploratory Data Analysis:** Determine which ​​variables are most relevant through applying univariate, bivariate, and multivariate analysis. In addition, analyze the veracity of the hypotheses.<br>
**Phase 05. Data Preparation:** Apply RobustScaler and MinMaxScaler rescaling methods on the features competition_distance, competition_time_month, promo_time_week, and year. Apply encoding transformation on the features store_type, assortment, and state_holiday. Apply cyclical transformation on the features day_of_week, month, day, and week_of_year.<br>
**Phase 06. Feature Selection:** Split the dataset into the train and the test, filter the variables considering the correlation with the response variable and apply Boruta as a feature selector.<br>
**Phase 07. Machine Learning Modeling:** compare machine learning modeling performance considering a baseline (Average), two linear (Linear Regression and Regularized Linear Regression - Lasso), and two non-linear (Random Forest Regressor and XGBoost Regressor). Implementation of cross-validation to compare models with their real performance and ranking based on the less RMSE error.<br>
**Phase 08. Hyperparameter Fine Tunning:** apply the random search optimization method to find a good solution quickly based on a search space that contains the parameters with values ​​within a range.<br>
**Phase 09. Translation and Error interpretation:** Error analysis based on business performance to create scenarios ( best and worst scenarios ) and Machine learning model performance analysis (error rate and residue analysis).<br>
**Phase 10. Deploy to Production:** create a class named "Rossmann.py" containing the data preparation and feature engineering. Create an API named "Handler" using Flask to communicate the Rossmann class with the trained model to get the sales forecast based on a "Rossmann API" request. Create an API named "Rossmann API" using Flask to communicate the "Handler" API with the test dataset and also with the telegram application containing a Telegram Bot.<br>
**Phase 11. Telegram Bot:** Deploy API "Handler" and "Rossmann API" on Heroku cloud. Create a Telegram Bot that receives the drugstore sales forecasting after a user sends a message containing the drugstore number.
 <br>
 
 ## 5.Best Insights
### 5.1 - Stores with closer competitors should sell less.
**False, Stores with closer competitors sell more**

### 5.2 - Stores should sell less on weekends.
**True, stores sell less on weekends**
 
 ## 6. Machine Learning Models Applied and Performance

The following machine learning models were trained:
 
  * Average model (baseline);
  * Linear Regression,
  * Linear Regression Regularized (Lasso), 
  * Random Forest Regressor
  * XGBoost Regressor
   

All the models applied went through the Cross Validation stage to verify the real performance.
