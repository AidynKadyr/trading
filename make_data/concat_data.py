import pandas as pd


def concat_data(currencies_data, macro_data):
    df = pd.concat([currencies_data, macro_data], axis=1)
    df = df.dropna()

    df["Year"] = pd.DatetimeIndex(df.index).year
    df["Month"] = pd.DatetimeIndex(df.index).month
    df["Week"] = pd.DatetimeIndex(df.index).week
    df["Dayofweek"] = pd.DatetimeIndex(df.index).dayofweek
    df["Day"] = pd.DatetimeIndex(df.index).day
    df["Dayofyear"] = pd.DatetimeIndex(df.index).dayofyear

    return df
