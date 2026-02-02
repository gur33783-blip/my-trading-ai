import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- BRANDING & LOGO SECTION ---
st.set_page_config(page_title="GURI TRADER PB13", layout="wide")

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
mode = st.sidebar.radio("Trading Mode Chuno", ["Intraday (Safe)", "Scalping (Fast)"])
ticker = st.sidebar.selectbox("Market Select Karo", ["^NSEI", "^NSEBANK"])

interval = "5m" if "Intraday" in mode else "1m"
period = "5d" if "Intraday" in mode else "1d"

data = yf.download(ticker, period=period, interval=interval, progress=False)

if not data.empty:
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Indicators
    data['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
    data['EMA5'] = data['Close'].ewm(span=5, adjust=False).mean()
    
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    data['RSI'] = 100 - (100 / (1 + (gain/loss)))

    S = float(data['Close'].iloc[-1])
    vwap_val = float(data['VWAP'].iloc[-1])
    ema_val = float(data['EMA5'].iloc[-1])
    rsi_val = float(data['RSI'].iloc[-1])
    atm_strike = round(S / 50) * 50 if "^NSEI" in ticker else round(S / 100) * 100

    # --- HINDI AI SIGNAL ENGINE ---
    st.write("---")
    col1, col2 = st.columns([2, 1])

    with col1:
        if "Intraday" in mode:
            if S > vwap_val and rsi_val > 50:
                st.success(f"🚀 **BUY {atm_strike} CE (CALL)**")
                st.info("Bhai trend Upar hai, kharid sakte ho! Target pe nazar rakho.")
                target, sl = S + (S*0.003), vwap_val
            elif S < vwap_val and rsi_val < 50:
                st.error(f"📉 **BUY {atm_strike} PE (PUT)**")
                st.info("Market Neeche ja raha hai, Put lene ka mauka hai!")
                target, sl = S - (S*0.003), vwap_val
            else:
                st.warning("🟡 **WARNING: RUK JAO BHAI!**")
                st.write("Market abhi Sideways hai. VWAP line ke pass hai, abhi trade lena risky ho sakta hai. Sahi break ka wait karo.")
        else: # Scalping
            if S > ema_val:
                st.success(f"⚡ **SCALP: BUY {atm_strike} CE**")
                st.info("Tezi dikh rahi hai, fatafat entry lo!")
                target, sl = S + 15, S - 12
            else:
                st.error(f"❄️ **SCALP: BUY {atm_strike} PE**")
                st.info("Giraavat hai, fatafat exit plan ke sath entry lo!")
                target, sl = S - 15, S + 12

    with col2:
        st.metric("Live Price", f"₹{S:.2f}")
        if 'target' in locals():
            st.write(f"🎯 **Target:** {target:.2f}")
            st.write(f"🛡️ **Stoploss:** {sl:.2f}")

    # --- CHART ---
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Price'))
    line_val = vwap_val if "Intraday" in mode else ema_val
    line_name = "VWAP" if "Intraday" in mode else "EMA5"
    fig.add_trace(go.Scatter(x=data.index, y=data[line_name], line=dict(color='yellow', width=2), name=line_name))
    fig.update_layout(height=500, template="plotly_dark", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    st.info(f"💡 **Guri ki Tip:** Trade hamesha Stoploss ke sath karein. Capital hai toh kal phir trade milega!")

else:
    st.error("Internet check karo bhai, data nahi aa raha!")
