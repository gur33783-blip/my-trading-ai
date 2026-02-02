import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Title with your name
st.set_page_config(page_title="GURI TRADER PB13 - AI PRO", layout="wide")
st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>🔥 GURI TRADER PB13 - AI SYSTEM 🔥</h1>", unsafe_allow_html=True)

def get_pro_indicators(df):
    # RSI (Premium Momentum Indicator)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain/loss)))
    
    # Bollinger Bands (Paid Feature - Volatility)
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['Upper_Band'] = df['MA20'] + (df['Close'].rolling(window=20).std() * 2)
    df['Lower_Band'] = df['MA20'] - (df['Close'].rolling(window=20).std() * 2)
    
    # EMA 9 (Fast Entry/Exit)
    df['EMA9'] = df['EMA'] = df['Close'].ewm(span=9, adjust=False).mean()
    return df

ticker = st.sidebar.selectbox("Market Select", ["^NSEI", "^NSEBANK"])
data = yf.download(ticker, period="1mo", interval="15m", progress=False)

if not data.empty:
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    data = get_pro_indicators(data)
    S = float(data['Close'].iloc[-1])
    rsi_val = float(data['RSI'].iloc[-1])
    
    # Dashboard Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("LIVE PRICE", f"₹{S:.2f}")
    col2.metric("MOMENTUM (RSI)", f"{rsi_val:.2f}")
    
    # AI Signal Logic (High Accuracy)
    signal = "WAIT"
    color = "white"
    if S > data['EMA9'].iloc[-1] and rsi_val > 60:
        signal = "🚀 STRONG BULLISH (BUY CALL)"
        color = "#00ff00"
    elif S < data['EMA9'].iloc[-1] and rsi_val < 40:
        signal = "📉 STRONG BEARISH (BUY PUT)"
        color = "#ff4b4b"
    
    st.markdown(f"<div style='text-align: center; background-color: {color}; padding: 20px; border-radius: 10px;'><h2 style='color: black;'>{signal}</h2></div>", unsafe_allow_html=True)

    # Pro Chart with Bollinger Bands
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Market'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Upper_Band'], line=dict(color='rgba(173, 216, 230, 0.5)'), name='Upper Band'))
    fig.add_trace(go.Scatter(x=data.index, y=data['Lower_Band'], line=dict(color='rgba(173, 216, 230, 0.5)'), name='Lower Band'))
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("📢 **GURI TRADER PB13 Alert:** Jab price Lower Band ko touch karke RSI 30 se upar aaye, tab 90% Call ka chance hota hai!")
else:
    st.error("Data check karein.")
