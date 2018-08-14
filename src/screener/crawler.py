"""This module represents a web crawler. It gets the data from
Alpha Vantage's API
"""

__author__ = 'Andres Beltran'
__version__ = '1.0'


import json
import os
import ssl
import time
import datetime
import pandas as pd
from urllib.request import urlopen


def get_url(ticker, interval):
    """Sets the URL
    Args:
        ticker (str): Ticker Symbol
        interval (str): Time interval
    Returns:
        str: The final URL for the API
    """

    # Get the final API url
    alpha_api = 'O1C7ECLZQODUYN6D'
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'
    outputsize = 'full'
    return url + '&symbol=' + ticker + '&outputsize=' + outputsize + \
        '&interval=' + interval + '&apikey=' + alpha_api


def get_dictionary(ticker, interval):
    """Gets the dictionary that stores all the data from the API
    Args:
        ticker (str): Ticker Symbol
        interval (str): Time interval
    Returns:
        dict: The dictionary that stores timestamps and the stock's data
    """
    # Turn certificate's verification off
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

    try:
        response = urlopen(get_url(ticker, interval))
        data = json.load(response)

        # Get the key(dictionary) where all dates are stored
        print("Pulling data...", str(datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S')))
        dictionary = data[list(data.keys())[1]]
        return dictionary

    except Exception as e:
        raise


def parse_dictionary(dict, current_day):
    """Parse the data from the API's dictionary
    Args:
        dict (dict): The dictionary with all the data
        current_day (int): Today's day as an integer
    Returns:
        :obj:'pandas.DataFrame': The dataframe with dates as indices, and open,
        high, low, close, and volume values
    """
    dates = []
    open = []
    high = []
    low = []
    close = []
    volume = []

    # key is the date
    # subkey is open,high, low, close
    # dict[key][subkey] is the value of each subkey
    for key in dict:
        now = pd.to_datetime(key)
        open_time = pd.to_datetime(now.strftime('%Y-%m-%d') + ' 9:30:00')

        if now.day == current_day and now >= open_time:
            dates.insert(0, pd.to_datetime(key))

            for subkey in dict[key]:
                if (subkey == '1. open'):
                    open.insert(0, float(dict[key][subkey]))
                elif (subkey == '2. high'):
                    high.insert(0, float(dict[key][subkey]))
                elif (subkey == '3. low'):
                    low.insert(0, float(dict[key][subkey]))
                elif (subkey == '4. close'):
                    close.insert(0, float(dict[key][subkey]))
                else:
                    volume.insert(0, float(dict[key][subkey]))

    if not dates:
        raise Exception('No Data!')

    df_dict = {'Date': dates,
               'Open': open,
               'High': high,
               'Low': low,
               'Close': close,
               'Volume': volume
               }

    return pd.DataFrame(df_dict)


def add_last_row(dict, df):
    """Adds a row to the dataframe when the API's values are updated
    Args:
        dict (dict): The dictionary with all the data
        df (:obj:'pandas.DataFrame':): Stock's dataframe
    """
    last_row = []
    for key in dict:
        if pd.to_datetime(key) > df.index[-1]:
            last_key = pd.to_datetime(key)

            for subkey in dict[key]:
                if (subkey == '1. open'):
                    last_row.append(float(dict[key][subkey]))
                elif (subkey == '2. high'):
                    last_row.append(float(dict[key][subkey]))
                elif (subkey == '3. low'):
                    last_row.append(float(dict[key][subkey]))
                elif (subkey == '4. close'):
                    last_row.append(float(dict[key][subkey]))
                else:
                    last_row.append(float(dict[key][subkey]))

            df.loc[last_key] = last_row
