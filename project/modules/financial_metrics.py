import numpy as np


def calculate_performance_metrics(results, risk_free_rate=0.0):
    # Calculate Total Return
    initial_balance = results["Balance"].iloc[0]
    final_balance = results["Balance"].iloc[-1]
    total_return = (final_balance - initial_balance) / initial_balance

    # Calculate Annualized Return
    num_years = (
        results.index[-1] - results.index[0]
    ).days / 365.0  # number of days in the period divided by 365 to get number of years.
    annualized_return = (1.0 + total_return) ** (1.0 / num_years) - 1.0

    # Calculate Daily Returns
    results["Daily Return"] = results["Balance"].pct_change()

    # Calculate Sharpe Ratio
    daily_risk_free_rate = (1.0 + risk_free_rate) ** (1.0 / 365.0) - 1.0
    excess_daily_returns = results["Daily Return"] - daily_risk_free_rate
    sharpe_ratio = (excess_daily_returns.mean() / excess_daily_returns.std()) * np.sqrt(
        252.0
    )

    # Calculate Maximum Drawdown
    cumulative_returns = (1.0 + results["Daily Return"]).cumprod()
    previous_peaks = cumulative_returns.cummax()
    drawdown = (cumulative_returns / previous_peaks) - 1.0
    max_drawdown = drawdown.min()

    # Calculate Win Rate
    num_winning_trades = (results["PnL"] >= 0).sum()
    num_total_trades = len(results)
    win_rate = num_winning_trades / num_total_trades

    # Calculate Profit Factor
    total_profit = results[results["PnL"] > 0]["PnL"].sum()
    total_loss = results[results["PnL"] < 0]["PnL"].sum()
    profit_factor = abs(total_profit / total_loss)

    # Create a dictionary to store the calculated metrics
    performance_metrics = {
        "Total Return(%)": total_return * 100,
        "CAGR(%)": annualized_return * 100,
        "Sharpe": sharpe_ratio,
        "Max Drawdown(%)": max_drawdown * 100,
        "WinR(%)": win_rate * 100,
        "PrftFactor": profit_factor,
    }

    return performance_metrics  # pd.DataFrame(performance_metrics, index = ['Metrics'])
