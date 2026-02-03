import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import random

# --- PRO THEME & DESIGN ---
st.set_page_config(page_title="Guri AI Terminal", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Sora', sans-serif; background-color: #fcfdfe; }
    
    /* Premium Header */
    .main-header { display: flex; align-items: center; gap: 15px; background: #fff; padding: 15px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .profile-img { width: 50px; height: 50px; border-radius: 50%; border: 2px solid #00d09c; }

    /* Signal Cards */
    .sig-card { padding: 20px; border-radius: 12px; margin-bottom: 15px; text-align: center; border: 2px solid #e2e8f0; }
    .call-btn { background: #00d09c; color: white; border-radius: 8px; padding: 10px; font-weight: bold; }
    .put-btn { background: #eb5b3c; color: white; border-radius: 8px; padding: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- ROBUST DATA ENGINE ---
@st.cache_data(ttl=0.1)
def get_safe_data(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="1m").tail(30)
        if not df.empty:
            ltp = df['Close'].iloc[-1]
            prev = t.info.get('previousClose', df['Open'].iloc[0])
            return df, float(ltp), float(ltp - prev), float(((ltp - prev) / prev) * 100)
    except Exception:
        pass
    return None, 0.0, 0.0, 0.0

# --- HEADER SECTION ---
st.markdown(f"""
    <div class="main-header">
        <img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" class="profile-img">
        <div><h2 style="margin:0;">GURI TERMINAL <span style="color:#00d09c;">AI</span></h2></div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR & CHAT MEMORY ---
with st.sidebar:
    st.markdown("### 🗨️ AI Chat Support")
    if 'chat_mem' not in st.session_state: st.session_state.chat_mem = []
    
    user_q = st.text_input("Ask Market...", placeholder="Nifty view?")
    if user_q:
        st.session_state.chat_mem.append(f"👤: {user_q}")
        st.session_state.chat_mem.append(f"🤖: Analysis checking... Resistance at 25950. Trade safe!")
    
    for m in st.session_state.chat_mem[-4:]: st.write(m)
    st.divider()

# --- MAIN ENGINE ---
m_list = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK"}
selected = st.selectbox("", list(m_list.keys()), label_visibility="collapsed")
df, ltp, change, pct = get_safe_data(m_list[selected])

col_signals, col_chart = st.columns([1, 2.5])

if df is not None and ltp > 0:
    with col_signals:
        # FIXED ERROR LOGIC: Using float check to prevent TypeError
        mean_price = df['Close'].mean()
        rsi_sim = 52 # Logic for future RSI
        
        if ltp > mean_price:
            st.markdown('<div class="sig-card" style="border-color:#00d09c;">'
                        '<h3 style="color:#00d09c;">🚀 BUY CALL</h3>'
                        f'<p>Entry: {ltp:.2f}<br>TGT: {ltp+40:.2f}<br>SL: {ltp-20:.2f}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="sig-card" style="border-color:#eb5b3c;">'
                        '<h3 style="color:#eb5b3c;">📉 BUY PUT</h3>'
                        f'<p>Entry: {ltp:.2f}<br>TGT: {lt
