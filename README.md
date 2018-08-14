# Live Intraday Stock Screener

The program allows to graph live intraday stock quotes using candlestick charts, and some performance indicators, such as simple moving averages, the Relative Strength Index (RSI), and the Volume Price Trend (VPT). The script also allows to search for the ticker symbol of a company given the name of the stock, so that it can be graphed later. The database file contains NYSE and NASDAQ stocks. Intraday data are obtained from Alpha Vantage’s free API. A web crawler and a database manager module are included as part of the project.

## Getting Started
### Prerequisites
* Python 2.7 or above.
* Git

## Installing the program
1.- Open command line and clone the project: 
```bash
git clone https://github.com/andresbeltran98/LiveStockScreener.git
```
2.- Type: 
```bash
cd LiveStockScreener
```
3.- Install the project and its dependencies (if you want, you can create a virtual environment within the project’s folder, so that all site-packages are installed there):
```bash
python setup.py install
```

## Running the program
* To generate a live graph type:
```bash
screener -g/or --graph [ticker symbol]
```
Example:
```bash
screener -g AAPL
```

* To search for the ticker symbol of a company
```bash
screener -s/or --search [company’s name]
```
Example:
```
screener --search Intel
```
Will return a list of all the stocks whose name includes the word “intel”

## Documentation
Documentation is offered under doc/index.html <br>
Or you can see it [here](http://htmlpreview.github.io/?https://github.com/andresbeltran98/HuffmanCompressor/blob/master/doc/index.html)

## Author
* Andres Beltran - B.S. Computer Science candidate. CWRU 2021

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
