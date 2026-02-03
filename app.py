import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import random

# --- CONFIG & THEME ---
if 'theme_color' not in st.session_state:
    st.session_state.theme_color = "#00d09c"

st.set_page_config(page_title="GURI AI SIGNALS", layout="wide", initial_sidebar_state="expanded")

# --- SIDEBAR: PHOTO & THEME ---
with st.sidebar:
    my_photo_url = "https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg"
    st.image(my_photo_url, caption="GURI TRADER PB13", width=150)
    st.session_state.theme_color = st.color_picker("Dashboard Theme", st.session_state.theme_color)
    st.divider()
    st.info("AI Logic: Tracking 0.001s Price Action")

# --- DATA & AI SIGNAL ENGINE ---
@st.cache_data(ttl=0.01)
def get_live_signals(symbol):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="1d", interval="1m")
    if not df.empty:
        ltp = df['Close'].iloc[-1]
        prev_close = ticker.info.get('previousClose', df['Open'].iloc[0])
        change = ltp - prev_close
        pct = (change / prev_close) * 100
        
        # --- AI SIGNAL LOGIC (CORE) ---
        # Moving Average + Volume Spike for Signal
        sma = df['Close'].rolling(window=20).mean().iloc[-1]
        vol_spike = df['Volume'].iloc[-1] > df['Volume'].rolling(10).mean().iloc[-1]
        
        signal = "WAIT"
        if ltp > sma and vol_spike: signal = "BUY_CALL"
        elif ltp < sma and vol_spike: signal = "BUY_PUT"
        
        return df, ltp, change, pct, signal
    return None, 0, 0, 0, "WAIT"

# --- UI LAYOUT ---
st.markdown(f"### 🖥️ GURI TERMINAL - AI LIVE SIGNALS")
market = st.radio("Select Market:", ["NIFTY 50", "BANK NIFTY", "SENSEX"], horizontal=True)
m_map = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "SENSEX": "^BSESN"}

df, ltp, change, pct, ai_sig = get_live_signals(m_map[market])

if df is not None:
    # --- LIVE PRICE & CHANGE ---
    c_color = "#00d09c" if change >= 0 else "#eb5b3c"
    st.markdown(f"""
        <div style="background:white; padding:20px; border-radius:15px; border-left:8px solid {st.session_state.theme_color};">
            <h1 style="margin:0;">{market}</h1>
            <h2 style="margin:0;">₹{ltp:,.2f}</h2>
            <p style="color:{c_color}; font-size:20px; font-weight:bold;">{'+' if change >= 0 else ''}{change:.2f} ({pct:.2f}%)</p>
        </div>
    """, unsafe_allow_html=True)

    # --- 🚨 DYNAMIC AI CALL/PUT SIGNALS 🚨 ---
    st.write("---")
    if ai_sig != "WAIT":
        strike = round(ltp / 50) * 50
        sig_type = "CALL (CE)" if ai_sig == "BUY_CALL" else "PUT (PE)"
        sig_color = "#00d09c" if ai_sig == "BUY_CALL" else "#eb5b3c"
        
        st.markdown(f"""
            <div style="background:{sig_color}; color:white; padding:25px; border-radius:15px; text-align:center;">
                <h2 style="margin:0;">🚀 AI SIGNAL: BUY {market} {strike} {sig_type}</h2>
                <div style="display:flex; justify-content:space-around; margin-top:15px;">
                    <div><b>ENTRY</b><br>₹{ltp:.2f}</div>
                    <div><b>TARGET</b><br>₹{ltp+45 if ai_sig=="BUY_CALL" else ltp-45:.2f}</div>
                    <div><b>STOP LOSS</b><br>₹{ltp-20 if ai_sig=="BUY_CALL" else ltp+20:.2f}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚖️ AI Analysis: Market Sideways... Waiting for Volume Breakout.")

    # --- LIVE CHART ---
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.update_layout(height=450, template="plotly_white", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# --- CHULBULI BAATEIN (3-Min Update) ---
if 'last_tip_time' not in st.session_state:
    st.session_state.last_tip_time = time.time()
    st.session_state.current_tip = "Guri bhai, aaj market mood mein lag raha hai! 🚀"

if time.time() - st.session_state.last_tip_time > 180:
    tips = ["Profit book karo, lalach nahi! 💰", "SL hit hua toh zid mat karo, nikal jao! ⛑️", "Guri ka AI sabse fast hai, dhyan se trade karo! 🔥"]
    st.session_state.current_tip = random.choice(tips)
    st.session_state.last_tip_time = time.time()

st.info(f"💡 **Chulbuli Tip:** {st.session_state.current_tip}")

# --- FAST REFRESH ---
time.sleep(0.01)
st.rerun()
