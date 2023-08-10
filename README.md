# Prediction of Future HDB Resale Flat Prices
## Overview
Predict future HDB (Housing & Development Board) resale flat prices

## Dataset Source
The main dataset, HDB resale flat price, was obtained from the government official data site, [link](https://data.gov.sg/dataset/resale-flat-prices). As this dataset also consists of transactions for en-bloc flats, a list of en-bloc flats was cross referenced to remove these data.
* The list of completed Selective En-bloc Redevelopment Scheme (SERS) projects for selected HDB flats were referenced from [the official Housing & Development Board site](https://www.hdb.gov.sg/residential/living-in-an-hdb-flat/sers-and-upgrading-programmes/sers/sers-projects/completed-sers-projects). These flats, which are usually more than 25 years old, are selected for redevelopment, thus residents are required to move out of these selected flats. More information to understand more about SERS [here](https://www.hdb.gov.sg/residential/living-in-an-hdb-flat/sers-and-upgrading-programmes/sers)

The list of MRT stations were obtained from [Wikipedia](https://en.wikipedia.org/wiki/List_of_Singapore_MRT_stations).

Latitudes and longitudes coordinates of MRT stations and HDB flats were obtained through [OneMap Search API](https://www.onemap.gov.sg/apidocs/). [OneMap Routing API](https://www.onemap.gov.sg/apidocs/) was also used to determine the walking distance and time from the HDB flat to the nearest MRT station.

## Exploratory Data Analysis

## Data Preparation (Cleaning, Feature Engineering etc.)
HDB resale flat prices data from year 2000 onwards were used for this project. As some flats were selected for en-bloc (refer to [SERS](https://www.hdb.gov.sg/residential/living-in-an-hdb-flat/sers-and-upgrading-programmes/sers)) during this period, data for en-bloc flats are removed as they are no longer in transaction in the market (note that the replacement flats were designated new addresses). 

## Modelling


## Evaluation of Models & Discussion


## Limitations & Future Improvements
The current set of features used for housing price prediction can be expanded futher to include other features that buyers take into consideration when looking to purchase a HDB flat. For example, accesibility to amenities such as supermarkets, shopping malls and eateries may affect the price of resale flats. Incorporating more features that buyers take into consideration is likely to be able to improve the accuracy of resale flat price predictions. However, there is a lack of data on the presence of such amenities over the years, hence it would be difficult to attempt to incorporate these features into the data.

Futhermore, the nature of the dataset is time series data, hence traditional time series forecasting methods such as ARIMA can be explored to compare its accuracy to forecasting using machine learning.
