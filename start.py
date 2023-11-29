import os
from datetime import date
import pandas as pd


from modules import forecast 
from make_data.get_macro_data import get_macro_data
from make_data.get_currency_data import get_currency_data
from make_data.concat_data import concat_data
from features.indicators import TechnicalIndicators
from order import place_an_order


pair = "USDSGD"
start_date = "01/01/2009"
end_start = "08/31/2023"
forecast_day = '2023-09-01'

currencies = get_currency_data(
    pair, start_date, end_start,
    "EURGBP", "EURUSD", "GBPUSD", "EURSGD"
)

macroData = get_macro_data(
    start_date, end_start,
    "USA", "China",
    "Germany", "Singapore",
    "France", "GB"
)

dataset = concat_data(currencies, macroData)


if __name__ == "__main__":
    lookback = 20
    finalData = TechnicalIndicators(dataset, lookback)
    df = finalData.returnData()
    df.to_csv(
        f"{os.getcwd()}/datasets/data_for_prediction/IB_{pair.lower().replace('/', '')}_{date.today() - pd.Timedelta(days=1)}.csv"
    )
    print("Data uploaded!")
    forecast = forecast.make_forecast(df, forecast_day)
    print(f"Forecast for {forecast_day} = {forecast}")
    
    place_an_order(forecast)






