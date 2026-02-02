import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="AI Trading Pro", layout="wide")

st.title("🚀 AI Market Predictor: Nifty & Bank Nifty")
st.write("Live Bullish/Bearish Analysis with Entry & Exit Signals")

def get_data(ticker):
    df = yf.download(ticker, period='5d', interval='15m', progress=False)
    # RSI Calculation
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain/loss)))
    # Moving Average
    df['MA20'] = df['Close'].rolling(window=20).mean()
    return df

stocks = {"Nifty 50": "^NSEI", "Bank Nifty": "^NSEBANK", "Fin Nifty": "NIFTY_FIN_SERVICE.NS"}
selected_stock = st.sidebar.selectbox("Select Index", list(stocks.keys()))

data = get_data(stocks[selected_stock])
curr_price = data['Close'].iloc[-1]
rsi_val = data['RSI'].iloc[-1]
ma_val = data['MA20'].iloc[-1]

# AI Logic for Signals
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Live Price", f"₹{curr_price:.2f}")
with col2:
    st.metric("RSI (Momentum)", f"{rsi_val:.2f}")

with col3:
    if curr_price > ma_val and rsi_val > 60:
        st.error("🚀 SIGNAL: STRONG BUY / CALL")
    elif curr_price < ma_val and rsi_val < 40:
        st.error("📉 SIGNAL: STRONG SELL / PUT")
    else:
        st.warning("⚪ SIGNAL: WAIT / NEUTRAL")

# Professional Chart
fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
st.plotly_chart(fig, use_container_width=True)

st.write("⚠️ **Disclaimer:** Ye sirf educational purpose ke liye hai. Trade lene se pehle stop-loss zaroor lagayein.")
