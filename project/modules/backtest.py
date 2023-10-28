import pandas as pd


def run_backtest(historical_data, position_size, commission):
    """
    Run a backtest on historical data to calculate profit and loss (PnL) based on positions.

    Args:
        historical_data (pandas.DataFrame): Historical data including 'Open',
        'Close', and 'Predicted' columns.
        position_size (float): Size of the position.
        commission (float): Commission for openning or closing a trade.

    Returns:
        float: Total profit and loss (PnL) from the backtest.
        Dataframe: Dataframe containing "Balance", "PnL", "Open", "Close" 
        data for each position.

    """
    balance = position_size

    # Create a new DataFrame to store the results
    results = pd.DataFrame(
        index=historical_data.index,
        columns=["Balance", "PnL", "Position", "Open", "Close"],
    )

    # Loop through the historical data
    for i in range(len(historical_data) - 1):
        today = historical_data.iloc[i]
        tomorrow = historical_data.iloc[i + 1]

        # Check for long position
        if today["Close"] <= tomorrow["Predicted"]:
            position = "Long"
            openprice = tomorrow["Open"]
            closeprice = tomorrow["Close"]

            units_to_buy = position_size / openprice
            PnL = (closeprice - openprice) * units_to_buy - commission * 2
            balance += PnL

        # Check for short position
        elif today["Close"] > tomorrow["Predicted"]:
            position = "Short"
            openprice = tomorrow["Open"]
            closeprice = tomorrow["Close"]

            units_to_sell = position_size / openprice
            PnL = (openprice - closeprice) * units_to_sell - commission * 2
            balance += PnL

        # Update the results DataFrame
        results.loc[tomorrow.name] = [balance, PnL, position, openprice, closeprice]

    results.dropna(inplace=True)
    results[["Balance", "PnL", "Open", "Close"]] = results[
        ["Balance", "PnL", "Open", "Close"]
    ].astype(float)
    return results["PnL"].sum(), results
