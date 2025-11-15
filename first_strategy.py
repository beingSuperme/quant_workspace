import akshare as ak
import backtrader as bt
import matplotlib.pyplot as plt
import pandas as pd

class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')
    
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        
    def next(self):
        # 检查是否有未完成的订单
        if self.order:
            return
            
        if not self.position:
            # 空仓时，如果当前收盘价小于前一天收盘价，则买入
            if self.dataclose[0] < self.dataclose[-1]:
                self.log(f'买入 {self.dataclose[0]:.2f}')
                self.order = self.buy()
        else:
            # 持仓时，如果持有超过5个周期，则卖出
            if len(self) >= (self.bar_executed + 5):
                self.log(f'卖出 {self.dataclose[0]:.2f}')
                self.order = self.close()
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # 订单已提交/已接受，等待成交
            return

        # 订单已完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'买入执行 {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'卖出执行 {order.executed.price:.2f}')
                
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单取消/保证金不足/被拒绝')
            
        self.order = None

# 获取数据
stock_data = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20200101", end_date="20231231")
print("数据获取成功！")
print(stock_data.head())

# 数据预处理
stock_data['日期'] = pd.to_datetime(stock_data['日期'])
stock_data.set_index('日期', inplace=True)

# 绘制股价走势
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
plt.figure(figsize=(12, 6))
plt.plot(stock_data.index, stock_data['收盘'])
plt.title('平安银行股价走势')
plt.xlabel('日期')
plt.ylabel('收盘价')
plt.grid(True)
plt.show()

# Backtrader回测
cerebro = bt.Cerebro()
cerebro.addstrategy(TestStrategy)

# 准备数据格式
data = bt.feeds.PandasData(dataname=stock_data)
cerebro.adddata(data)

# 设置初始资金
cerebro.broker.setcash(100000.0)
cerebro.broker.setcommission(commission=0.001)  # 设置手续费

print(f'初始资金: {cerebro.broker.getvalue():.2f}')
cerebro.run()
print(f'最终资金: {cerebro.broker.getvalue():.2f}')

# 绘制回测结果
cerebro.plot()