import pandas as pd
from xgboost import XGBRegressor

from modules.data_processing import (
    create_next_day_dates,
    create_lagged_features,
    create_lagged_target,
)

from modules.model import predict


def make_forecast(data, forecast_day):
    dates = pd.date_range(
                        start=pd.Timestamp(forecast_day) - pd.tseries.offsets.BusinessDay(1), 
                        end=forecast_day, freq="B")

    df = create_next_day_dates(data)
    df = create_lagged_features(df, 1)
    df = create_lagged_target(df, 5)


    y_pred = predict(
        df, 
        dates, 
        XGBRegressor(), 
        True
    )
    return y_pred

