import bt
import matplotlib.pyplot as plt
import pandas as pd

data = bt.get('^NSEI', start='2016-01-01')
#print data
#sma  = pd.rolling_mean(data,34)
df = pd.DataFrame(data)
#print df
sma = df.rolling(window=34,center=False).mean()
#print sma

strategy = bt.Strategy('Price-MA Cross', [bt.algos.SelectWhere(data>sma),
                                           bt.algos.WeighEqually(),
                                           bt.algos.Rebalance()
                                           ])
test = bt.Backtest(strategy, data)
result = bt.run(test)
print result
result.plot(), result.display()
plt.show()
