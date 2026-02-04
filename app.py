import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import datetime
import pytz
import random

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="GURI GHOST V5.6", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
    :root { --gold: #f0b90b; --bg: #030303; --green: #02c076; --red: #f84960; }
    .stApp { background-color: var(--bg); color: #e9eaeb; }
    .price-box { background: #0d0d0d; padding: 20px; border-radius: 15px; border: 1px solid #222; text-align: center; }
    .price-val { font-family: 'JetBrains Mono'; font-size: 45px; color: var(--gold); font-weight: 800; }
    .intl-tag { background: #111; padding: 5px 12px; border-radius: 8px; border: 1px solid #333; font-size: 13px; font-weight: 800; }
    .alert-box { background: rgba(56, 189, 248, 0.1); border-left: 4px solid #38bdf8; padding: 12px; border-radius: 8px; margin-top: 10px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MARKET TIMING & HOLIDAY LOGIC ---
def is_market_open():
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(tz)
    # Weekend check
    if now.weekday() >= 5: return False
    # Time check (9:15 to 15:30)
    start = now.replace(hour=9, minute=15, second=0)
    end = now.replace(hour=15, minute=30, second=0)
    # Simple Holiday list (Bhai isme dates add kar sakte ho)
    holidays = ["2026-01-26", "2026-08-15", "2026-10-02"] 
    if now.strftime("%Y-%m-%d") in holidays: return False
    return start <= now <= end

# --- 3. DATA ENGINE (MULTI-SOURCE) ---
@st.cache_data(ttl=1)
def get_global_data(idx):
    try:
        symbols = {"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK", "NASDAQ": "^IXIC", "VIX": "^INDIAVIX"}
        t = yf.Ticker(symbols.get(idx, "^NSEI"))
        info = t.fast_info
        
        # Current Global Price
        curr = info.last_price
        change = ((curr - info.previous_close)/info.previous_close)*100
        
        # History for Indian Index only
        hist = pd.DataFrame()
        if idx in ["NIFTY", "BANKNIFTY"]:
            hist = t.history(period="1d", interval="1m")
            
        return {"df": hist, "price": curr, "change": change}
    except: return None

# --- 4. SIDEBAR (ADVANCED CHAT & CONTROL) ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid var(--gold); margin-bottom:10px;">""", unsafe_allow_html=True)
    
    st.title("🧠 ADVANCED AI")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if st.button("🗑️ CLEAR HISTORY"):
        st.session_state.messages = []
        st.rerun()

    user_q = st.chat_input("Duniya bhar ka kuch bhi pucho...")
    if user_q:
        # Advanced Logic Simulation
        nasdaq_val = get_global_data("NASDAQ")['change']
        response = f"Guri bhai, main dekh raha hoon NASDAQ abhi {nasdaq_val:+.2f}% par hai. Iska asar kal hamare market par dikhega. "
        if "gap" in user_q.lower(): response += "Global cues positive hain, Gap-up ki umeed hai."
        else: response += "Abhi market trap kar raha hai, thoda shant raho."
        
        st.session_state.messages.append({"role": "user", "content": user_q})
        st.session_state.messages.append({"role": "ai", "content": response})

    for msg in reversed(st.session_state.messages):
        color = "#38bdf8" if msg["role"] == "ai" else "#eee"
        st.markdown(f"<div style='background:#111; padding:10px; border-radius:8px; margin-bottom:5px; color:{color};'><b>{'🤖 AI' if msg['role']=='ai' else '👤 GURI'}:</b> {msg['content']}</div>", unsafe_allow_html=True)
    
    selected_idx = st.selectbox("CHOOSE INDEX", ["NIFTY", "BANKNIFTY"])

# --- 5. MAIN TERMINAL DASHBOARD ---
@st.fragment(run_every=1)
def global_terminal_v56(idx_name):
    market_status = is_market_open()
    idx_data = get_global_data(idx_name)
    nasdaq = get_global_data("NASDAQ")
    vix = get_global_data("VIX")
    
    if idx_data and nasdaq and vix:
        # GLOBAL CALCULATION (Alert Logic)
        impact_score = "NEUTRAL"
        impact_color = "#38bdf8"
        if nasdaq['change'] > 0.8 and vix['change'] < 0:
            impact_score = "🚀 BULLISH GLOBAL SIGNAL"
            impact_color = "#02c076"
        elif nasdaq['change'] < -0.8 or vix['change'] > 5:
            impact_score = "⚠️ GLOBAL PANIC DETECTED"
            impact_color = "#f84960"

        # HEADER (ALWAYS LIVE)
        st.markdown(f"""
            <div style="display:flex; gap:12px; margin-bottom:15px;">
                <div class="intl-tag">🌎 NASDAQ: <span style="color:{'#02c076' if nasdaq['change']>0 else '#f84960'}">{nasdaq['change']:+.2f}%</span></div>
                <div class="intl-tag">📉 VIX: {vix['price']:.2f}</div>
                <div class="intl-tag">⏰ MARKET: {'<span style="color:#02c076">OPEN</span>' if market_status else '<span style="color:#f84960">CLOSED</span>'}</div>
                <div class="intl-tag" style="border-color:{impact_color};">⚡ {impact_score}</div>
            </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1, 2.5])
        
        with c1:
            st.markdown(f"""
                <div class="price-box">
                    <p style="margin:0; color:#888;">{idx_name} LIVE</p>
                    <div class="price-val">₹{idx_data['price']:,.2f}</div>
                    <p style="font-size:18px; color:{'#02c076' if idx_data['change']>0 else '#f84960'};">{idx_data['change']:+.2f}%</p>
                </div>
            """, unsafe_allow_html=True)
            
            # GLOBAL REFLECTION ALERT
            st.markdown(f"""
                <div class="alert-box">
                    <b>🌍 Global Insight:</b><br>
                    Nasdaq {nasdaq['change']:+.2f}% aur VIX {vix['price']:.2f} ke hisab se hamare market mein abhi 
                    {'Strength' if nasdaq['change']>0 else 'Weakness'} bani hui hai.
                </div>
            """, unsafe_allow_html=True)

        with c2:
            if not idx_data['df'].empty:
                df = idx_data['df']
                fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                                increasing_line_color='#02c076', decreasing_line_color='#f84960')])
                fig.update_layout(height=450, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=f"v56_{idx_name}")
            else:
                st.warning("Guri bhai, Indian Market band hai, isliye chart refresh nahi ho raha. International metrics upar check karo.")

global_terminal_v56(selected_idx)
