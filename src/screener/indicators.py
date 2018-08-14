"""This module contains the mathematical formulas to calculate several
stock indicators
"""

__author__ = 'Andres Beltran'
__version__ = '1.0'

import numpy as np


def movingaverage(values, window):
    """Calculates a Simple Moving Average
    Args:
        values (int): The integer value of the current moving average
        window (int): The window used to calculate the current moving average
    Returns:
        int: The Moving Average with the specified values
    """
    weights = np.repeat(1.0, window)/window
    smas = np.convolve(values, weights, 'valid')
    return smas


def rsi_function(prices, period=14):
    """Calculates the Relative Strength Index (RSI)
    Args:
        prices ([int]): The integer value of the current moving average
        period (int): The number of data points used to calculate the RSI
    Returns:
        [int]: The list containg the values for the RSI
    """
    deltas = np.diff(prices)
    seed = deltas[:period+1]
    up = seed[seed >= 0].sum()/period
    down = -seed[seed < 0].sum()/period
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100./(1. + rs)

    for i in range(period, len(prices)):
        delta = deltas[i-1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(period-1)+upval)/period
        down = (down*(period-1)+downval)/period
        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi
