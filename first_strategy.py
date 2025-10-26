import akshare as ak
import backtrader as bt
import matplotlib.pyplot as plt

class TestStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        
    def next(self):
        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                self.buy()
        else:
            if len(self) >= (self.bar_executed + 5):
                self.close()

# 获取数据
stock_data = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20200101", end_date="20231231")
print("数据获取成功！")
print(stock_data.head())

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
plt.figure(figsize=(12, 6))
plt.plot(stock_data['日期'], stock_data['收盘'])
plt.title('平安银行股价走势')
plt.show()