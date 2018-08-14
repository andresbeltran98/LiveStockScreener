"""This module plots the candlesticks, volume, moving averages, and RSI
"""

__author__ = 'Andres Beltran'
__version__ = '1.0'


import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
import datetime
import pytz
import pandas as pd
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from matplotlib import style
from mpl_finance import candlestick_ohlc
import screener.indicators as indicators
import screener.crawler as crawler


def rsi_graph_settings(axrsi):
    """Configures the RSI plot
    Args:
        axrsi (:obj:'matplotlib.axes.Axes':): RSI axis
    """
    # Grid and labels
    axrsi.grid(True, alpha=0.3, linestyle='dotted')
    axrsi.set_ylabel('RSI', fontname='Arial', fontsize=13)
    plt.setp(axrsi.get_xticklabels(), visible=False)

    # Spines
    axrsi.spines['bottom'].set_color('white')
    axrsi.spines['bottom'].set_alpha(0.6)
    axrsi.spines['left'].set_color('white')
    axrsi.spines['left'].set_alpha(0.6)
    axrsi.spines['top'].set_color('white')
    axrsi.spines['top'].set_alpha(0.6)
    axrsi.spines['right'].set_color('white')
    axrsi.spines['right'].set_alpha(0.6)

    # Lines
    axrsi.axhline(70, color='red', linewidth=0.5)
    axrsi.axhline(30, color='green', linewidth=0.5)
    axrsi.set_yticks([30, 70])


def candlestick_graph_settings(ax1):
    """Configures the Candlesticks plot
    Args:
        ax1 (:obj:'matplotlib.axes.Axes':): Main axis
    """
    # Grid and labels
    ax1.grid(True, alpha=0.3, linestyle='dotted')
    ax1.set_ylabel('Stock Price', fontname='Arial', fontsize=14, labelpad=9)
    ax1.yaxis.set_ticks_position('left')
    ax1.yaxis.set_label_position('left')

    # Spines
    ax1.spines['bottom'].set_color('white')
    ax1.spines['bottom'].set_alpha(0.6)
    ax1.spines['left'].set_color('white')
    ax1.spines['left'].set_alpha(0.6)
    ax1.spines['top'].set_color('black')
    ax1.spines['right'].set_color('black')


def volume_graph_settings(axvolume, df):
    """Configures the Volume plot
    Args:
        axvolume (:obj:'matplotlib.axes.Axes':): Volume axis
        df (:obj:'pandas.DataFrame':): Stock's dataframe
    """
    # Grid and labels
    axvolume.grid(False)
    plt.setp(axvolume.get_yticklabels(), visible=False)
    axvolume.tick_params(axis='y', color='black')
    axvolume.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    for label in axvolume.xaxis.get_ticklabels():
        label.set_rotation(45)
    axvolume.set_xlabel(df.index[-1].strftime('%B %-d, %Y'),
                        fontname='Arial', fontsize=13, labelpad=9)

    # Spines
    axvolume.spines['top'].set_color('black')
    axvolume.spines['right'].set_color('black')


def graph_data(stock, df, fig, MA1, MA2):
    """Graphs everything
    Args:
        stock (str): Stock's name
        df (:obj:'pandas.DataFrame':): Stock's dataframe
        fig (:obj:'matplotlib.figure.Figure':): Figure
        MA1 (int): Fast Simple Moving Average
        MA2 (int): Slow Simple Moving Average
    """
    # General figure's settings
    fig.clf()
    fig.suptitle(stock, fontname='Arial', fontsize=16)
    plt.subplots_adjust(left=.12, right=.95, top=.92, bottom=.15, hspace=.21)

    # Calculate Moving Averages
    Av1 = indicators.movingaverage(df['Close'], MA1)
    Av2 = indicators.movingaverage(df['Close'], MA2)
    SP = len(df.index[MA2-1:])

    # Create subplots
    axvolume = plt.subplot2grid((5, 4), (1, 0), rowspan=4, colspan=4)
    axrsi = plt.subplot2grid((5, 4), (0, 0), sharex=axvolume, rowspan=1,
                             colspan=4)

    # Plot RSI
    rsi = indicators.rsi_function(df['Close'])
    axrsi.plot(df.index[-SP:], rsi[-SP:])
    axrsi.fill_between(df.index[-SP:], rsi[-SP:], 70, where=(rsi[-SP:] >= 70),
                       facecolor='red', edgecolor='red')
    axrsi.fill_between(df.index[-SP:], rsi[-SP:], 30, where=(rsi[-SP:] <= 30),
                       facecolor='green', edgecolor='green')

    # Plot Volume
    axvolume.fill_between(df.index[-SP:], 0, df['Volume'][-SP:],
                          facecolor='#00ffe8', alpha=0.2)
    axvolume.set_ylim(0, 1.1*df['Volume'].max())

    # Plot Candlesticks
    ax1 = axvolume.twinx()
    df_ohlc = df['Close'][-SP:].resample('3Min').ohlc()
    df_ohlc.reset_index(inplace=True)
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
    candlestick_ohlc(ax1, df_ohlc.values[-SP:], width=0.0005, colorup='g')

    # Plot Moving Averages
    label1 = str(MA1) + ' SMA'
    label2 = str(MA2) + ' SMA'
    ax1.plot(df.index[-SP:], Av1[-SP:], label=label1, linewidth=0.7)
    ax1.plot(df.index[-SP:], Av2[-SP:], label=label2, linewidth=0.7)
    ax1.legend(loc=9, ncol=2, prop={'size': 7}, fancybox=True)

    # Subplots' settings
    volume_graph_settings(axvolume, df)
    candlestick_graph_settings(ax1)
    rsi_graph_settings(axrsi)


def animate(i, ticker, stock_name, period, df, fig, MA1, MA2):
    """Updates and animates the graph
    Args:
        i (int): Interval
        ticker (str): Ticker symbol
        stock_name (str): Stock's namespace
        period (int): Intraday period (1 or 5 min)
        df (:obj:'pandas.DataFrame':): Stock's dataframe
        fig (:obj:'matplotlib.figure.Figure':): Figure
        MA1 (int): Fast Simple Moving Average
        MA2 (int): Slow Simple Moving Average
    """
    crawler.add_last_row(crawler.get_dictionary(ticker, period), df)
    graph_data(stock_name, df, fig, MA1, MA2)


def handle_close(evt):
    """Closes the figure
    Args:
        evt (event)
    """
    print('Closed Figure!')
    sys.exit()


def custom_exchandler(type, value, traceback):
    pass


def run(ticker, stock_name):
    """Runs the script and plots the graphs
    Args:
        ticker (str): Ticker symbol
        stock_name (str): Stock's name
    """

    # sys.excepthook = custom_exchandler
    style.use('dark_background')
    fig = plt.figure(figsize=(9, 6))
    fig.canvas.set_window_title('Stock Screener')
    fig.canvas.mpl_connect('close_event', handle_close)
    period = '1min'
    MA1 = 5  # fast MA
    MA2 = 13  # slow MA
    title = stock_name + ' ({})'.format(ticker)

    try:
        dict = crawler.get_dictionary(ticker, period)
    except Exception as e:
        sys.stderr.write('Error in the API')
        raise

    day = datetime.datetime.now(pytz.timezone('US/Eastern'))
    current_time = pd.to_datetime(day.strftime('%Y-%m-%d %-H:%-M'))
    open_time = pd.to_datetime(day.strftime('%Y-%m-%d') + ' 9:30')
    stock_market_is_open = current_time >= open_time and day.hour < 17

    if day.isoweekday() == 6 or current_time < open_time:
        day_to_graph = (day.date() - datetime.timedelta(days=1)).day
    elif day.isoweekday() == 7:
        day_to_graph = (day.date() - datetime.timedelta(days=2)).day
    else:
        day_to_graph = day.day

    try:
        df = crawler.parse_dictionary(dict, day_to_graph)
        df.set_index('Date', inplace=True)
    except Exception as e:
        print(e)
        raise

    while day.isoweekday() in range(1, 6) and stock_market_is_open:
        ani = animation.FuncAnimation(fig, animate, interval=30000,
                                      fargs=(ticker, title, period, df, fig,
                                             MA1, MA2))
        plt.show()

    graph_data(title, df, fig, MA1, MA2)
    plt.show()
