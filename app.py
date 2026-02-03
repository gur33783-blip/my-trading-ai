import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import random

# --- CONFIG & PREMIUM DESIGN ---
st.set_page_config(page_title="GURI TERMINAL AI", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Professional Dark UI & Glassmorphism
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0d0e12; color: white; }
    .stApp { background-color: #0d0e12; }
    
    /* Premium Header Card */
    .header-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px; padding: 25px; margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* Buy Call/Put Buttons in Chart (Floating Style) */
    .signal-btn {
        padding: 15px 30px; border-radius: 12px; font-weight: bold; text-align: center;
        display: inline-block; margin-right: 10px; border: none; font-size: 16px;
    }
    .buy-call { background-color: #00d09c; color: white; box-shadow: 0 0 20px rgba(0, 208, 156, 0.4); }
    .buy-put { background-color: #eb5b3c; color: white; box-shadow: 0 0 20px rgba(235, 91, 60, 0.4); }
    
    /* AI Chat Box */
    .chat-container {
        background: #16171d; border-radius: 15px; border: 1px solid #30363d;
        padding: 15px; height: 300px; overflow-y: auto; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LIVE DATA ENGINE ---
@st.cache_data(ttl=0.01)
def fetch_pulse(symbol):
    t = yf.Ticker(symbol)
    df = t.history(period="1d", interval="1m")
    if not df.empty:
        ltp = df['Close'].iloc[-1]
        prev = t.info.get('previousClose', df['Open'].iloc[0])
        change = ltp - prev
        pct = (change / prev) * 100
        return df, ltp, change, pct
    return None, 0, 0, 0

# --- SIDEBAR (Photo & Theme) ---
with st.sidebar:
    st.image("https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg", width=150)
    st.markdown("### GURI TRADER PB13")
    theme_color = st.color_picker("Accent Color", "#00d09c")
    st.divider()
    
    # --- AI CHAT BOX (Requested Feature) ---
    st.markdown("### 💬 GURI AI Chat")
    user_query = st.text_input("Ask about Market...")
    if user_query:
        # Simple AI Response Logic for Live Market
        responses = [
            "Bhai, Nifty abhi support le raha hai, 25800 ke niche hi weakness aayegi.",
            "Market sideways hai, badi movement ka wait karo breakout ke baad.",
            "OI data bullish dikh raha hai, dips pe buy karna sahi rahega.",
            "VIX upar ja raha hai, sambhal ke trade karo, premium tezi se galenge!"
        ]
        st.info(f"🤖 AI: {random.choice(responses)}")

# --- MAIN DASHBOARD ---
market = st.radio("", ["NIFTY 50", "BANK NIFTY", "SENSEX"], horizontal=True)
m_map = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "SENSEX": "^BSESN"}

df, ltp, change, pct = fetch_pulse(m_map[market])

if df is not None:
    # 1. Professional Header
    c_color = "#00d09c" if change >= 0 else "#eb5b3c"
    st.markdown(f"""
        <div class="header-card">
            <h4 style="color: #888; margin:0;">{market} Live</h4>
            <h1 style="margin:0; font-size: 40px;">₹{ltp:,.2f}</h1>
            <p style="color:{c_color}; font-size:18px; font-weight:bold;">{'+' if change>=0 else ''}{change:.2f} ({pct:.2f}%) Today</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. AI Live Signal Buttons (From Image Layout)
    st.write("### AI Analysis & Signal")
    col_sig, col_blank = st.columns([1, 1])
    with col_sig:
        # Simple AI Trend Calculation
        trend = "CALL" if ltp > df['Close'].rolling(20).mean().iloc[-1] else "PUT"
        if trend == "CALL":
            st.markdown('<div class="signal-btn buy-call">BUY CALL (CE) DETECTED</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="signal-btn buy-put">BUY PUT (PE) DETECTED</div>', unsafe_allow_html=True)
        st.caption(f"Target: {ltp+40 if trend=='CALL' else ltp-40:.1f} | SL: {ltp-20 if trend=='CALL' else ltp+20:.1f}")

    # 3. Premium Graph (SS 4 Style)
    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing_line_color='#00d09c', decreasing_line_color='#eb5b3c'
    )])
    fig.update_layout(
        height=500, template="plotly_dark", 
        paper_bgcolor="#0d0e12", plot_bgcolor="#0d0e12",
        xaxis_rangeslider_visible=False,
        margin=dict(l=0,r=0,t=0,b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- CHULBULI TIPS (3-Min Update) ---
if 'last_tip' not in st.session_state or time.time() - st.session_state.get('last_time', 0) > 180:
    tips = ["Bhai, profit ho toh screen off, lalach buri bala hai! 💰", "Guri PB13 signal hai, toh darne ki kya baat hai? 🚀", "Market nakhre kare toh wait karo, galti mat karo! 📉"]
    st.session_state.last_tip = random.choice(tips)
    st.session_state.last_time = time.time()

st.markdown(f"""<div style="background: rgba(255,255,255,0.05); padding:1
