import pandas as pd
import numpy as np


def zigzag(xohlc, high_source, low_source, devtol):
    data_count = len(xohlc)
    pivots = [0] * data_count
    updir = xohlc['Close'][0] > xohlc['Open'][0]
    last_low_index = 0
    last_high_index = 0

    i = 0
    while i < data_count:

        new_higher_high = xohlc[high_source][i] > xohlc[high_source][last_high_index]
        new_higher_low = xohlc[low_source][i] > xohlc[low_source][last_low_index]
        new_lower_high = xohlc[high_source][i] < xohlc[high_source][last_high_index]
        new_lower_low = xohlc[low_source][i] < xohlc[low_source][last_low_index]

        if updir:
            deviation = abs(xohlc[low_source][last_high_index] -
                            xohlc[low_source][i]) / xohlc[low_source][last_high_index]

            if deviation > devtol and not new_higher_high and new_lower_low:
                pivots[last_high_index] = -1
                updir = False
                last_low_index = i
            else:
                last_high_index = i if new_higher_high else last_high_index
                last_low_index = i if new_higher_low else last_low_index
        else:
            deviation = abs(xohlc[high_source][last_low_index] -
                            xohlc[high_source][i]) / xohlc[high_source][last_low_index]
            if deviation > devtol and not new_lower_low and new_higher_high:
                pivots[last_low_index] = +1
                updir = True
                last_high_index = i
            else:
                last_high_index = i if new_lower_high else last_high_index
                last_low_index = i if new_lower_low else last_low_index
        i = i + 1

    return pd.Series(pivots)


def split_signals(data):
    return {"long": data.index[data == -1], "short": data.index[data == +1]}
