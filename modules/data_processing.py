from pandas.tseries.offsets import BDay

dt_columns = ["Year", "Month", "Week", "Dayofweek", "Day", "Dayofyear"]


def create_next_day_dates(df):
    """
    Create a new row for the next day and fill in calendar data for that date.

    Args:
        df (pandas.DataFrame): DataFrame containing calendar data.

    Returns:
        pandas.DataFrame: DataFrame with the next day's calendar data added.

    """
    df = df.copy()
    last_day = df.index[-1]
    nxt_day = last_day + BDay(1)
    df.loc[nxt_day] = 0
    df.loc[nxt_day, dt_columns] = [
        nxt_day.year,
        nxt_day.month,
        nxt_day.week,
        nxt_day.dayofweek,
        nxt_day.day,
        nxt_day.dayofyear,
    ]
    return df


def create_lagged_features(df, num_lags):
    """
    Create new columns with lagged versions of features.

    Args:
        df (pandas.DataFrame): DataFrame containing features.
        num_lags (int): Number of lagged versions to create.

    Returns:
        pandas.DataFrame: DataFrame with lagged features added.

    """
    df = df.copy()
    lagged_features = df.drop(dt_columns + ["Close"], axis=1).columns
    for feature in lagged_features:
        for i in range(1, num_lags + 1):
            df[f"{feature}_L{i}"] = df[feature].shift(i)

    df.drop(lagged_features, axis=1, inplace=True)
    return df


def create_lagged_target(df, lags):
    """
    Create lagged target variable.

    Args:
        df (pandas.DataFrame): DataFrame containing target variable.
        lags (int): Number of lagged versions to create.

    Returns:
        pandas.DataFrame: DataFrame with lagged target variable added.

    """
    df = df.copy()
    for i in range(1, lags + 1):
        df[f"Close_L{i}"] = df["Close"].shift(i)
    df = df.dropna()
    return df
