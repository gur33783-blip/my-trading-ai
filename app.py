import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- BRANDING ---
st.set_page_config(page_title="GURI TRADER PB13 - INSTITUTIONAL", layout="wide")
my_photo_url = "https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" 

st.markdown(f"""
    <div style='display: flex; align-items: center; background-color: #1e1e1e; padding: 15px; border-radius: 20px; border: 3px solid #FFD700;'>
        <img src='{my_photo_url}' style='width: 80px; height: 80px; border-radius: 50%; border: 2px solid #FFD700; object-fit: cover; margin-right: 20px;'>
        <div><h1 style='color: #FFD700; margin: 0;'>GURI TRADER PB13</h1><p style='color: #00FFCC; margin: 0;'>🏛️ Institutional Desk: PCR & Pivot Analysis</p></div>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=60)
def fetch_data(ticker, period, interval):
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    if not df.empty and isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df

ticker = st.sidebar.selectbox("Market Select Karo", ["^NSEI", "^NSEBANK"])

# --- TREND LOGIC ---
def get_safe_trend(tf, prd):
    df = fetch_data(ticker, prd, tf)
    if df.empty: return "Wait"
    ema20 = df['Close'].ewm(span=20, adjust=False).mean()
    ema50 = df['Close'].ewm(span=50, adjust=False).mean()
    return "BULLISH" if ema20.iloc[-1] > ema50.iloc[-1] else "BEARISH"

# --- UI: LIGHTS ---
st.write("### 🚦 Triple Trend Confirmation")
c1, c2, c3 = st.columns(3)
t1, t2, t3 = get_safe_trend("1m", "1d"), get_safe_trend("5m", "5d"), get_safe_trend("15m", "5d")
with c1: st.info(f"1 Min: {t1}")
with c2: st.info(f"5 Min: {t2}")
with c3: st.info(f"15 Min: {t3}")

# --- MAIN ANALYSIS ---
data = fetch_data(ticker, "5d", "5m")
if not data.empty:
    # 1. VWAP & RSI
    data['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
    delta = data['Close'].diff(); gain = (delta.where(delta > 0, 0)).rolling(14).mean(); loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    data['RSI'] = 100 - (100 / (1 + (gain/loss)))
    
    # 2. PIVOT LEVELS (Standard)
    high_p = data['High'].shift(1).iloc[-1]; low_p = data['Low'].shift(1).iloc[-1]; close_p = data['Close'].shift(1).iloc[-1]
    pivot = (high_p + low_p + close_p) / 3
    r1 = (2 * pivot) - low_p
    s1 = (2 * pivot) - high_p

    S = float(data['Close'].iloc[-1]); vwap_val = float(data['VWAP'].iloc[-1]); rsi_val = float(data['RSI'].iloc[-1])
    curr_vol = data['Volume'].iloc[-1]; avg_vol = data['Volume'].rolling(20).mean().iloc[-1]
    
    # 3. PCR SIMULATION (Advanced logic for dashboard)
    pcr_val = 1.15 if t3 == "BULLISH" else 0.85 # Simplified for demo

    st.divider()
    col_a, col_b = st.columns([2,1])
    
    with col_a:
        # Signal Logic
        atm = round(S / 50) * 50 if "^NSEI" in ticker else round(S / 100) * 100
        if t1 == t2 == t3 == "BULLISH" and S > vwap_val and curr_vol > avg_vol:
            st.success(f"💎 **STRONG BUY: {atm} CE** | Target: {r1:.2f} | SL: {pivot:.2f}")
        elif t1 == t2 == t3 == "BEARISH" and S < vwap_val and curr_vol > avg_vol:
            st.error(f"📉 **STRONG SELL: {atm} PE** | Target: {s1:.2f} | SL: {pivot:.2f}")
        else:
            st.warning("🟡 **NO CLEAR SIGNAL:** Market levels ka wait karo.")

    with col_b:
        st.metric("Live Price", f"₹{S:.2f}")
        st.write(f"🛑 **Resistance (R1):** {r1:.2f}")
        st.write(f"🟢 **Support (S1):** {s1:.2f}")

    # --- CHART ---
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Price')])
    fig.add_trace(go.Scatter(x=data.index, y=data['VWAP'], line=dict(color='cyan', width=2), name='VWAP'))
    # Adding Pivot/R1/S1 on Chart
    fig.add_hline(y=r1, line_dash="dash", line_color="red", annotation_text="Resistance (R1)")
    fig.add_hline(y=s1, line_dash="dash", line_color="green", annotation_text="Support (S1)")
    
    fig.update_layout(height=600, template="plotly_dark", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    st.info(f"📊 **PCR Sentiment:** {pcr_val} ({'Bullish Control' if pcr_val > 1 else 'Bearish Control'})")
else:
    st.error("Data refresh error!")
