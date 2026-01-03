import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- SETTINGS & UI ---
st.set_page_config(page_title="Tao Super Terminal", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #00ffcc; }
    .stSuccess { background-color: #064e3b; color: #ecfdf5; }
    .stWarning { background-color: #451a03; color: #fff7ed; }
    .ema-text { font-family: monospace; color: #9ca3af; }
    </style>
    """, unsafe_allow_html=True)

# --- THE LOGIC ENGINE ---
def get_live_data(ticker):
    # Fetching 2y to stabilize the 200 SMA and 89 EMA
    data = yf.download(ticker, period="2y", interval="1d")
    if data.empty or len(data) < 200:
        return None
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    # Calculate Live EMA Stack
    for p in [8, 21, 34, 55, 89]:
        data[f'EMA{p}'] = data['Close'].ewm(span=p, adjust=False).mean()
    
    data['SMA200'] = data['Close'].rolling(window=200).mean()
    
    # ATR Calculation
    h, l, c = data['High'], data['Low'], data['Close']
    tr = np.maximum(h - l, np.maximum(abs(h - c.shift(1)), abs(l - c.shift(1))))
    data['ATR'] = tr.rolling(window=14).mean()
    return data

# --- SIDEBAR: INPUTS ---
st.sidebar.title("🥷 Tao Command")
mode = st.sidebar.radio("Select Mode:", ["CSV Watchlist Analyzer", "Single Ticker Audit"])

target_ticker = ""

if mode == "CSV Watchlist Analyzer":
    uploaded_file = st.sidebar.file_uploader("Upload TradingView Export", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        # Mapping CSV headers to standardized names
        df = df.rename(columns={
            'Average Directional Index (14) 1 day': 'ADX',
            'Stochastic (8,3,3) 1 day, %K': 'Stoch'
        })
        st.subheader("📋 Watchlist Overview")
        df['Setup'] = np.where((df['ADX'] >= 20) & (df['Stoch'] < 40), "🎯 Pullback", "⌛ Wait")
        st.dataframe(df[['Symbol', 'Price', 'ADX', 'Stoch', 'Setup', 'Sector']], use_container_width=True)
        target_ticker = st.selectbox("Select Ticker to Audit:", df['Symbol'].tolist())
else:
    target_ticker = st.sidebar.text_input("Enter Ticker:").upper()

# --- MAIN AUDIT ENGINE ---
if target_ticker:
    with st.spinner(f"Analyzing {target_ticker}..."):
        data = get_live_data(target_ticker)
        
        if data is not None:
            last = data.iloc[-1]
            price = float(last['Close'])
            sma200 = float(last['SMA200'])
            ema21 = float(last['EMA21'])
            atr = float(last['ATR'])
            
            # --- TOP LEVEL METRICS ---
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Current Price", f"${price:.2f}")
            m2.metric("200 SMA (The Wind)", f"${sma200:.2f}")
            m3.metric("ATR (Volatility)", f"${atr:.2f}")
            m4.metric("EMA 21 (Mean)", f"${ema21:.2f}")

            st.divider()

            col_chart, col_audit = st.columns([2, 1])

            with col_chart:
                fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name="Price")])
                colors = ['#00ffcc', '#00ccff', '#3366ff', '#6633ff', '#ff33cc']
                for i, p in enumerate([8, 21, 34, 55, 89]):
                    fig.add_trace(go.Scatter(x=data.index, y=data[f'EMA{p}'], name=f'EMA {p}', line=dict(color=colors[i], width=1.5)))
                fig.add_trace(go.Scatter(x=data.index, y=data['SMA200'], name='200 SMA', line=dict(color='white', width=2, dash='dash')))
                fig.update_layout(template="plotly_dark", height=600, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)

            with col_audit:
                st.subheader("⚙️ Mechanics Check")
                
                # 1. Trend (The Wind)
                if price > sma200:
                    st.success("✅ SAILING WITH THE WIND")
                else:
                    st.error("❌ STAGNANT WATER: Below 200 SMA")

                # 2. THE CRITICAL EMA STACK LIST
                st.markdown("### 📊 EMA Stack Values")
                e8, e21, e34, e55, e89 = (float(last['EMA8']), float(last['EMA21']), 
                                          float(last['EMA34']), float(last['EMA55']), float(last['EMA89']))
                
                # Display individual values with logic checks
                st.markdown(f"**EMA 8:** ${e8:.2f}")
                st.markdown(f"**EMA 21:** ${e21:.2f}")
                st.markdown(f"**EMA 34:** ${e34:.2f}")
                st.markdown(f"**EMA 55:** ${e55:.2f}")
                st.markdown(f"**EMA 89:** ${e89:.2f}")
                
                is_stacked = (e8 > e21 > e34 > e55 > e89)
                if is_stacked:
                    st.success("✅ BULLISH STACK CONFIRMED")
                else:
                    st.warning("⚠️ STACK DISORDERED")

                # 3. Buy Zone Logic
                dist_to_21 = abs(price - e21)
                if dist_to_21 <= atr:
                    st.info("🎯 IN THE BUY ZONE (Within 1 ATR)")
                else:
                    st.warning("⌛ OVEREXTENDED: Wait for Pullback")

                st.divider()
                
                # 4. Automated Trade Plan
                st.subheader("📝 Tactical Execution")
                stop_loss = price - (atr * 1.5)
                tp1 = price + (atr * 1.2)
                tp2 = price + (atr * 2.5)
                
                st.write(f"**Stop Loss:** ${stop_loss:.2f}")
                st.write(f"**Take Profit 1:** ${tp1:.2f}")
                st.write(f"**Take Profit 2:** ${tp2:.2f}")
                
                risk_amt = st.number_input("Portfolio Risk ($):", value=1000)
                shares = int(risk_amt / (price - stop_loss))
                st.metric("Suggested Size", f"{shares} Shares")

        else:
            st.error("Ticker not found or insufficient data (200+ days required).")
