import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import random

# --- HYPER-THEME CONFIG ---
st.set_page_config(page_title="GURI HYPER TERMINAL", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Premium Groww-Style Dark Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Roboto Mono', monospace; background-color: #090a0f; color: #e1e1e1; }
    .stApp { background-color: #090a0f; }
    
    /* Price Card - Groww Style */
    .price-container {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 15px; padding: 20px; margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }
    
    /* Signal Buttons */
    .sig-flex { display: flex; gap: 15px; margin: 15px 0; }
    .btn-call { background: #00d09c; color: #000; padding: 12px 24px; border-radius: 8px; font-weight: 900; box-shadow: 0 0 15px #00d09c; }
    .btn-put { background: #eb5b3c; color: #fff; padding: 12px 24px; border-radius: 8px; font-weight: 900; box-shadow: 0 0 15px #eb5b3c; }
    
    /* AI Chat Glass */
    .ai-chat { background: rgba(30, 31, 38, 0.8); border-radius: 12px; padding: 15px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- HYPER-SPEED DATA ENGINE ---
def get_hyper_data(symbol):
    # Using 'fast_info' to bypass heavy data loads for LTP
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="1d", interval="1m", prepost=True).tail(60) # Only last 60 mins for speed
    if not df.empty:
        ltp = df['Close'].iloc[-1]
        prev_close = ticker.info.get('previousClose', df['Open'].iloc[0])
        change = ltp - prev_close
        pct = (change / prev_close) * 100
        return df, ltp, change, pct
    return None, 0, 0, 0

# --- SIDEBAR & CHAT ---
with st.sidebar:
    st.image("https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg", width=140)
    st.markdown("### GURI AI CHAT")
    chat_input = st.text_input("Ask Market Move:", placeholder="Nifty kahan jayega?")
    if chat_input:
        st.markdown('<div class="ai-chat">🤖 <b>AI:</b> Nifty 21800 pe support le raha hai. Buying volume high hai, Call side momentum ban raha hai.</div>', unsafe_allow_html=True)
    st.divider()
    theme_color = st.color_picker("Custom Accent", "#00d09c")

# --- MAIN TERMINAL ---
m_choice = st.radio("", ["NIFTY 50", "BANK NIFTY", "SENSEX"], horizontal=True)
m_map = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "SENSEX": "^BSESN"}

df, ltp, change, pct = get_hyper_data(m_map[m_choice])

if df is not None:
    # Top Price Display
    c_color = "#00d09c" if change >= 0 else "#eb5b3c"
    st.markdown(f"""
        <div class="price-container">
            <p style="color: #888; margin:0; font-size:12px;">{m_choice} LIVE INDEX</p>
            <h1 style="margin:0; font-size:45px;">₹{ltp:,.2f}</h1>
            <p style="color:{c_color}; font-size:20px; font-weight:bold;">
                {'+' if change >= 0 else ''}{change:.2f} ({pct:.2f}%) Today
            </p>
        </div>
    """, unsafe_allow_html=True)

    # AI Signal Generation
    st.markdown("### AI LIVE SCALPER")
    trend = "CALL" if ltp > df['Close'].rolling(10).mean().iloc[-1] else "PUT"
    
    col1, _ = st.columns([2,1])
    with col1:
        if trend == "CALL":
            st.markdown(f'<div class="sig-flex"><div class="btn-call">BUY CALL (CE) DETECTED</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="sig-flex"><div class="btn-put">BUY PUT (PE) DETECTED</div></div>', unsafe_allow_html=True)
        st.caption(f"🎯 Target: {ltp+35 if trend=='CALL' else ltp-35:.1f} | 🛡️ SL: {ltp-15 if trend=='CALL' else ltp+15:.1f}")

    # Candlestick Graph
    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing_line_color='#00d09c', decreasing_line_color='#eb5b3
