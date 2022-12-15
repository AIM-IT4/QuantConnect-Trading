#region imports
from AlgorithmImports import *
#endregion
# from quantconnect import *

# Import necessary libraries
# import quantconnect.algorithm as algo
# import quantconnect.data.market as market
# import quantconnect.data.fundamental as fundamental
# import quantconnect.orders as orders

# Import necessary libraries


class PairsTradingStrategy(QCAlgorithm):
    def Initialize(self):
        # Set the cash we'd like to use for our backtest
        self.SetCash(100000)

        # Set the trading securities
        self.security1 = self.AddEquity("SPY", Resolution.Daily)
        self.security2 = self.AddEquity("AAPL", Resolution.Daily)

        # Set the lookback period for calculating the spread
        self.lookback = 20

        # Set the mean reversion threshold
        self.threshold = 0.5

    def on_data(self, data):
        # Get the current prices of the securities
        price1 = data[self.security1].price
        price2 = data[self.security2].price

        # Calculate the spread
        spread = (price1 / price2) - self.history(self.security1, self.lookback, Resolution.Daily)[0].close / self.history(self.security2, self.lookback, Resolution.Daily)[0].close

        # Check if we have no positions in the securities
        if not self.portfolio.positions[self.security1].amount and not self.portfolio.positions[self.security2].amount:
            # If the spread is above the mean reversion threshold, go long on the first security and short on the second
            if spread > self.threshold:
                self.order(self.security1, 1)
                self.order(self.security2, -1)
        # If we have positions in the securities
        else:
            # If the spread is below the mean reversion threshold, close the positions
            if spread < -self.threshold:
                self.liquidate()

