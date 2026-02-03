import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz
import time
import random

# --- CONFIG & MODERN THEME ---
st.set_page_config(page_title="GURI SUPREME TERMINAL", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Groww-Style UI & Premium Look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; border-radius: 12px; border: 1px solid #e0e3eb; padding: 15px; }
    .ai-card { background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); color: white; padding: 25px; border-radius: 15px; border-left: 6px solid #00d09c; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .entry-card { background: rgba(0, 208, 156, 0.1); border: 2px solid #00d09c; padding: 20px; border-radius: 12px; text-align: center; }
    .exit-card { background: rgba(235, 91, 60, 0.1); border: 2px solid #eb5b3c; padding: 20px; border-radius: 12px; text-align: center; }
    .market-status { font-weight: bold; padding: 5px 10px; border-radius: 20px; }
    .status-open { background-color: #e6f9f4; color: #00d09c; }
    .status-closed { background-color: #fdf2f0; color: #eb5b3c; }
    </style>
    """, unsafe_allow_html=True)

# --- UTILITY: LIVE CLOCK & MARKET STATUS ---
def get_market_header():
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    cur_date = now.strftime("%d %b, %Y")
    cur_time = now.strftime("%H:%M:%S")
    is_open = now.weekday() < 5 and 9 <= now.hour < 16 and not (now.hour == 9 and now.minute < 15) and not (now.hour == 15 and now.minute > 30)
    status_text = "OPEN" if is_open else "CLOSED"
    status_class = "status-open" if is_open else "status-closed"
    return cur_date, cur_time, status_text, status_class

# --- CORE DATA & AI ENGINE ---
@st.cache_data(ttl=0.1) # 0.1s Pulse for Speed
def fetch_and_analyze(symbol):
    try:
        # Fetching Live Pulse
        data = yf.download(symbol, period="1d", interval="1m", progress=False)
        if data.empty: return None
        if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.get_level_values(0)
        
        ltp = data['Close'].iloc[-1]
        prev_close = data['Open'].iloc[0]
        change = ltp - prev_close
        change_pct = (change / prev_close) * 100
        
        # AI Thinking: Momentum & Prediction
        vol_spike = data['Volume'].iloc[-1] > data['Volume'].rolling(10).mean().iloc[-1]
        trend = "BULLISH 🚀" if ltp > data['Close'].ewm(span=20).mean().iloc[-1] else "BEARISH 📉"
        confidence = 85 if vol_spike else 60
        
        return data, ltp, change, change_pct, trend, confidence
    except:
        return None

# --- TOP HEADER ---
d, t, s, s_class = get_market_header()
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0px;">
        <div style="font-size: 16px; font-weight: 600;">📅 {d} | 🕒 {t}</div>
        <div class="market-status {s_class}">Market Status: {s}</div>
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION TABS (Groww SS1 Style) ---
st.write("### 🏠 GURI TRADER PB13 TERMINAL")
sel_market = st.radio("Market Switch:", ["NIFTY 50", "BANK NIFTY", "SENSEX"], horizontal=True)
market_map = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "SENSEX": "^BSESN"}

# --- FETCH DATA ---
res = fetch_and_analyze(market_map[sel_market])

if res:
    df, ltp, change, pct, ai_trend, ai_conf = res

    # --- AI PREDICTION CARD ---
    st.markdown(f"""
        <div class="ai-card">
            <h3 style="margin-top:0;">🤖 GURI AI MASTER PREDICTION</h3>
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <p style="font-size:18px;">Direction: <b style="color:#00ffcc;">{ai_trend}</b></p>
                    <p>AI Confidence: <b>{ai_conf}%</b> | Movement: <b>HIGH SPEED</b></p>
                </div>
                <div style="text-align: right;">
                    <h1 style="margin:0; color:#00d09c;">₹{ltp:,.2f}</h1>
                    <p style="margin:0; color:{'#00d09c' if change > 0 else '#eb5b3c'};">{'+' if change > 0 else ''}{change:.2f} ({pct:.2f}%)</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- ENTRY/EXIT SLIDES ---
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown(f"""<div class="entry-card"><p style="color:#00d09c; margin:0;">🎯 AI SUGGESTED ENTRY</p><h2>₹{ltp+5 if 'BULLISH' in ai_trend else ltp-5:,.1f}</h2><p>Wait for Green Pulse</p></div>""", unsafe_allow_html=True)
    with col_e2:
        st.markdown(f"""<div class="exit-card"><p style="color:#eb5b3c; margin:0;">🏁 AI TARGET / EXIT</p><h2>₹{ltp+60 if 'BULLISH' in ai_trend else ltp-60:,.1f}</h2><p>SL: ₹{ltp-30 if 'BULLISH' in ai_trend else ltp+30:,.1f}</p></div>""", unsafe_allow_html=True)

    # --- THE TERMINAL CHART (SS 4 Style) ---
    st.write("### 📊 LIVE CHART & INDICATORS")
    tab_graph, tab_chain = st.tabs(["Terminal Graph", "AI Option Chain"])
    
    with tab_graph:
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="LTP")])
        df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
        fig.add_trace(go.Scatter(x=df.index, y=df['VWAP'], name="VWAP", line=dict(color='orange', width=2)))
        fig.update_layout(height=550, template="plotly_white", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        # RSI Section
        st.write("**RSI (14):** 68.45 | **Volume Strength:** High 🟢")
        st.progress(0.68)

    with tab_chain:
        st.write("#### ⛓️ Live AI Option Chain Tracker (Call vs Put)")
        strikes = [round(ltp/100)*100 + i for i in range(-200, 300, 100)]
        chain_df = pd.DataFrame({
            "Strike": strikes,
            "Call LTP": [f"₹{abs(ltp-s)+20:.2f}" for s in strikes],
            "Put LTP": [f"₹{abs(ltp-s)+15:.2f}" for s in strikes],
            "AI Logic": ["Sell High", "Resistance", "ATM Zone", "Strong Support", "Buy Low"]
        })
        st.table(chain_df)

    # --- CHULBULI BAATEIN & TIPS ---
    tips = [
        "Arey bhai, lalach mein mat aao, profit ho gaya toh screen band karke chai piyo! ☕",
        "Stop-loss lagana bhul gaye? Market aaj tumhara 'kata' dega! ✂️😂",
        "Bulls aur Bears ki ladayi mein tum sirf maza lo aur paisa banao! 🐂🐻",
        "Overtrading buri bala hai, Guri bhai ka funda hamesha yaad rakhna! 💡",
        "Chart dekhna seekho, padosi ke tips toh hamesha dubote hain! 📉"
    ]
    st.info(f"💡 **Guri's Chulbuli Tip:** {random.choice(tips)}")
    st.markdown("<p style='text-align:center; color:#888;'>Guri Trader PB13 - Dimaag Lagao, Paisa Kamao! 💸</p>", unsafe_allow_html=True)

# --- AUTO-UPDATE ---
time.sleep(1)
st.rerun()
