import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
    r2_score,
)
from backtest import run_backtest
from financial_metrics import calculate_performance_metrics
from config import position_size, commission_per_trade


def evaluate(true_target, ohlc_df, predictions, params_name):
    """
    Evaluate the performance of a predictive model by computing various metrics and backtesting.

    Args:
        df (pandas.DataFrame): The original DataFrame containing the 'Close' prices.
        dates (list): List of dates for evaluation.
        predictions (pandas.Series): Predicted values corresponding to the evaluation dates.
        params_name (str): Name of the parameters used for the evaluation.

    Returns:
        pandas.DataFrame: Evaluation results including metrics and profit.

    """

    # Extract test data and predictions
    predicted_target = predictions.values[:-1] 

    # Compute evaluation metrics
    mse = mean_squared_error(true_target, predicted_target)
    rmse = mean_squared_error(true_target, predicted_target, squared=False)
    mae = mean_absolute_error(true_target, predicted_target)
    mape = mean_absolute_percentage_error(true_target, predicted_target)
    r2 = r2_score(true_target, predicted_target)

    bt_data = pd.concat([ohlc_df, predictions], axis=1)
    bt_data.rename(columns={0: "Predicted"}, inplace=True)
    bt_data.dropna(inplace=True)


    # Run backtest
    profit, backtest_df = run_backtest(bt_data, position_size, commission_per_trade)

    # Create a dictionary with evaluation results
    res = {
       # "MSE": [mse],
        "RMSE": [rmse],
        "MAE": [mae],
       # "MAPE": [mape],
        "R2": [r2],
        "Profit": [profit],
    }

    # Create a DataFrame from the results dictionary
    metrics = calculate_performance_metrics(backtest_df, risk_free_rate=0.04)
    res.update(metrics)  # combine two dictionaries res and metrics
    df_scores = pd.DataFrame(res, index=[params_name]).round(5)

    return df_scores
