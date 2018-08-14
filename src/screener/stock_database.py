"""This module contains the functions for database management
"""

__author__ = 'Andres Beltran'
__version__ = '1.0'

import sqlite3
import csv


conn = sqlite3.connect('src/stocks.db')
c = conn.cursor()


def create_table():
    """Generates the database table"""
    c.execute('CREATE TABLE IF NOT EXISTS stocksInfo (symbol TEXT, name TEXT)')


def data_entry(symbol, name):
    """Inserts an item into the database
    Args:
        symbol (str): The ticker Symbol
        name (str): Stock's name
    """
    c.execute('INSERT INTO stocksInfo (symbol, name) VALUES (?, ?)',
              (symbol, name))
    conn.commit()


def insert_all_elements():
    """Parses a CSV file and inserts all the values to the database"""
    with open('src/NYSE.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for line in csv_reader:
            data_entry(line['Symbol'], line['Name'])


# create_table()
# insert_all_elements()
c.close()
conn.close()
