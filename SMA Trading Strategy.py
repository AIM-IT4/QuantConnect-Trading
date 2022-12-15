#region imports
from AlgorithmImports import *
#endregion
# from quantconnect import *

# Import necessary libraries
# import quantconnect.algorithm as algo
# import quantconnect.data.market as market
# import quantconnect.data.fundamental as fundamental
# import quantconnect.orders as orders

class SimpleMovingAverageAlgorithm(QCAlgorithm):
    def Initialize(self):
        # Set the cash we'd like to use for our backtest
        self.SetCash(100000)

        # Set the symbol we'd like to use for our backtest
        self.symbol = self.AddEquity("SPY").Symbol

        # Set the time frame for our simple moving average
        self.time_frame = 30

        # Set our simple moving average
        self.sma = self.SMA(self.symbol, self.time_frame)

        # Schedule an event to be fired every day at 4:00 PM
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.At(16, 0), self.Trade)

    def Trade(self):
        # If we don't have data for our simple moving average, do nothing
        if not self.sma.IsReady:
            return

        # Get the current price of the security
        current_price = self.Securities[self.symbol].Price

        # If the current price is greater than our simple moving average, buy
        if current_price > self.sma.Current.Value:
            self.Log("Purchasing {0}".format(self.symbol.Value))
            self.Order(self.symbol, 1)

        # If the current price is less than our simple moving average, sell
        elif current_price < self.sma.Current.Value:
            self.Log("Selling {0}".format(self.symbol.Value))
            self.Order(self.symbol, -1)

# # Create an instance of our algorithm
# algo = SimpleMovingAverageAlgorithm()

# # Run the algorithm
# algo.Run()
