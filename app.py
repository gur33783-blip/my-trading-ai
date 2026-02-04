import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import numpy as np
import time

# --- 1. PREMIUM UI & CSS ---
st.set_page_config(page_title="GURI GHOST V8.1", layout="wide")

st.markdown("""
    <style>
    :root { --groww-green: #00d09c; --groww-red: #eb5b5d; --bg: #030303; }
    .stApp { background-color: var(--bg); color: white; }
    .pulse-dot { height: 12px; width: 12px; border-radius: 50%; display: inline-block; margin-right: 10px; }
    .sector-card { background: #111; padding: 10px; border-radius: 8px; border: 1px solid #222; font-size: 12px; text-align: center; }
    .intl-tag { background: #1a1a1a; padding: 5px 12px; border-radius: 6px; border: 1px solid #333; font-size: 13px; font-weight: 700; }
    .opportunity-card { background: linear-gradient(145deg, #0d0d0d, #1a1a1a); padding: 15px; border-radius: 12px; border: 1px solid #333; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. TURBO DATA ENGINE ---
@st.cache_data(ttl=1)
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
                hist['EMA9'] = hist['Close'].ewm(span=9).mean()
                exp1 = hist['Close'].ewm(span=12).mean(); exp2 = hist['Close'].ewm(span=26).mean()
                hist['MACD'] = exp1 - exp2; hist['Sig'] = hist['MACD'].ewm(span=9).mean()
                res['df'] = hist
            
            fast_info = t.fast_info
            res[name] = {"price": fast_info.last_price, "change": ((fast_info.last_price - fast_info.previous_close)/fast_info.previous_close)*100}
        return res
    except: return None

# --- 3. MAIN TERMINAL ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid #00d09c; margin-bottom:10px;">""", unsafe_allow_html=True)
    st.title("🎯 GURI SNIPER V8.1")
    st.divider()
    if st.button("🔄 RE-SYNC DATA"):
        st.cache_data.clear()
        st.rerun()

tf = st.select_slider("⚡ TIMEFRAME", options=["1m", "5m", "15m"], value="1m")

@st.fragment(run_every=2)
def locked_terminal_v81(idx_name, timeframe):
    data = fetch_safe_data(idx_name, timeframe)
    if not data or 'df' not in data:
        st.warning("🔄 Fetching Live Feed...")
        return

    df = data['df']
    
    # 🌍 INTERNATIONAL HEADER
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
            sc = "#00d09c" if s_data['change'] > 0 else "#eb5b5d"
            st.markdown(f"""<div class="sector-card">{item}<br><b style="color:{sc};">₹{s_data['price']:,.1f}</b></div>""", unsafe_allow_html=True)

    with col_mid:
        # STRATEGY & PULSE
        velocity = df['Close'].diff().tail(3).mean()
        decision = "WAIT"
        if velocity > 0.4 and df['MACD'].iloc[-1] > df['Sig'].iloc[-1]: decision = "CALL"
        elif velocity < -0.4 and df['MACD'].iloc[-1] < df['Sig'].iloc[-1]: decision = "PUT"
        
        dot_c = "#00d09c" if decision == "CALL" else "#eb5b5d" if decision == "PUT" else "#444"
        
        st.markdown(f"""
            <div style="display:flex; align-items:center; margin-bottom:10px;">
                <span class="pulse-dot" style="background:{dot_c}; box-shadow:0 0 10px {dot_c};"></span>
                <span style="font-size:42px; font-weight:800;">₹{data['MAIN']['price']:,.2f}</span>
                <span style="font-size:20px; color:{'#00d09c' if data['MAIN']['change']>0 else '#eb5b5d'}; margin-left:15px;">{data['MAIN']['change']:+.2f}%</span>
            </div>
        """, unsafe_allow_html=True)
        
        # CHART (STABLE)
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.8, 0.2])
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], 
                                    increasing_line_color='#00d09c', decreasing_line_color='#eb5b5d', name='Price'), row=1, col=1)
        
        # Arrows
        buy_pts = df[(df['MACD'] > df['Sig']) & (df['MACD'].shift(1) <= df['Sig'].shift(1))]
        sell_pts = df[(df['MACD'] < df['Sig']) & (df['MACD'].shift(1) >= df['Sig'].shift(1))]
        fig.add_trace(go.Scatter(x=buy_pts.index, y=buy_pts['Low']*0.999, mode='markers', marker=dict(symbol='triangle-up', size=12, color='#00d09c'), name='Buy'), row=1, col=1)
        fig.add_trace(go.Scatter(x=sell_pts.index, y=sell_pts['High']*1.001, mode='markers', marker=dict(symbol='triangle-down', size=12, color='#eb5b5d'), name='Sell'), row=1, col=1)

        # Volume
        v_colors = ['#00d09c' if df['Close'].iloc[i] > df['Open'].iloc[i] else '#eb5b5d' for i in range(len(df))]
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=v_colors, name='Volume'), row=2, col=1)

        fig.update_layout(height=580, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0), 
                          paper_bgcolor='black', plot_bgcolor='black', uirevision='constant', hovermode='x unified')
        fig.update_yaxes(side="right", gridcolor='#111')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col_right:
        st.subheader("🚀 INTEL")
        if decision != "WAIT":
            st.markdown(f"""<div class="opportunity-card" style="border-color:{dot_c}; border-width:2px;"><b>🚀 {decision} BLAST</b><br>Gamma: High<br>Hold: 3-5 Mins</div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="opportunity-card">Market Rangebound</div>""", unsafe_allow_html=True)
        
        st.markdown("### 📊 DATA")
        st.markdown(f"""<div style="background:#111; padding:12px; border-radius:10px; border-left:4px solid #f0b90b;">OI Trend: <b>{'Bullish' if data['MAIN']['change'] > 0 else 'Bearish'}</b><br>Gamma Spike: <b>{'ACTIVE' if abs(velocity) > 0.6 else 'Wait'}</b></div>""", unsafe_allow_html=True)

# Select Market
target_m = st.selectbox("MARKET", ["NIFTY", "BANKNIFTY"], label_visibility="collapsed")
locked_terminal_v81(target_m, tf)
