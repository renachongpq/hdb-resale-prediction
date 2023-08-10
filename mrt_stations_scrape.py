import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

"""
get list of all mrt and lrt stations names
"""

mrt_url = 'https://mrtmapsingapore.com/mrt-stations-singapore/'
lrt_url = 'https://mrtmapsingapore.com/lrt-stations/'

def scraper(url):
    stations = []
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    result = soup.findAll('td', class_='column-2')
    for i in range(len(result)):
        stations.append(result[i].text)
    df = pd.DataFrame({'name': stations})
    return df

mrt_stations = scraper(mrt_url)
lrt_stations = scraper(lrt_url)

# mrt_stations.to_csv('./data/mrt_stations.txt', index=False)
# lrt_stations.to_csv('./data/lrt_stations.txt', index=False)