from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.tools import yahoofinance
from pyalgotrade.technical import ma
from pyalgotrade.technical import ma

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, order):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.instrument = instrument
        self.setUseAdjustedValues(True)
        self.sma = ma.SMA(feed[instrument].getPriceDataSeries(), 15)
        self.position = None
        self.order = order


    def onBars(self, bars):
        if self.sma[-1] == None:
            return

        bar = bars[self.instrument]
        if (self.sma[-1] > bar.getPrice()) and self.position == None:
            print "buy "+ str(bar.getDateTime())
            self.position = self.enterLong(self.instrument, self.order, True)
        elif(self.sma[-1] < bar.getPrice() and self.position) :
            print "buy " + str(bar.getDateTime())
            self.position.exitMarket()
        #self.info("%s %s" % (bar.getClose(), self.__sma[-1]))

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info('BUY ' + str(self.order) + ' ' + tick + ' at $%.2f/share' % (execInfo.getPrice()))



    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info('SELL ' + str(self.order) + ' ' + tick + ' at $%.2f/share' % (execInfo.getPrice()))
        self.position = None


# Load the yahoo feed from the CSV file
filename = 'orcl-2016.csv'
tick = 'infy.ns'
year = 2016

yahoofinance.download_daily_bars(tick, year, filename)
feed = yahoofeed.Feed()
feed.addBarsFromCSV(tick, filename)

# Evaluate the strategy with the feed's bars.
myStrategy = MyStrategy(feed, tick, 10)
myStrategy.run()

