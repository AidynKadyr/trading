import pandas as pd
import time
from xgboost import XGBRegressor

from config import (
    start_day,
    forecast_day,
    dataset_name,
    exp_id,
    save,
    n_estimators_list,
    max_depth_list,
    eta_list,
    gamma_list,
    min_child_weight_list,
    lambda_list,
    alpha_list,
    objective_list,
    weights
)

from data_processing import (
    create_next_day_dates,
    create_lagged_features,
    create_lagged_target,
)

from evaluate import evaluate
from hyperparameters import get_all_params
from model import predict



"""
This script performs the following steps:
1. Reads the dataset from a CSV file.
2. Applies data processing inclduing lagged features and target.
3. Generates a list of hyperparameter combinations using the get_all_params function.
4. Iterates over the hyperparameter combinations and performs predictions using the XGBoost regressor.
5. Evaluates the predictions and stores the scores in a DataFrame.
6. Prints the scores DataFrame and the total execution time.
"""

if __name__ == "__main__":
    start_time = time.time()

    dataset = pd.read_csv(
        f"../../data/data_for_simulation/{dataset_name}", index_col=0, parse_dates=True
    )
    data = dataset.copy()

    df = create_next_day_dates(data)
    df = create_lagged_features(df, 1)
    df = create_lagged_target(df, 5)

    scores_df = pd.DataFrame()
    dates = pd.date_range(start=start_day, end=forecast_day, freq="B")

    hyperparameters_list = get_all_params(
        n_estimators_list,
        max_depth_list,
        eta_list,
        gamma_list,
        min_child_weight_list,
        lambda_list,
        alpha_list,
        objective_list,
    )

    for params in hyperparameters_list:
        iteration_start = time.time()

        print(f"Parameters: {params}")
        params_name = (
            f'{exp_id}_{params["n_estimators"]}_'
            f'{params["max_depth"]}_{params["eta"]}_{params["gamma"]}_'
            f'{params["min_child_weight"]}_{params["lambda"]}_{params["alpha"]}_{params["objective"]}'
        )
    #     features_to_pca1 = [ 'EURGBP_L1', 'EURUSD_L1', 'GBPUSD_L1',
    #    'USDCNY_L1', 'EURSGD_L1']

    #     features_to_pca2 = ['Open_L1', 'High_L1', 'Low_L1', 'Close_L1']

    #     features_to_pca2 = ['EMA_9_L1',
    #    'SMA_5_L1', 'SMA_10_L1', 'MACD_L1', 'RSI_L1', 'Stochastic_L1', 'ATR_L1',
    #    'B_MA_L1', 'BU_L1', 'BL_L1', 'plus_di_L1', 'minus_di_L1', 'adx_L1']
        
        y_pred = predict(
            df, 
            dates, 
            XGBRegressor(**params, tree_method="gpu_hist"), 
            weights
            #,features_to_pca1, features_to_pca2,  number_of_pca_components = 2
        )

        y_test = df["Close"].loc[dates][1:-1]
        ohlc_df = dataset[["Open", "High", "Low", "Close"]]
        scores = evaluate(y_test, ohlc_df, y_pred, params_name)

        scores_df = pd.concat([scores_df, scores])
        scores_df = scores_df.sort_values("Profit", ascending=False)
        if save:
            scores_df.to_csv(f"Results/{exp_id}.csv")
        
        iteration_end = time.time()
        iteration_time = iteration_end - iteration_start
        print(f"TIME: {iteration_time}")

    print(scores_df)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"TIME: {execution_time}")
