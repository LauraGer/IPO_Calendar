import pandas as pd
import numpy as np

def get_monthly_returns(stock_data):
    # 1. Monthly Returns
    # Calculate the monthly returns based on the closing prices.
    # This helps assess the percentage change in the stock's value over each month.
    stock_data['monthly_returns'] = stock_data['close'].pct_change()

    return stock_data

def get_average_true_range(stock_data):
    # 2. Average True Range (ATR)
    # Measures the average range between high and low prices,
    # providing an indication of volatility.
    stock_data['ATR'] = stock_data[['high', 'low', 'close']].apply(lambda x: max(x) - min(x), axis=1).rolling(window=14).mean()

    return stock_data

def get_moving_average(stock_data):
    # 3. Moving Averages
    # Indicates the variability of monthly returns.
    # Assess the trend direction by comparing short-term and long-term moving averages.
    stock_data['50-day MA'] = stock_data['close'].rolling(window=50).mean()
    stock_data['200-day MA'] = stock_data['close'].rolling(window=200).mean()

    return stock_data

def get_price_to_earnings_ratio(stock_data, earnings_data):
    # 4. Price-to-Earnings Ratio (P/E Ratio)
    # Assuming you have earnings data in a separate DataFrame named 'earnings_data' with columns 'Date', 'Earnings'
    # Evaluate the stock's valuation relative to its earnings.
    merged_data = pd.merge(stock_data, earnings_data, on='Date')
    merged_data['P/E Ratio'] = merged_data['close'] / merged_data['Earnings']

    return merged_data

def get_price_to_sales_ratio(stock_data, revenue_data):
    # 5. Price-to-Sales Ratio (P/S Ratio)
    # Assuming you have revenue data in a separate DataFrame named 'revenue_data' with columns 'Date', 'Revenue'
    # Assess the stock's valuation relative to its revenue.
    merged_data = pd.merge(stock_data, revenue_data, on='Date')
    merged_data['P/S Ratio'] = merged_data['close'] / merged_data['Revenue']

    return merged_data

def get_average_monthly_trading_volume(stock_data):
    # 6. Average Monthly Trading Volume
    # Evaluate the liquidity of the stock by assessing the average monthly trading volume.
    stock_data['Average Monthly Volume'] = stock_data['Volume'].rolling(window=20).mean()

    return stock_data

def get_sharpe_ratio(stock_data):
    # 7. Sharpe Ratio
    # Measure the risk-adjusted performance by considering the ratio of excess returns to volatility.
    risk_free_rate = 0.02  # Example risk-free rate
    stock_data['Excess Returns'] = stock_data['Monthly Returns'] - risk_free_rate / 12
    sharpe_ratio = np.sqrt(12) * stock_data['Excess Returns'].mean() / stock_data['Excess Returns'].std()

    return sharpe_ratio

def get_maximum_drawdown(stock_data):
    # 8. Maximum Drawdown
    # Identify the maximum peak-to-trough decline over the monthly period, providing insights into historical risk.
    cumulative_returns = (1 + stock_data['Monthly Returns']).cumprod()
    cumulative_max = cumulative_returns.cummax()
    drawdown = (cumulative_max - cumulative_returns) / cumulative_max
    max_drawdown = drawdown.max()

    return max_drawdown

def get_relation_strength_index(stock_data):
    # 9. Relative Strength Index (RSI)
    # Assess overbought or oversold conditions using the Relative Strength Index.
    period = 14  # adjustable RSI period
    delta = stock_data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    average_gain = gain.rolling(window=period).mean()
    average_loss = loss.rolling(window=period).mean()
    rs = average_gain / average_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi
