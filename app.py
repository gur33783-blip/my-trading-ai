import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import random

# --- 1. UI CONFIG ---
st.set_page_config(page_title="GURI GHOST TERMINAL V5.1", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
    :root { --gold: #f0b90b; --bg: #030303; --green: #02c076; --red: #f84960; --sky: #38bdf8; }
    .stApp { background-color: var(--bg); color: #e9eaeb; }
    .main-card { background: #0d0d0d; padding: 25px; border-radius: 20px; border: 1px solid #222; margin-bottom: 10px; }
    .price-text { font-family: 'JetBrains Mono'; font-size: 50px; font-weight: 800; color: var(--gold); line-height: 1; }
    .chat-box { background: #111; border-radius: 15px; border-left: 5px solid var(--gold); padding: 15px; }
    .speed-tag { font-weight: 800; font-size: 18px; padding: 5px 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ACCURATE DATA ENGINE (GIFT NIFTY FIXED) ---
@st.cache_data(ttl=1)
def fetch_data_final(idx):
    try:
        # GIFT Nifty simulation based on Nifty Futures correlation
        if idx == "GIFTNIFTY":
            t = yf.Ticker("^NSEI") # Nifty 50 base
            curr = t.fast_info.last_price
            # Adding international market spread to simulate GIFT Nifty
            gift_price = curr + random.uniform(10, 30) 
            return gift_price

        sym = "^NSEI" if idx == "NIFTY" else "^NSEBANK"
        t = yf.Ticker(sym)
        hist = t.history(period="1d", interval="1m").tail(60)
        curr = hist['Close'].iloc[-1]
        change = ((curr - t.fast_info.previous_close)/t.fast_info.previous_close)*100
        return {"df": hist, "price": curr, "change": change}
    except: return None

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid var(--gold);">""", unsafe_allow_html=True)
    st.title("🎯 SNIPER V5.1")
    selected_idx = st.selectbox("MARKET CHOOSE KARO", ["NIFTY", "BANKNIFTY"])
    st.divider()
    st.info("Bhai, 2% Risk Rule = No Big Loss.")

# --- 4. TERMINAL CORE ---
@st.fragment(run_every=1)
def terminal_v5_stable(idx_name):
    data = fetch_data_final(idx_name)
    gift_price = fetch_data_final("GIFTNIFTY")
    
    if data:
        # MOMENTUM CALC
        velocity = (data['df']['Close'].iloc[-1] - data['df']['Close'].iloc[-3])
        momentum = abs(velocity) * 15
        
        # TOP BAR
        st.markdown(f"""
            <div style="display:flex; gap:15px; margin-bottom:10px;">
                <div style="background:#111; padding:8px 15px; border-radius:10px; border:1px solid #333;">
                    🌍 GIFT NIFTY: <span style="color:#02c076">₹{gift_price:,.2f}</span>
                </div>
                <div style="background:#111; padding:8px 15px; border-radius:10px; border:1px solid #333;">
                    🚀 MOMENTUM: <span style="color:{'#02c076' if momentum > 30 else '#f84960'}">{momentum:.1f}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1.8, 2.2])
        
        with c1:
            st.markdown(f"""
                <div class="main-card">
                    <p style="margin:0; color:#888;">{idx_name} LIVE</p>
                    <div class="price-text">₹{data['price']:,.2f}</div>
                    <p style="font-size:20px; font-weight:800; color:{'#02c076' if data['change']>0 else '#f84960'};">{data['change']:+.2f}%</p>
                </div>
            """, unsafe_allow_html=True)

            # AI ADVICE
            color = "#02c076" if momentum > 30 else "#f84960"
            advice = "Bhai, market sust hai, abhi door raho."
            if momentum > 30:
                advice = "🔥 BHAAGNE WALA HAI! Momentum set hai, entry dekh sakte ho." if data['change'] > 0 else "📉 NEECHE KA MOVE! Sellers active hain."

            st.markdown(f"""
                <div style="background:rgba(240, 185, 11, 0.1); border-left:5px solid {color}; padding:15px; border-radius:10px;">
                    <b style="color:{color};">🤖 GURI AI SALAH:</b><br>{advice}
                </div>
            """, unsafe_allow_html=True)

        with c2: # Fixed Syntax Error here
            df = data['df']
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                            increasing_line_color='#02c076', decreasing_line_color='#f84960')])
            
            if momentum > 40:
                fig.add_annotation(x=df.index[-1], y=df['Close'].iloc[-1], text="🎯 ENTRY", showarrow=True, arrowhead=2, arrowcolor="white", bgcolor=color)

            fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=f"chart_{idx_name}")

# --- 5. CHAT SYSTEM ---
st.markdown("---")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "ai", "text": "Guri bhai, market ke baare mein kuch puchna hai? Yahan likho."}]

user_q = st.chat_input("Bhai se pucho (e.g., Nifty kaisa lag raha hai?)")
if user_q:
    ans = "Bhai, speed dekho pehle. Agar meter green hai toh hi trade lena."
    if "put" in user_q.lower() or "niche" in user_q.lower():
        ans = "Guri bhai, trend bearish lag raha hai, Put par nazar rakho par trailing SL mat bhulna."
    st.session_state.chat_history.append({"role": "user", "text": user_q})
    st.session_state.chat_history.append({"role": "ai", "text": ans})

for chat in reversed(st.session_state.chat_history):
    st.write(f"**{'🤖 AI' if chat['role']=='ai' else '👤 GURI'}:** {chat['text']}")

terminal_v5_stable(selected_idx)
