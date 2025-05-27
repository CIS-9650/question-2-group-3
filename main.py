# importing all the libraries that are required for the script
import requests
import json
import pandas as pd
import numpy as np
import re
from urllib.parse import quote
from bs4 import BeautifulSoup
import time
import sqlite3
import certifi
import ssl
from getpass import getpass

# Create a custom SSL context using certifi's CA bundle
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl._create_default_https_context = lambda: ssl_context

# setting the URL to web scrape
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

# setting the headers to access API smoothly
headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.9',
  'Connection': 'keep-alive'
  }

# request to access the page
page = requests.get(url, headers=headers)

# check the connection to the page
page.status_code

# set the variable "tables" with a pandas script to look for table types in the page
tables = pd.read_html(url)

# set the dataframe as the first table (index 0) of all the tables in the page
df = tables[0]

# print the dataframe to check status (note: there is an extra column with no value and an extra row with no valuable data)
print(df)

# apply "index" on the dataframe and set the parameters so the first value of the table starts at index 1 instead of 0
df.index = range(1, len(df) + 1)

# apply "iloc" on the dataframe to select the rows and columns that contain data we need for the API, then set it as adj_table
adj_table = df.iloc[:100, :-1]

# export the "adj_table" dataframe as a CSV file type to download locally
adj_table.to_csv('most_traded_companies.csv', index = False)

# Twelve Data API Configuration
# Prompt user for API key
api_key = getpass("Enter your Twelve Data API key (input hidden): ")
api_url = 'https://api.twelvedata.com/time_series'

# Assuming adj_table is already defined (a DataFrame with a 'Symbol' column)
symbols = adj_table['Symbol'].tolist()[:50]
api_results = []

symbols = adj_table['Symbol'].tolist()[:50]  # Grabs first 50 symbols

# Setting api_results as empty list to initialize
api_results = []

# Defining function to get stock data (now using Twelve Data)
def get_stock_data(symbol, api_key):
    params = {
        "symbol": symbol,
        "interval": "1week",  # Weekly data
        "outputsize": "1",    # Only most recent week
        "apikey": api_key,
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    return data

for x, symbol in enumerate(symbols[:50]):  # Grabs the first 50 symbols
    if x > 0 and x % 8 == 0:  # Twelve Data only allows 8 requests per minute so the final output should take roughly 5 minutes
        time.sleep(65)  # Wait 65 seconds after every 8 requests

    try:
        print(f'Getting Data for {symbol}')
        stock_data = get_stock_data(symbol, api_key)

        if 'values' in stock_data and len(stock_data['values']) > 0: #making sure that the
            latest_data = stock_data['values'][0]  # This is grabbing the most recent week data

            api_results.append({
                'Symbol': symbol,
                'Date': latest_data['datetime'],
                'Open': latest_data['open'],
                'High': latest_data['high'],
                'Low': latest_data['low'],
                'Close': latest_data['close']
            })
        else:
            print(f"No weekly data found for {symbol}")
            api_results.append({
                'Symbol': symbol,
                'Date': np.nan,
                'Open': np.nan,
                'High': np.nan,
                'Low': np.nan,
                'Close': np.nan,
            })
  # this is is catching any errors that occur during the processing
    except Exception as e:
        print(f"Error fetching {symbol}: {str(e)}")
        api_results.append({
            'Symbol': symbol,
            'Date': np.nan,
            'Open': np.nan,
            'High': np.nan,
            'Low': np.nan,
            'Close': np.nan,
        })

# Creating and merging the dataframe
api_dataframe = pd.DataFrame(api_results)
final_results_sp500 = pd.merge(adj_table, api_dataframe, on='Symbol', how='left')

# Exporting the results
final_results_sp500.to_csv('sp_weekly_twelvedata.csv', index=False)

#this is combining it to sql lite database
sql_data = sqlite3.connect('final_results_sp500.db')
final_results_sp500.to_sql('sp500_companies', sql_data, if_exists='replace', index=False)
sql_data.close()

print("The Data has been saved to combine the wikipedia results and the api results for SP 500")
