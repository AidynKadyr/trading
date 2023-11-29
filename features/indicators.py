import pandas as pd
from ta.momentum import RSIIndicator, StochasticOscillator
import talib
from .patterns import CandlestickPatterns
import numpy as np


class TechnicalIndicators:
    def __init__(self, df, lookback) -> None:
        self.df = df
        self.featurecalculator()
        self.bollinger_bands()
        self.get_adx(lookback)
        # self.indicators(lookback)
        # self.candleStcikPatter()

    def candleStcikPatter(self):
        for pattern in CandlestickPatterns.keys():
            pattern_function = getattr(talib, pattern)
            self.df[CandlestickPatterns[pattern]] = pattern_function(
                self.df["Open"], self.df["High"],
                self.df["Low"], self.df["Close"]
            )

    def featurecalculator(self):
        # exponential moving average of window 9
        self.df["EMA_9"] = self.df["Close"].ewm(
            span=9, min_periods=9).mean()
        # moving average of window 5, 10
        self.df["SMA_5"] = self.df["Close"].rolling(window=5).mean()
        self.df["SMA_10"] = self.df["Close"].rolling(window=10).mean()

        EMA_12 = pd.Series(self.df["Close"].ewm(
            span=12, min_periods=12).mean())
        EMA_26 = pd.Series(self.df["Close"].ewm(
            span=26, min_periods=26).mean())
        self.df["MACD"] = pd.Series(EMA_12 - EMA_26)
        # calculates Relative Strength Index
        self.df["RSI"] = RSIIndicator(self.df["Close"]).rsi()
        # calculates Stochastic Oscillator
        self.df["Stochastic"] = StochasticOscillator(
            self.df["High"], self.df["Low"], self.df["Close"]
        ).stoch()

        high_low = self.df["High"] - self.df["Low"]
        high_close = np.abs(self.df["High"] - self.df["Close"].shift())
        low_close = np.abs(self.df["Low"] - self.df["Close"].shift())

        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)

        self.df["ATR"] = true_range.rolling(14).sum() / 14

    def bollinger_bands(self):
        n = 20
        m = 2
        # takes dataframe on input
        # n = smoothing length
        # m = number of standard deviations away from MA

        # typical price
        TP = (self.df["High"] + self.df["Low"] + self.df["Close"]) / 3
        # but we will use Adj close instead for now, depends

        data = TP
        # data = df['Adj Close']

        # takes one column from dataframe
        B_MA = pd.Series((data.rolling(n, min_periods=n).mean()), name="B_MA")
        sigma = data.rolling(n, min_periods=n).std()

        BU = pd.Series((B_MA + m * sigma), name="BU")
        BL = pd.Series((B_MA - m * sigma), name="BL")

        self.df = self.df.join(B_MA)
        self.df = self.df.join(BU)
        self.df = self.df.join(BL)

    def get_adx(self, lookback):
        high = self.df["High"]
        low = self.df["Low"]
        close = self.df["Close"]
        plus_dm = high.diff()
        minus_dm = low.diff()
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm > 0] = 0

        tr1 = pd.DataFrame(high - low)
        tr2 = pd.DataFrame(abs(high - close.shift(1)))
        tr3 = pd.DataFrame(abs(low - close.shift(1)))
        frames = [tr1, tr2, tr3]
        tr = pd.concat(frames, axis=1, join="inner").max(axis=1)
        atr = tr.rolling(lookback).mean()

        plus_di = 100 * (plus_dm.ewm(alpha=1 / lookback).mean() / atr)
        minus_di = abs(100 * (minus_dm.ewm(alpha=1 / lookback).mean() / atr))
        dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
        adx = ((dx.shift(1) * (lookback - 1)) + dx) / lookback
        adx_smooth = adx.ewm(alpha=1 / lookback).mean()

        self.df["plus_di"] = plus_di
        self.df["minus_di"] = minus_di
        self.df["adx"] = adx_smooth
        self.df = self.df.dropna()

    def indicators(self, lookback):
        rsi = talib.RSI(self.df["Close"], timeperiod=20)
        rsiBuySell = (rsi < 30) & (rsi.shift(1) >= 30)
        self.df["RSI"] = rsiBuySell.astype(int)

        slowk, slowd = talib.STOCH(
            self.df["High"],
            self.df["Low"],
            self.df["Close"],
            fastk_period=5,
            slowk_period=3,
            slowk_matype=0,
            slowd_period=3,
            slowd_matype=0,
        )
        stochBuySell = ((slowk > slowd) & (slowk.shift(1) < slowd.shift(1))) & (
            slowd < 20
        )
        self.df["Stochastic"] = stochBuySell.astype(int)

        for i in [10, 20, 30, 50, 100]:
            shortSMA = talib.SMA(self.df["Close"], i)
            longSMA = talib.SMA(self.df["Close"], i - i / 2)
            smaBuySell = (shortSMA >= longSMA) & (shortSMA.shift(1) <= longSMA.shift(1))
            self.df[f"SMA_{i}"] = smaBuySell.astype(int)

        tredADX = talib.ADX(
            self.df["High"], self.df["Low"], self.df["Close"],
            timeperiod=lookback
        )
        trendYes = tredADX > 25
        self.df["ADX"] = trendYes.astype(int)

    def returnData(self):
        return self.df
