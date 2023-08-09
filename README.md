# Prediction of Future HDB Resale Flat Prices
## Overview
Predict future HDB (Housing & Development Board) resale flat prices

## Dataset Source
Majority of the datasets have been obtained from the government official data site, [data.gov.sg](https://data.gov.sg/). These are the datasets obtained from the site:
* HDB resale flat prices: [link](https://data.gov.sg/dataset/resale-flat-prices)
* List of supermarkets in Singapore (updated until 18 October 2021): [link](https://data.gov.sg/dataset/listing-of-licensed-supermarkets)

The list of MRT and LRT stations were obtained from [mrtmapofsingapore.com](https://mrtmapsingapore.com/).

The list of completed Selective En-bloc Redevelopment Scheme (SERS) projects for selected HDB flats were obtained from [the official Housing & Development Board site](https://www.hdb.gov.sg/residential/living-in-an-hdb-flat/sers-and-upgrading-programmes/sers/sers-projects/completed-sers-projects).
* These flats, which are usually more than 25 years old, are selected for redevelopment. Hence, residents are required to move out of these selected flats for redevelopment. More information to understand more about SERS [here](https://www.hdb.gov.sg/residential/living-in-an-hdb-flat/sers-and-upgrading-programmes/sers)

Lastly, latitudes and longitudes coordinates of various locations were obtained through [OneMap API](https://www.onemap.gov.sg/apidocs/). These were mainly used to determine the distance between the location of the resale flat and nearby amenities.

## Exploratory Data Analysis

## Data Preparation (Cleaning, Feature Engineering etc.)
HDB resale flat prices data from year 2000 onwards were used for this project. As some flats were selected for en-bloc (refer to [SERS](https://www.hdb.gov.sg/residential/living-in-an-hdb-flat/sers-and-upgrading-programmes/sers)) during this period, data for en-bloc flats are removed as they are no longer in transaction in the market (note that the replacement flats were designated new addresses). 

## Modelling


## Evaluation of Models & Discussion


## Limitations & Future Improvements
The current set of features used for housing price prediction can be expanded futher to include other features that buyers take into consideration when looking to purchase a HDB flat. For example, the proximity of HDB flats to public transportation (specifically, MRT stations) is an important factor that a significant number of buyers consider when buying a HDB flat. Accesibility to amenities such as supermarkets, shopping malls and eateries may also affect the price of resale flats. Incorporating more features that buyers take into consideration is likely to be able to improve the accuracy of resale flat price predictions.

Futhermore, the nature of the dataset is time series data, hence traditional time series forecasting methods such as ARIMA can be explored to compare its accuracy to forecasting using machine learning.
