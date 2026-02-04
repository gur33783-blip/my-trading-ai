import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import numpy as np
import time

# --- 1. PREMIUM UI & ANIMATIONS ---
st.set_page_config(page_title="GURI GHOST V8.0", layout="wide")

st.markdown("""
    <style>
    :root { --groww-green: #00d09c; --groww-red: #eb5b5d; --bg: #030303; }
    .stApp { background-color: var(--bg); color: white; }
    .pulse-dot { height: 12px; width: 12px; border-radius: 50%; display: inline-block; margin-right: 10px; }
    .sector-card { background: #111; padding: 10px; border-radius: 8px; border: 1px solid #222; font-size: 12px; text-align: center; }
    .intl-tag { background: #1a1a1a; padding: 5px 12px; border-radius: 6px; border: 1px solid #333; font-size: 13px; font-weight: 700; }
    .opportunity-card { background: linear-gradient(145deg, #0d0d0d, #1a1a1a); padding: 15px; border-radius: 12px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ROBUST DATA ENGINE (ANTI-CRASH) ---
@st.cache_data(ttl=1) # Reduced frequency slightly to stop Websocket errors
def fetch_safe_data(idx, interval):
    targets = {
        "MAIN": "^NSEI" if idx == "NIFTY" else "^NSEBANK",
        "NASDAQ": "^IXIC", "VIX": "^INDIAVIX",
        "RELIANCE": "RELIANCE.NS", "HDFCBANK": "HDFCBANK.NS", "IT": "^CNXIT", "AUTO": "^CNXAUTO"
    }
    res = {}
    try:
        for name, sym in targets.items():
            t = yf.Ticker(sym)
            if name == "MAIN":
                hist = t.history(period="1d", interval=interval).tail(100)
                if hist.empty: continue
                # Strategy Logic
                hist['EMA9'] = hist['Close'].ewm(span=9).mean()
                exp1 = hist['Close'].ewm(span=12).mean(); exp2 = hist['Close'].ewm(span=26).mean()
                hist['MACD'] = exp1 - exp2; hist['Sig'] = hist['MACD'].ewm(span=9).mean()
                res['df'] = hist
            
            # Use safe fetching for info
            fast_info = t.fast_info
            res[name] = {"price": fast_info.last_price, "change": ((fast_info.last_price - fast_info.previous_close)/fast_info.previous_close)*100}
        return res
    except Exception as e:
        # If Websocket or fetch fails, return None to avoid app crash
        return None

# --- 3. SIDEBAR (LOCKED) ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid #00d09c; margin-bottom:10px;">""", unsafe_allow_html=True)
    st.title("🎯 GURI SNIPER V8.0")
    if st.button("RE-SYNC DATA (Fix Lag)"):
        st.cache_data.clear()
        st.rerun()

# --- 4. MAIN TERMINAL ---
tf = st.select_slider("⚡ TIMEFRAME", options=["1m", "5m", "15m"], value="1m")

@st.fragment(run_every=2) # 2 seconds refresh to keep Websocket connection stable
def stable_terminal_v8(idx_name, timeframe):
    data = fetch_safe_data(idx_name, timeframe)
    
    if data is None or 'df' not in data:
        st.warning("⚠️ Connection Weak... Re-syncing in 2 seconds.")
        time.sleep(1)
        return

    df = data['df']
    
    # 🌍 INTERNATIONAL HEADER (LOCKED)
    st.markdown(f"""
        <div style="display:flex; gap:10px; margin-bottom:15px; overflow-x: auto;">
            <div class="intl-tag">🇺🇸 NASDAQ: <span style="color:{'#00d09c' if data['NASDAQ']['change']>0 else '#eb5b5d'}">{data['NASDAQ']['change']:+.2f}%</span></div>
            <div class="intl-tag">📉 VIX: {data['VIX']['price']:.2f}</div>
            <div class="intl-tag">🏢 IT: {data['IT']['change']:+.2f}%</div>
            <div class="intl-tag">🚗 AUTO: {data['AUTO']['change']:+.2f}%</div>
        </div>
    """, unsafe_allow_html=True)

    col_left, col_mid, col_right = st.columns([0.8, 3, 1.2])

    with col_left:
        st.markdown("### 🏛️ SECTORS")
        for item in ["RELIANCE", "HDFCBANK"]:
            s_data = data[item]
            c = "#00d09c" if s_data['change'] > 0 else "#eb5b5d"
            st.markdown(f"""<div class="sector-card">{item}<br><b style="color:{c}; font-size:14px;">₹{s_data['price']:,.1f}</b></div>""", unsafe_allow_html=True)

    with col_mid:
        # STRATEGY LOGIC
        decision = "WAIT"
        velocity = df['Close'].diff().tail(3).mean()
        if velocity > 0.4 and df['MACD'].iloc[-1] > df['Sig'].iloc[-1]: decision = "CALL"
        elif velocity < -0.4 and df['MACD'].iloc[-1] < df['Sig'].iloc[-1]: decision = "PUT"
        
        dot_color = "#00d09c" if decision == "CALL" else "#eb5b5d" if decision == "PUT" else "#444"
        
        st.markdown(f"""
            <div style="display:flex; align-items:center; margin-bottom:1
