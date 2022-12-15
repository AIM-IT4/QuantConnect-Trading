#region imports
from AlgorithmImports import *
#endregion
# from quantconnect import *

from QuantConnect.Data.Custom import *
from QuantConnect.Data.Market import TradeBar, QuoteBar
from QuantConnect import *
from QuantConnect.Algorithm import *

class SimpleTradingAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2018, 1, 1)
        self.SetEndDate(2018, 12, 31)
        self.SetCash(100000)

        self.AddEquity("SPY", Resolution.Daily)

    def OnData(self, data):
        if not self.Portfolio.Invested:
            self.MarketOrder("SPY", 1000)
