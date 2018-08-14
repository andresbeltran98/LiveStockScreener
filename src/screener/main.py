"""This is the main module. It parses the command line arguments
and runs the script
"""

__author__ = 'Andres Beltran'
__version__ = '1.0'

import sys
import argparse
import sqlite3
import screener.intraday_stock as intraday

# Connects to the database
conn = sqlite3.connect('src/stocks.db')
c = conn.cursor()


def get_name_from_ticker(ticker):
    """Returns the company's name from its ticker Symbol
    Args:
        ticker (str): Ticker Symbol
    Returns:
        tuple: The name of the company at index 0
    """
    conn = sqlite3.connect('src/stocks.db')
    c = conn.cursor()
    symbol = ('{}'.format(ticker),)
    c.execute("SELECT name FROM stocksInfo WHERE symbol=?", symbol)
    return c.fetchone()


def get_stock_from_name(name):
    """Returns all the companies in the database that match a given name
    Args:
        name (str): The name of the company to search for
    Returns:
        tuple: The symbol and name of all the companies found in the database
    """
    conn = sqlite3.connect('src/stocks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM stocksInfo WHERE name LIKE '%"+name+"%'")
    return c.fetchall()


def parse_arguments(args):
    """Parse command line arguments
    Args:
        args ([str]): Command line parameters as list of strings
    Returns:
        :obj:'argparse.Namespace': command line parameters namespace
    """
    parser = argparse.ArgumentParser(description='Live Intraday Stock Screener')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-g',
        '--graph',
        metavar='',
        help='Stock ticker symbol')
    group.add_argument(
        '-s',
        '--search',
        metavar='',
        help='Find the ticker symbol for a given company\'s name')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='1.0',
        help='Program\'s version')

    return parser.parse_args(args)


def run():
    """Runs the script"""
    args = parse_arguments(sys.argv[1:])

    if args.graph is not None:
        name = get_name_from_ticker(args.graph)
        c.close()
        conn.close()
        if name is None:
            print('Ticker not found. To search for a company\'s symbol type:',
                  '\nscreener [--search or -i] [company\'s name]')
            return
        intraday.run(args.graph, name[0])

    if args.search is not None:
        info = get_stock_from_name(args.search)
        if info:
            for company in info:
                print(company)
        else:
            print('Not found')


if __name__ == '__main__':
    run()
