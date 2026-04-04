import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from datetime import datetime, timedelta
import os

print("=== 工商银行 (ICBC) 股票分析报告 ===\n")

# 工商银行股票代码
tickers = {
    "A股": "601398.SS",
    "H股": "1398.HK"
}

try:
    # 获取H股数据（通常更稳定）
    ticker = tickers["H股"]
    stock = yf.Ticker(ticker)
    
    # 获取基本信息
    info = stock.info
    
    print(f"📊 股票代码: {ticker} (工商银行 H股)")
    print(f"📅 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 价格信息
    print("\n💰 价格信息:")
    print(f"   当前价格: {info.get('currentPrice', 'N/A')} HKD")
    print(f"   今日涨跌: {info.get('regularMarketChange', 'N/A')} HKD")
    if info.get('regularMarketChangePercent'):
        print(f"   涨跌幅: {info.get('regularMarketChangePercent', 'N/A')}%")
    print(f"   开盘价: {info.get('regularMarketOpen', 'N/A')} HKD")
    print(f"   最高价: {info.get('dayHigh', 'N/A')} HKD")
    print(f"   最低价: {info.get('dayLow', 'N/A')} HKD")
    print(f"   成交量: {info.get('volume', 'N/A'):,} 股")
    
    # 基本面信息
    print("\n📈 基本面信息:")
    print(f"   市值: {info.get('marketCap', 'N/A'):,} HKD")
    print(f"   市盈率(PE): {info.get('trailingPE', 'N/A')}")
    print(f"   市净率(PB): {info.get('priceToBook', 'N/A')}")
    print(f"   股息率: {info.get('dividendYield', 'N/A')}")
    print(f"   每股收益(EPS): {info.get('trailingEps', 'N/A')} HKD")
    
    # 获取历史数据（1个月）
    print("\n📅 获取历史数据中...")
    hist = stock.history(period="1mo")
    
    if not hist.empty:
        print(f"✅ 获取到 {len(hist)} 个交易日数据")
        print(f"   数据期间: {hist.index[0].strftime('%Y-%m-%d')} 至 {hist.index[-1].strftime('%Y-%m-%d')}")
        
        # 计算统计信息
        start_price = hist['Close'].iloc[0]
        current_price = hist['Close'].iloc[-1]
        price_change = current_price - start_price
        price_change_pct = (price_change / start_price) * 100
        
        print(f"\n📊 1个月表现:")
        print(f"   起始价格: {start_price:.2f} HKD")
        print(f"   当前价格: {current_price:.2f} HKD")
        print(f"   价格变动: {price_change:+.2f} HKD ({price_change_pct:+.2f}%)")
        print(f"   最高价: {hist['High'].max():.2f} HKD")
        print(f"   最低价: {hist['Low'].min():.2f} HKD")
        print(f"   平均成交量: {hist['Volume'].mean():,.0f} 股/日")
        
        # 技术指标计算
        print(f"\n📈 技术指标:")
        
        # 简单移动平均
        sma_5 = hist['Close'].rolling(window=5).mean().iloc[-1]
        sma_10 = hist['Close'].rolling(window=10).mean().iloc[-1]
        print(f"   5日移动平均: {sma_5:.2f} HKD")
        print(f"   10日移动平均: {sma_10:.2f} HKD")
        
        # 相对强弱（简单版本）
        up_days = (hist['Close'] > hist['Close'].shift(1)).sum()
        total_days = len(hist) - 1
        if total_days > 0:
            rs_ratio = up_days / total_days
            print(f"   上涨天数比例: {rs_ratio:.1%} ({up_days}/{total_days}天)")
        
        # 波动率
        daily_returns = hist['Close'].pct_change().dropna()
        volatility = daily_returns.std() * (252 ** 0.5)  # 年化波动率
        print(f"   年化波动率: {volatility:.1%}")
        
        # 生成图表
        print(f"\n📊 正在生成价格图表...")
        
        # 创建图表目录
        chart_dir = os.path.join(os.path.expanduser("~"), ".openclaw", "charts")
        os.makedirs(chart_dir, exist_ok=True)
        
        # 生成蜡烛图
        chart_path = os.path.join(chart_dir, f"icbc_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        
        # 设置图表样式
        mc = mpf.make_marketcolors(
            up='red', down='green',
            edge={'up':'red', 'down':'green'},
            wick={'up':'red', 'down':'green'},
            volume='in'
        )
        
        s = mpf.make_mpf_style(marketcolors=mc, gridstyle='--')
        
        # 创建图表
        fig, axes = mpf.plot(
            hist,
            type='candle',
            style=s,
            title=f'工商银行 (1398.HK) - 1个月价格走势',
            ylabel='价格 (HKD)',
            volume=True,
            ylabel_lower='成交量',
            figratio=(12, 8),
            figscale=1.2,
            returnfig=True
        )
        
        # 保存图表
        fig.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        print(f"✅ 图表已保存: {chart_path}")
        print(f"\n💡 投资建议:")
        print("   1. 工商银行作为中国四大行之一，具有稳定的基本面和分红")
        print("   2. H股通常比A股有折价，提供更好的估值机会")
        print("   3. 关注中国宏观经济政策和利率变化对银行股的影响")
        print("   4. 长期投资者可关注股息收益和估值修复机会")
        
    else:
        print("❌ 无法获取历史数据")
        
except Exception as e:
    print(f"❌ 错误: {e}")
    print("\n💡 可能的原因:")
    print("   1. Yahoo Finance API 限流")
    print("   2. 网络连接问题")
    print("   3. 股票代码不正确或数据不可用")
    
print("\n" + "=" * 50)
print("报告生成完成。数据来源: Yahoo Finance")
print("投资有风险，入市需谨慎。")