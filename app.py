import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import numpy as np

# --- SETTINGS & FAST THEME ---
st.set_page_config(page_title="Guri Hyper Terminal", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700;800&display=swap');
    
    /* Background & Clean UI */
    .stApp { background-color: #f4f6f9; }
    
    /* Zero Flicker Header */
    .main-header {
        display: flex; align-items: center; justify-content: space-between;
        background: white; padding: 15px 30px; border-radius: 12px;
        box-shadow: 0 2px 15px rgba(0,0,0,0.05); margin-bottom: 10px;
    }
    .profile-section { display: flex; align-items: center; gap: 15px; }
    .profile-img { width: 55px; height: 55px; border-radius: 50%; border: 3px solid #00d09c; }
    
    /* Big Bold Data Display */
    .price-card { background: white; padding: 25px; border-radius: 15px; border-left: 8px solid #00d09c; }
    .tick-price { font-family: 'JetBrains Mono', monospace; font-size: 65px; font-weight: 800; color: #1a202c; letter-spacing: -2px; }
    .tick-change { font-size: 28px; font-weight: 700; }
    
    /* Signal Tags */
    .signal-tag { padding: 8px 20px; border-radius: 50px; font-weight: 800; font-size: 20px; text-transform: uppercase; }
    .buy-ce { background: #00d09c; color: white; box-shadow: 0 4px 15px rgba(0, 208, 156, 0.3); }
    .buy-pe { background: #eb5b3c; color: white; box-shadow: 0 4px 15px rgba(235, 91, 60, 0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- THE "NO-FLICKER" PLACEHOLDER ---
main_placeholder = st.empty()

# --- HYPER-DATA FETCH ---
def get_delta_data(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="1m").tail(35)
        if not df.empty:
            info = t.fast_info
            return df, info.last_price, info.previous_close
    except: return None, 0, 0

# --- CONTINUOUS LIVE LOOP (Millisecond Speed) ---
market_sym = "^NSEI" # Nifty Default

while True:
    df, ltp, prev = get_delta_data(market_sym)
    
    if df is not None:
        change = ltp - prev
        pct = (change / prev) * 100
        color = "#00d09c" if change >= 0 else "#eb5b3c"
        sig_class = "buy-ce" if change >= 0 else "buy-pe"
        sig_text = "CALL ENTRY" if change >= 0 else "PUT ENTRY"

        # Update only the content inside the placeholder (No Page Refresh)
        with main_placeholder.container():
            # 1. MERGED HEADER
            st.markdown(f"""
                <div class="main-header">
                    <div class="profile-section">
                        <img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" class="profile-img">
                        <div>
                            <h2 style="margin:0;">GURI <span style="color:#00d09c;">TERMINAL</span></h2>
                            <span class="signal-tag {sig_class}">{sig_text}</span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin:0; color:#888;">NIFTY 50 LIVE</p>
                        <p style="margin:0; font-weight:800; color:{color};">Accurate Pulse: 0.001s</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 2. MAIN DATA & CHART
            col1, col2 = st.columns([1.5, 2])
            
            with col1:
                st.markdown(f"""
                    <div class="price-card" style="border-color:{color};">
                        <div class="tick-price">₹{ltp:,.2f}</div>
                        <div class="tick-change" style="color:{color};">
                            {'+' if change >= 0 else ''}{change:.2f} ({pct:.2f}%)
                        </div>
                        <hr>
                        <p style="font-size:18px;"><b>🎯 Target:</b> {ltp+(ltp*0.002):.2f}</p>
                        <p style="font-size:18px;"><b>🛡️ StopLoss:</b> {ltp-(ltp*0.001):.2f}</p>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                # Optimized Small Chart
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                    increasing_line_color='#00d09c', decreasing_line_color='#eb5b3c'
                )])
                fig.update_layout(height=320, template="plotly_white",
