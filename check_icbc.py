import yfinance as yf
import pandas as pd

# 工商银行股票代码
# ticker = "601398.SS"  # A股
ticker = "1398.HK"   # H股

try:
    # 获取股票数据
    stock = yf.Ticker(ticker)
    
    # 获取基本信息
    info = stock.info
    
    print(f"=== 工商银行 ({ticker}) ===")
    print(f"当前价格: {info.get('currentPrice', 'N/A')}")
    print(f"今日涨跌: {info.get('regularMarketChange', 'N/A')} ({info.get('regularMarketChangePercent', 'N/A')}%)")
    print(f"开盘价: {info.get('regularMarketOpen', 'N/A')}")
    print(f"最高价: {info.get('dayHigh', 'N/A')}")
    print(f"最低价: {info.get('dayLow', 'N/A')}")
    print(f"成交量: {info.get('volume', 'N/A'):,}")
    print(f"市值: {info.get('marketCap', 'N/A'):,}")
    print(f"市盈率(PE): {info.get('trailingPE', 'N/A')}")
    print(f"市净率(PB): {info.get('priceToBook', 'N/A')}")
    print(f"股息率: {info.get('dividendYield', 'N/A')}")
    
    # 获取历史数据
    hist = stock.history(period="6mo")
    if not hist.empty:
        print(f"\n=== 6个月价格走势 ===")
        print(f"起始日期: {hist.index[0].strftime('%Y-%m-%d')}")
        print(f"结束日期: {hist.index[-1].strftime('%Y-%m-%d')}")
        print(f"起始价格: {hist['Close'].iloc[0]:.2f}")
        print(f"当前价格: {hist['Close'].iloc[-1]:.2f}")
        print(f"涨跌幅: {((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0] * 100):.2f}%")
        print(f"最高价: {hist['High'].max():.2f}")
        print(f"最低价: {hist['Low'].min():.2f}")
        
except Exception as e:
    print(f"错误: {e}")
    print("\n尝试安装依赖: pip install yfinance pandas")