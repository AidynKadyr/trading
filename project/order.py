from ib_insync import *
from datetime import datetime, time


def get_last_close(ib, contract):
    bars = ib.reqHistoricalData(
        contract,
        endDateTime="",
        durationStr="2 D",
        barSizeSetting="1 day",
        whatToShow="MIDPOINT",
        useRTH=True,
    )
    return util.df(bars)["close"].iloc[-1]


def calculate_limit_price(ib, contract):
    ticker = ib.reqMktData(contract, snapshot=True)
    ib.sleep(2)  # Wait for data to be received
    bid_price = ticker.bid
    ask_price = ticker.ask
    return (bid_price + ask_price) / 2


def place_an_order(forecast):
    # Replace this with actual prediction from your XGBoost model
    prediction = forecast

    ib = IB()
    ib.connect("127.0.0.1", 7497, clientId=1)
    contract = Forex("USDSGD")

    yesterday_close = get_last_close(ib, contract)

    # Calculate the desired execution time
    desired_execution_time = time(16, 47)  # 7:15 PM

    # Get the current time
    current_time = datetime.now().time()

    # Calculate the time until the desired execution time
    time_to_wait = (
        datetime.combine(datetime.today(), desired_execution_time)
        - datetime.combine(datetime.today(), current_time)
    ).total_seconds()

    print("Sleeping until desired execution time...")
    ib.sleep(max(0, time_to_wait - 2))  # Account for additional 2 seconds

    limit_price = calculate_limit_price(ib, contract)

    if prediction >= yesterday_close:
        action = "BUY"
    elif prediction < yesterday_close:
        action = "SELL"
    else:
        action = None

    limit = True

    if action:
        if limit:
            order = LimitOrder(action, 9000, limit_price)
        else:
            order = MarketOrder(action, 9000)  # buys at the ask, sells at the bid

        print(f"Prediction = {prediction:.5f}")
        print(f"Last Close = {yesterday_close:.5f}")
        print(f"{action} order created at price: {limit_price:.5f}")

        trade = ib.placeOrder(contract, order)
        print(trade)

        def order_filled(trade, fill):
            print("ORDER HAS BEEN FILLED")
            print(order)
            print(fill)

        trade.fillEvent += order_filled  # 14mintues

        ib.run()

    # ib.disconnect()


if __name__ == "__main__":
    place_an_order()
