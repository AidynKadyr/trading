# -*- coding: utf-8 -*-
import re
import pandas as pd
from ib_insync import Forex, util
from .ib_connection import ib_connection


@ib_connection
def get_currency_data(main_currency,
                      start_date=0, end_date=0,
                      *other_pairs, ib=None):
    """
    This function retrieves historical currency data for the main currency
    and any other pairs specified.
    The data includes the open, high, low, and close prices.

    Parameters:
        main_currency (str): The main currency for which to retrieve data.
        start_date (int, optional): The start date for which to retrieve data.
        end_date (int, optional): The end date for which to retrieve data.
        *other_pairs (str): Additional currency pairs for which to retrieve data.

    Returns:
        df_main (pd.DataFrame): A DataFrame containing the historical currency
        data for the main currency and other pairs.
    """

    df_main = pd.DataFrame()
    main_bars = ib.reqHistoricalData(
        Forex(main_currency),
        endDateTime="",
        durationStr="14 Y",
        barSizeSetting="1 day",
        whatToShow="MIDPOINT",
        useRTH=True,
        formatDate=1,
        keepUpToDate=True,
    )
    df_main[["date", "Open", "High", "Low", "Close"]] = util.df(main_bars)[
        ["date", "open", "high", "low", "close"]
    ]
    df_main = df_main.set_index("date")
    df_main.index = pd.to_datetime(df_main.index)

    for pairs in other_pairs:

        df_pair = pd.DataFrame()
        pair_bars = ib.reqHistoricalData(
            Forex(pairs),
            endDateTime="",
            durationStr="14 Y",
            barSizeSetting="1 day",
            whatToShow="MIDPOINT",
            useRTH=True,
            formatDate=1,
            keepUpToDate=True,
        )
        df_pair[["date", pairs]] = util.df(pair_bars)[["date", "close"]]
        df_pair = df_pair.set_index("date")
        df_pair.index = pd.to_datetime(df_pair.index)
        df_main = df_main.merge(df_pair, on="date", how="inner")

    df_main = df_main.resample("B").mean()
    df_main = df_main.fillna(method="ffill")
    ib.disconnect()
    return df_main
