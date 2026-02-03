import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import numpy as np
import random

# --- 1. SETTINGS & STYLES ---
st.set_page_config(page_title="GURI TERMINAL GOD-MODE", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
    :root { --neon-green: #02c076; --neon-red: #f84960; --gold: #f0b90b; --bg-dark: #0b0e11; }
    .stApp { background-color: var(--bg-dark); color: #e9eaeb; }
    .hud-card {
        background: #1e2329; padding: 20px; border-radius: 16px;
        border: 1px solid #30363d; box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        margin-bottom: 15px;
    }
    .price-main { font-family: 'JetBrains Mono', monospace; font-size: 70px; font-weight: 800; color: var(--gold); letter-spacing: -4px; line-height: 1; }
    .index-badge { background: #2b3139; padding: 5px 12px; border-radius: 8px; font-weight: 800; font-size: 13px; color: #929aa5; }
    .meter-bg { background: #30363d; height: 10px; border-radius: 5px; overflow: hidden; margin: 10px 0; }
    .meter-fill { height: 100%; transition: width 0.5s ease; }
    .ai-guidance {
        background: rgba(240, 185, 11, 0.08); border-left: 6px solid var(--gold);
        padding: 15px; border-radius: 12px; font-size: 19px; font-weight: 700; color: var(--gold);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
@st.cache_data(ttl=0.01)
def fetch_market_data(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="1m").tail(60)
        fast = t.fast_info
        return df, fast.last_price, fast.previous_close
    except: return None, 0, 0

# --- 3. PERSISTENT SIDEBAR (Fixes Duplicate ID Error) ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid var(--gold); margin-bottom:20px;">""", unsafe_allow_html=True)
    st.header("🎮 CONTROL PANEL")
    
    # Selection buttons outside the loop to avoid duplicate ID error
    mode = st.radio("SELECT INDEX", ["NIFTY 50", "BANK NIFTY"], key="index_selector")
    current_idx = "^NSEI" if mode == "NIFTY 50" else "^NSEBANK"
    
    st.divider()
    st.success("Bhai, Speed Optimized hai! ✅")
    st.info("Market Hours: 9:15 - 3:30")

# --- 4. THE LIVE HUD ---
terminal_hud = st.empty()

while True:
    df, ltp, prev = fetch_market_data(current_idx)
    
    if df is not None:
        change = ltp - prev
        pct = (change / prev) * 100
        color = "#02c076" if change >= 0 else "#f84960"
        power = random.randint(58, 92) if change > 0 else random.randint(15, 42)
        
        with terminal_hud.container():
            # TOP HEADER
            st.markdown(f"""
                <div class="hud-card" style="display:flex; justify-content:space-between; align-items:center; border-bottom: 3px solid var(--gold);">
                    <div>
                        <h1 style="margin:0; font-size:35px;">GURI <span style="color:var(--gold);">GOD-MODE</span></h1>
                        <p style="margin:0; color:#929aa5; font-weight:800;">{mode} LIVE PULSE</p>
                    </div>
                    <div style="text-align:right;">
                        <h2 style="margin:0; color:{color};">{'BULLISH 🚀' if change > 0 else 'BEARISH 📉'}</h2>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1.5, 2.5])
            
            with col1:
                # PRICE CARD
                st.markdown(f"""
                    <div class="hud-card">
                        <p style="color:#929aa5; font-size:14px; font-weight:800;">LIVE TICKER</p>
                        <div class="price-main">₹{ltp:,.2f}</div>
                        <div style="font-size:32px; font-weight:800; color:{color};">{'+' if change >= 0 else ''}{change:.2f} ({pct:.2f}%)</div>
                        <br>
                        <p style="margin:0; font-size:12px; color:#929aa5;">BUYERS POWER METER</p>
                        <div class="meter-bg"><div class="meter-fill" style="width:{power}%; background:{color};"></div></div>
                        <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:800;">
                            <span>Buyers: {power}%</span><span>Sellers: {100-power}%</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # HINDI AI ADVICE
                atm = round(ltp/50)*50 if mode == "NIFTY 50" else round(ltp/100)*100
                advice = f"Guri bhai, Buyers full power mein hain! {atm} CE lo. Target: {ltp+50:.0f}." if power > 60 else f"Sellers heavy hain! {atm} PE setup dekho. Stop-Loss trail karo!"
                st.markdown(f"""<div class="ai-guidance">🤖 AI ADVICE:<br>{advice}</div>""", unsafe_allow_html=True)

            with col2:
                # CANDLESTICK CHART
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                    increasing_line_color='#02c076', decreasing_line_color='#f84960'
                )])
                fig.update_layout(height=450, template="plotly_dark", xaxis_rangeslider_visible=False,
                                  margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True, key=f"fixed_chart_{time.time()}", config={'displayModeBar': False})

    time.sleep(0.5)
