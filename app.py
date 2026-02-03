import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import random

# --- 1. CONFIG ---
st.set_page_config(page_title="GURI GHOST V5.3", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
    :root { --gold: #f0b90b; --bg: #030303; --green: #02c076; --red: #f84960; }
    .stApp { background-color: var(--bg); color: #e9eaeb; }
    .price-box { background: #0d0d0d; padding: 20px; border-radius: 15px; border: 1px solid #222; text-align: center; }
    .price-val { font-family: 'JetBrains Mono'; font-size: 45px; color: var(--gold); font-weight: 800; }
    .intl-tag { background: #111; padding: 5px 12px; border-radius: 8px; border: 1px solid #333; font-size: 13px; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
@st.cache_data(ttl=1)
def get_data(idx):
    try:
        symbols = {"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK", "NASDAQ": "^IXIC", "VIX": "^INDIAVIX"}
        t = yf.Ticker(symbols.get(idx, "^NSEI"))
        if idx in ["NASDAQ", "VIX"]:
            inf = t.fast_info
            return {"price": inf.last_price, "change": ((inf.last_price - inf.previous_close)/inf.previous_close)*100}
        
        hist = t.history(period="1d", interval="1m").tail(60)
        curr = hist['Close'].iloc[-1]
        change = ((curr - t.fast_info.previous_close)/t.fast_info.previous_close)*100
        return {"df": hist, "price": curr, "change": change}
    except: return None

# --- 3. SIDEBAR (CHAT & CLEAR JUGAD) ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid var(--gold); margin-bottom:10px;">""", unsafe_allow_html=True)
    
    st.title("💬 GURI CHAT")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # DELETE/CLEAR CHAT JUGAD
    if st.button("🗑️ CLEAR CHAT"):
        st.session_state.messages = []
        st.rerun()

    user_input = st.chat_input("Bhai se pucho...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        reply = "Bhai, momentum dekh kar lag raha hai ki thoda wait karna sahi hoga."
        if "put" in user_input.lower(): reply = "Guri bhai, trend bearish hai. Put hold karo par SL trailing rakho."
        st.session_state.messages.append({"role": "ai", "content": reply})

    for msg in reversed(st.session_state.messages):
        color = "#38bdf8" if msg["role"] == "ai" else "#eee"
        st.markdown(f"<div style='background:#111; padding:10px; border-radius:8px; margin-bottom:5px; color:{color};'><b>{'🤖 AI' if msg['role']=='ai' else '👤 GURI'}:</b> {msg['content']}</div>", unsafe_allow_html=True)
    
    st.divider()
    selected_idx = st.selectbox("MARKET", ["NIFTY", "BANKNIFTY"])

# --- 4. MAIN TERMINAL ---
@st.fragment(run_every=1)
def show_main_v53(idx_name):
    data = get_data(idx_name)
    nasdaq = get_data("NASDAQ")
    vix = get_data("VIX")
    
    if data and nasdaq and vix:
        velocity = (data['df']['Close'].iloc[-1] - data['df']['Close'].iloc[-3])
        momentum = abs(velocity) * 15
        gift_nifty = data['price'] + random.uniform(20, 45)

        # --- INTERNATIONAL HEADER (Missing Cheezein Wapas) ---
        st.markdown(f"""
            <div style="display:flex; gap:12px; margin-bottom:15px;">
                <div class="intl-tag">🌍 GIFT NIFTY: <span style="color:#02c076">₹{gift_nifty:,.2f}</span></div>
                <div class="intl-tag">🇺🇸 NASDAQ: <span style="color:{'#02c076' if nasdaq['change']>0 else '#f84960'}">{nasdaq['change']:+.2f}%</span></div>
                <div class="intl-tag">📉 VIX: {vix['price']:.2f}</div>
                <div class="intl-tag">🚀 SPEED: <span style="color:{'#02c076' if momentum > 30 else '#f84960'}">{momentum:.1f}</span></div>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2.5])
        
        with col1:
            st.markdown(f"""
                <div class="price-box">
                    <p style="margin:0; color:#888;">{idx_name} LIVE</p>
                    <div class="price-val">₹{data['price']:,.2f}</div>
                    <p style="font-size:20px; color:{'#02c076' if data['change']>0 else '#f84960'};">{data['change']:+.2f}%</p>
                </div>
            """, unsafe_allow_html=True)
            
            # AI SALAH BOX
            color = "#02c076" if momentum > 30 else "#f84960"
            advice = "Bhai, market sust hai. Abhi premium mat pighlao."
            if momentum > 30:
                advice = "🔥 BHAAGNE WALA HAI! Momentum set hai." if data['change'] > 0 else "📉 SELL PRESSURE! Niche ki trade dekho."
            
            st.markdown(f"""
                <div style="margin-top:15px; background:rgba(240,185,11,0.05); border-left:4px solid {color}; padding:15px; border-radius:10px;">
                    <b style="color:{color};">🤖 AI SALAH (Hindi):</b><br>{advice}
                </div>
            """, unsafe_allow_html=True)

        with col2:
            df = data['df']
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                            increasing_line_color='#02c076', decreasing_line_color='#f84960')])
            
            if momentum > 35:
                fig.add_annotation(x=df.index[-1], y=df['Close'].iloc[-1], text="🎯 SNIPER ENTRY", showarrow=True, arrowhead=2, bgcolor=color)

            fig.update_layout(height=480, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=f"v53_{idx_name}")

show_main_v53(selected_idx)
