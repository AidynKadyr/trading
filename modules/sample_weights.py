import numpy as np
def create_sample_weights(X_train):
    """
    Define sample weights parameter for XGBoost such that the last year
    weights the same as everything before that year.

    Args:
        X_train (pandas.DataFrame): Training dataset.

    Returns:
        numpy.ndarray: Sample weights for XGBoost.

    """
    year_ago = X_train[
        (X_train["Year"] == X_train.index[-1].year - 1)
        & (X_train["Month"] == X_train.index[-1].month)
    ].index[-1]

    weights1 = np.ones(len(X_train[:year_ago]))
    weights2 = np.ones(len(X_train[year_ago:][1:])) * (
        len(X_train[:year_ago]) / len(X_train[year_ago:][1:])
    )
    sample_weights = np.append(weights1, weights2)

    return sample_weights