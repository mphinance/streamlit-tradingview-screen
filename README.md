## 🥷 Tao Terminal: Systematic Trend-Following Dashboard

Tao Terminal is a high-performance Streamlit application built for systematic traders who follow trend-following principles and rigorous risk management. It automates the "Tao of Trading" logic to identify high-quality setups by verifying trend alignment, momentum strength, and mean-reversion pullbacks.

### 🚀 Key Features*

- Sailing with the Wind: Automatic verification of price action relative to the 200-day SMA to ensure you are trading with the long-term trend.
- The EMA Stack: Real-time audit of the 8, 21, 34, 55, and 89 Exponential Moving Averages to confirm bullish or bearish momentum.
- Precision Pullback Detection: Integration of Slow Stochastics (8,3) and ADX (14) to find low-risk "Buy the Dip" entries in strong trends.
- Dynamic Trade Planning: Automatically generates Entry Zones, Stop Losses (1.5x ATR), and multiple Take Profit targets based on current volatility.
- Watchlist Analyzer: Support for TradingView CSV exports to rank and filter multiple tickers simultaneously.
- Portfolio Risk Sizer: Integrated calculator to determine exact share counts based on a predefined dollar risk per trade.

### 🛠️ Installation

*Prerequisites*

- Python 3.8 or higher.
- A stable internet connection for Yahoo Finance data.

*Local Setup*

Clone the Repository:
```git clone https://github.com/mphinance/streamlit-tradingview-screen```
```cd streamlit-tradingview-screen```

Install Dependencies:
```pip install -r requirements.txt```

Run the Application:
```streamlit run tao_terminal.py```

### 📖 Usage Guide

*Mode 1: CSV Watchlist Analyzer*

- Export your "Stacked EMAs" watchlist from TradingView as a CSV file.
- Upload the file via the sidebar.
- The terminal will flag "🎯 Pullback" setups where ADX is >= 20 and Stochastics are < 40.
- Select a ticker to generate a full visual audit and trade plan.

*Mode 2: Single Ticker Audit*

- Enter any ticker symbol (e.g., GOOGL) in the sidebar.
- Review the Mechanics Check to ensure all EMA and Trend criteria are met.
- Adjust your Portfolio Risk to see the suggested position sizing.

### ⚠️ Disclaimer

*For Educational Purposes Only. Tao Terminal is a technical analysis tool and does not constitute financial advice. Trading involves significant risk.*
