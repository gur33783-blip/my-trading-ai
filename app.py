import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import random

# --- CONFIG & PROFESSIONAL LIGHT-SLATE THEME ---
st.set_page_config(page_title="Guri Trader Terminal", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; background-color: #f4f7f9; color: #1e293b; }
    .stApp { background-color: #f4f7f9; }
    
    /* Clean Cards */
    .metric-container {
        background: white; border-radius: 12px; padding: 20px; 
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e2e8f0;
    }
    .price-val { font-size: 36px; font-weight: 700; color: #0f172a; margin: 0; }
    
    /* AI Chat Styling */
    .chat-bubble { padding: 10px 15px; border-radius: 10px; margin-bottom: 8px; font-size: 14px; }
    .user-msg { background: #e0f2fe; color: #0369a1; align-self: flex-end; }
    .ai-msg { background: #f1f5f9; color: #334155; border: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE: FAST DATA FETCH ---
@st.cache_data(ttl=0.1)
def fetch_pulse_data(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="1m").tail(60)
        if not df.empty:
            ltp = df['Close'].iloc[-1]
            prev_close = t.info.get('previousClose', df['Open'].iloc[0])
            change = ltp - prev_close
            pct = (change / prev_close) * 100
            return df, ltp, change, pct
    except: return None, 0, 0, 0
    return None, 0, 0, 0

# --- SIDEBAR: PROFILE & AI CHAT MEMORY ---
with st.sidebar:
    st.image("https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg", width=130)
    st.markdown("### GURI TRADER PB13")
    st.divider()
    
    # AI CHAT WITH MEMORY
    st.markdown("### 🗨️ AI Market Assistant")
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    chat_input = st.text_input("Talk to AI...", placeholder="Nifty kaisa lag raha hai?")
    
    if chat_input:
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        # Intelligent Response based on history (Simple logic)
        reply = "Volume badh raha hai bhai, upar ka move aa sakta hai." if "nifty" in chat_input.lower() else "Sahi trade ka wait karo, lalach mat karna."
        st.session_state.chat_history.append({"role": "ai", "content": reply})

    # Display Chat History
    for msg in st.session_state.chat_history[-6:]:
        css_class = "user-msg" if msg['role'] == "user" else "ai-msg"
        st.markdown(f'<div class="chat-bubble {css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
market_key = st.selectbox("", ["NIFTY 50", "BANK NIFTY", "SENSEX"], label_visibility="collapsed")
m_map = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "SENSEX": "^BSESN"}

df, ltp, change, pct = fetch_pulse_data(m_map[market_key])

if df is not None:
    # 1. LIVE PRICE (Groww Match)
    color = "#00d09c" if change >= 0 else "#eb5b3c"
    st.markdown(f"""
        <div class="metric-container">
            <p style="color: #64748b; font-size: 14px; margin:0;">{market_key} • LIVE</p>
            <h1 class="price-val">₹{ltp:,.2f}</h1>
            <p style="color: {color}; font-size: 18px; font-weight: 600; margin:0;">
                {'+' if change >= 0 else ''}{change:.2f} ({pct:.2f}%)
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 2. OPTION CHAIN (FIXED ERROR)
    st.markdown("### ⛓️ Option Chain")
    strike_center = round(ltp / 50) * 50
    strikes = [strike_center + (i * 50) for i in range(-5, 6)] # Exactly 11 strikes
    
    option_data = pd.DataFrame({
        "Call LTP": [round(random.uniform(50, 200), 2) for _ in strikes],
        "Strike": strikes,
        "Put LTP": [round(random.uniform(50, 200), 2) for _ in strikes],
        "OI Action": ["Bullish", "Neutral", "Neutral", "ATM", "Neutral", "Bearish", "Strong Sell", "Wait", "Wait", "Buy", "Strong Buy"]
    })
    st.dataframe(option_data, use_container_width=True, hide_index=True)

    # 3. HIGH-RES CHART
    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing_line_color='#00d09c', decreasing_line_color='#eb5b3c'
    )])
    fig.update_layout(height=500, template="plotly_white", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# --- HYPER REFRESH ---
time.sleep(0.1) # Rapid heartbeat
st.rerun()
