import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="GURI TRADER PB13 - Scalping Special", layout="wide")
st.markdown("<h1 style='text-align: center; color: #00FFCC;'>💎 GURI TRADER PB13: SCALPER AI 💎</h1>", unsafe_allow_html=True)

ticker = st.sidebar.selectbox("Market Select", ["^NSEI", "^NSEBANK"])
data = yf.download(ticker, period="1d", interval="1m", progress=False) # 1 min interval for scalping

if not data.empty:
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    S = float(data['Close'].iloc[-1])
    prev_s = float(data['Close'].iloc[-2])
    change = S - prev_s

    # --- SCALPING METER ---
    st.subheader(f"📊 Live Spot: ₹{S:.2f} ({'+' if change>0 else ''}{change:.2f})")
    
    # Strike Calculation
    atm = round(S / 50) * 50 if "^NSEI" in ticker else round(S / 100) * 100
    
    # Option Chain Table Design
    st.markdown("### ⚡ Option Chain Scalper Help")
    chain_data = {
        "Type": ["Deep ITM", "ITM", "ATM", "OTM"],
        "Call Strike": [atm-100, atm-50, atm, atm+50],
        "Put Strike": [atm+100, atm+50, atm, atm-50],
        "Delta (Speed)": ["0.80 (Fast)", "0.65 (Medium)", "0.50 (Normal)", "0.30 (Slow)"]
    }
    st.table(pd.DataFrame(chain_data))

    # --- SCALPING LOGIC ---
    # Fast EMA for Scalping
    data['EMA5'] = data['Close'].ewm(span=5, adjust=False).mean()
    curr_ema = data['EMA5'].iloc[-1]

    if S > curr_ema and change > 0:
        st.success(f"🚀 **SCALP ENTRY (CALL):** Price is hiking! Target ATM {atm} CE for quick points.")
        st.toast("ENTRY ALERT: HIKE DETECTED!", icon='🔥')
    elif S < curr_ema and change < 0:
        st.error(f"📉 **SCALP ENTRY (PUT):** Market dropping! Target ATM {atm} PE for quick points.")
        st.toast("ENTRY ALERT: DROP DETECTED!", icon='❄️')
    else:
        st.info("⌛ Waiting for Momentum... No Scalp Zone.")

    # Chart
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
    fig.update_layout(height=400, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.write("⚠️ **Guri's Scalping Tip:** Scalping mein 5-10 point lekar bahar nikal jao. Zyada lalach account saaf kar deta hai!")
else:
    st.error("Market data load nahi ho raha.")
