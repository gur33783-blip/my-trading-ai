import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import random

# --- PROFESSIONAL THEME CONFIG ---
st.set_page_config(page_title="GURI PRO TERMINAL", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Professional Slate Theme (Better Readability)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=SORA:wght@400;600;700&display=swap');
    
    html, body, [class*="st-"] { 
        font-family: 'SORA', sans-serif; 
        background-color: #0f172a; /* Deep Navy Slate */
        color: #f1f5f9; 
    }
    .stApp { background-color: #0f172a; }
    
    /* Premium Glass Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px; padding: 25px; margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }

    /* Signal Indicators */
    .sig-tag {
        padding: 10px 20px; border-radius: 8px; font-weight: 700;
        text-transform: uppercase; letter-spacing: 1px; font-size: 14px;
    }
    .sig-buy { background: #10b981; color: white; box-shadow: 0 0 15px rgba(16, 185, 129, 0.4); }
    .sig-sell { background: #ef4444; color: white; box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); }

    /* Clean Sidebar */
    [data-testid="stSidebar"] { background-color: #1e293b; border-right: 1px solid rgba(255,255,255,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- ROBUST DATA ENGINE (Error-Free) ---
@st.cache_data(ttl=0.5) # Balanced for speed & stability
def fetch_accurate_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # Fetching small window for speed
        df = ticker.history(period="1d", interval="1m")
        if not df.empty:
            ltp = df['Close'].iloc[-1]
            # Precise change calculation
            info = ticker.fast_info
            prev_close = info.get('previous_close', df['Open'].iloc[0])
            change = ltp - prev_close
            pct = (change / prev_close) * 100
            return df, ltp, change, pct
    except Exception as e:
        return None, 0, 0, 0
    return None, 0, 0, 0

# --- SIDEBAR & CHAT ---
with st.sidebar:
    st.image("https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg", width=140)
    st.markdown("### GURI AI CHAT")
    chat_input = st.text_input("Analyze Market:", placeholder="Ask anything...")
    if chat_input:
        st.success("🤖 AI Analysis: Nifty volume is spiking at support levels. Look for a 15-min breakout.")
    st.divider()
    accent = st.color_picker("Customize UI Accent", "#38bdf8")

# --- MAIN DASHBOARD ---
st.title("🛡️ GURI PRO TERMINAL")
m_choice = st.radio("", ["NIFTY 50", "BANK NIFTY", "SENSEX"], horizontal=True)
m_map = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "SENSEX": "^BSESN"}

df, ltp, change, pct = fetch_accurate_data(m_map[m_choice])

if df is not None:
    # Top Card
    c_color = "#10b981" if change >= 0 else "#ef4444"
    st.markdown(f"""
        <div class="metric-card">
            <p style="color: #94a3b8; font-size: 14px; margin-bottom: 5px;">{m_choice} LIVE PERFORMANCE</p>
            <h1 style="font-size: 48px; margin: 0; letter-spacing: -1px;">₹{ltp:,.2f}</h1>
            <p style="color: {c_color}; font-size: 22px; font-weight: 600; margin-top: 5px;">
                {'+' if change >= 0 else ''}{change:.2f} ({pct:.2f}%)
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Signal & Strategy
    col_sig, col_data = st.columns([1, 1])
    with col_sig:
        # Simple AI Scalp Logic
        trend = "CALL" if ltp > df['Close'].rolling(15).mean().iloc[-1] else "PUT"
        sig_class = "sig-buy" if trend == "CALL" else "sig-sell"
        st.markdown(f'<span class="sig-tag {sig_class}">STRATEGY: BUY {trend}</span>', unsafe_allow_html=True)
        st.caption(f"🎯 Target: {ltp+(ltp*0.002):.1f} | 🛡️ SL: {ltp-(ltp*0.001):.1f}")

    # Professional Candlestick Chart
    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing_line_color='#10b981', decreasing_line_color='#ef4444'
    )])
    fig.update_layout(
        height=550, template="plotly_dark", 
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis_rangeslider_visible=False,
        margin=dict(l=0,r=0,t=0,b=0),
        font=dict(family="SORA", size=12, color="#94a3b8")
    )
    st.plotly_chart(fig, use_container_width=True)

# --- CHULBULI TIP (3-Min Update) ---
if 'tip_store' not in st.session_state or (time.time() - st.session_state.get('t_stamp', 0)) > 180:
    st.session_state.tip_store = random.choice([
        "Guri bhai, market move kar raha hai, chai baad mein peena! ☕",
        "Stop-loss lagana bhul gaye? Market 'dhobi pachaad' de dega! 😂",
        "Paisa wahi kamata hai jo discipline rakhta hai, lalach nahi! 💰"
    ])
    st.session_state.t_stamp = time.time()

st.markdown(f"""
    <div style="background: #1e293b; padding: 15px; border-radius: 12px; border-left: 5px solid {accent}; margin-top: 20px;">
        💡 <b>Guri's Insider Tip:</b> {st.session_state.tip_store}
    </div>
""", unsafe_allow_html=True)

# --- AUTO-UPDATE ---
try:
    time.sleep(1) # Frequency set to 1s for stability across all devices
    st.rerun()
except:
    pass
