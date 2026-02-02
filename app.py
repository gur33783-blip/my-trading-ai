import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- BRANDING & LOGO SECTION ---
st.set_page_config(page_title="GURI TRADER PB13", layout="wide")

# Tumhari Photo ka link yahan set kar diya hai
my_photo_url = "https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" 

st.markdown(f"""
    <div style='display: flex; align-items: center; background-color: #1e1e1e; padding: 15px; border-radius: 20px; border: 3px solid #FFD700; margin-bottom: 20px;'>
        <img src='{my_photo_url}' style='width: 100px; height: 100px; border-radius: 50%; border: 2px solid #FFD700; object-fit: cover; margin-right: 25px;'>
        <div>
            <h1 style='color: #FFD700; margin: 0; font-family: sans-serif;'>GURI TRADER PB13</h1>
            <p style='color: #00FFCC; margin: 0; font-weight: bold;'>⚡ Professional Hybrid AI System</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
st.sidebar.markdown("### 🛠️ STRATEGY SETTINGS")
mode = st.sidebar.radio("Select Trading Mode", ["Intraday (Safe)", "Scalping (Fast)"])
ticker = st.sidebar.selectbox("Select Asset", ["^NSEI", "^NSEBANK"])

# Dynamic Timeframe Logic
interval = "5m" if "Intraday" in mode else "1m"
period = "5d" if "Intraday" in mode else "1d"

data = yf.download(ticker, period=period, interval=interval, progress=False)

if not data.empty:
    # Column fix for new yfinance update
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # --- INDICATORS CALCULATION ---
    # VWAP for Intraday
    data['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
    # EMA 5 for Scalping
    data['EMA5'] = data['Close'].ewm(span=5, adjust=False).mean()
    # RSI for Momentum
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    data['RSI'] = 100 - (100 / (1 + (gain/loss)))

    S = float(data['Close'].iloc[-1])
    vwap_val = float(data['VWAP'].iloc[-1])
    ema_val = float(data['EMA5'].iloc[-1])
    rsi_val = float(data['RSI'].iloc[-1])

    # --- AI SIGNAL ENGINE ---
    st.write("---")
    col1, col2 = st.columns([2, 1])

    with col1:
        if "Intraday" in mode:
            if S > vwap_val and rsi_val > 50:
                st.success(f"🚀 **BULLISH TREND:** Price is above VWAP. Good for Long!")
                target, sl = S + (S*0.003), vwap_val
            elif S < vwap_val and rsi_val < 50:
                st.error(f"📉 **BEARISH TREND:** Price is below VWAP. Good for Short!")
                target, sl = S - (S*0.003), vwap_val
            else:
                st.warning("🟡 **NEUTRAL:** Waiting for a clear break near VWAP.")
        else: # Scalping Mode
            if S > ema_val:
                st.success(f"⚡ **SCALP BUY:** Momentum is High! Quick Points Possible.")
                target, sl = S + 15, S - 12
            else:
                st.error(f"❄️ **SCALP SELL:** Momentum is Low! Quick Fall Possible.")
                target, sl = S - 15, S + 12

    with col2:
        st.metric("Live Price", f"₹{S:.2f}")
        if 'target' in locals():
            st.write(f"🎯 **TGT:** {target:.2f}")
            st.write(f"🛡️ **SL:** {sl:.2f}")

    # --- PRO CHARTING ---
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Market'))
    
    # Adaptive Line based on Mode
    if "Intraday" in mode:
        fig.add_trace(go.Scatter(x=data.index, y=data['VWAP'], line=dict(color='cyan', width=2), name='VWAP'))
    else:
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA5'], line=dict(color='orange', width=2), name='Fast EMA'))

    fig.update_layout(height=550, template="plotly_dark", xaxis_rangeslider_visible=False, title=f"{ticker} Live Analysis ({mode})")
    st.plotly_chart(fig, use_container_width=True)

    # Option Strike Helper
    atm = round(S / 50) * 50 if "^NSEI" in ticker else round(S / 100) * 100
    st.info(f"💡 **Guri's Strategy:** For best results, trade in ATM strike **{atm}**.")

else:
    st.error("Market data fetch nahi ho raha. Refresh karein.")
