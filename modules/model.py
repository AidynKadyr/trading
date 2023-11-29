import pandas as pd
import numpy as np
from modules.sample_weights import create_sample_weights

def predict(df, dates, model, weights):
    """
    Generate predictions using the specified model.

    Args:
        df (pandas.DataFrame): DataFrame containing the data.
        dates (list): List of dates for which predictions are to be made.
        model: Trained model for making predictions.

    Returns:
        pandas.Series: Series of predictions.

    """
    y_pred_all = np.zeros(shape=(len(dates) - 1))

    for i in range(len(dates) - 1):
        regressor = model
        y_train = df["Close"][: dates[i]]
        X_train = df.drop(["Close"], axis=1)[: dates[i]]

        if weights:
            sample_weights = create_sample_weights(X_train)
            regressor.fit(X_train, y_train, sample_weight=sample_weights)
        else:
            regressor.fit(X_train, y_train)
            
        X_test = df.drop(["Close"], axis=1).loc[[dates[i + 1]]]
        y_predict = regressor.predict(X_test)[0]

        y_pred_all[i] = y_predict

    predictions = pd.Series(y_pred_all, index=dates[1:]).round(5)
    return predictions[-1]
