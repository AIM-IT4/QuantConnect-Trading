# region imports
from AlgorithmImports import *
# endregion

from QuantConnect.Data.Consolidators import TradeBarConsolidator
from QuantConnect.Indicators import *
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Data.Market import TradeBar

class UpgradedBlueRabbit(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 6, 14)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        self.spy = self.AddEquity("SPY", Resolution.Daily)
        self.bnd = self.AddEquity("BND", Resolution.Daily)
        self.aapl = self.AddEquity("AAPL", Resolution.Daily)

        # Add a 50-day simple moving average to the SPY and BND data
        self.spy_sma = self.SMA("SPY", 50)
        self.bnd_sma = self.SMA("BND", 50)

        # Add a 14-day relative strength index (RSI) to the AAPL data
        self.aapl_rsi = self.RSI("AAPL", 14)

        # Consolidate daily data into weekly data for more efficient processing
        self.spy_consolidator = TradeBarConsolidator(timedelta(7))
        self.bnd_consolidator = TradeBarConsolidator(timedelta(7))
        self.aapl_consolidator = TradeBarConsolidator(timedelta(7))

        self.spy_consolidator.DataConsolidated += self.OnSpyDataConsolidated
        self.bnd_consolidator.DataConsolidated += self.OnBndDataConsolidated
        self.aapl_consolidator.DataConsolidated += self.OnAaplDataConsolidated

        self.SubscriptionManager.AddConsolidator("SPY", self.spy_consolidator)
        self.SubscriptionManager.AddConsolidator("BND", self.bnd_consolidator)
        self.SubscriptionManager.AddConsolidator("AAPL", self.aapl_consolidator)

    def OnData(self, data: Slice):
        pass

    def OnSpyDataConsolidated(self, sender, bar):
        if self.Portfolio.Invested and self.spy_sma.Current.Value < bar.Close:
            self.Liquidate()
        elif not self.Portfolio.Invested and self.spy_sma.Current.Value > bar.Close:
            self.SetHoldings("SPY", 0.33)

    def OnBndDataConsolidated(self, sender, bar):
        if self.Portfolio.Invested and self.bnd_sma.Current.Value < bar.Close:
            self.Liquidate()
        elif not self.Portfolio.Invested and self.bnd_sma.Current.Value > bar.Close:
            self.SetHoldings("BND", 0.33)

    def OnAaplDataConsolidated(self, sender, bar):
        if self.aapl_rsi.Current.Value < 30:
            self.SetHoldings("AAPL", 0.33)
        elif self.aapl_rsi.Current.Value > 70:
            self.Liquidate()
