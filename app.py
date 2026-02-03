import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import random

# --- 1. SUPREME UI & COLOR LOGIC ---
st.set_page_config(page_title="GURI GHOST TERMINAL V5", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
    :root { --gold: #f0b90b; --bg: #030303; --green: #02c076; --red: #f84960; --sky: #38bdf8; }
    .stApp { background-color: var(--bg); color: #e9eaeb; }
    .main-card { background: #0d0d0d; padding: 25px; border-radius: 20px; border: 1px solid #222; margin-bottom: 10px; }
    .price-text { font-family: 'JetBrains Mono'; font-size: 55px; font-weight: 800; color: var(--gold); line-height: 1; }
    .chat-box { background: #111; border-radius: 15px; border-left: 5px solid var(--gold); padding: 15px; height: 300px; overflow-y: auto; }
    .speed-meter-high { color: var(--green); font-weight: 800; font-size: 20px; }
    .speed-meter-low { color: var(--red); font-weight: 800; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FAST DATA ENGINE ---
@st.cache_data(ttl=0.1)
def fetch_data_v5(idx):
    try:
        sym = "^NSEI" if idx == "NIFTY" else "^NSEBANK"
        t = yf.Ticker(sym)
        hist = t.history(period="1d", interval="1m").tail(60)
        curr = hist['Close'].iloc[-1]
        change = ((curr - t.fast_info.previous_close)/t.fast_info.previous_close)*100
        return {"df": hist, "price": curr, "change": change}
    except: return None

# --- 3. SIDEBAR & MEMORY ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid var(--gold);">""", unsafe_allow_html=True)
    st.title("🎯 SNIPER V5")
    selected_idx = st.selectbox("MARKET", ["NIFTY", "BANKNIFTY"])
    st.info(f"Guri bhai, 2% Risk Rule ke mutabik Stop-Loss zaroor lagana.")

# --- 4. TERMINAL FRAGMENT ---
@st.fragment(run_every=1)
def terminal_core(idx_name):
    data = fetch_data_v5(idx_name)
    nasdaq = fetch_data_v5("NASDAQ") # Simulating for global
    
    if data:
        # MOMENTUM LOGIC (Yad rakhne ki zaroorat nahi, AI khud batayega)
        velocity = (data['df']['Close'].iloc[-1] - data['df']['Close'].iloc[-3])
        momentum = abs(velocity) * 15
        
        c1, c2 = st.columns([1.8, 2.2])
        
        with c1:
            st.markdown(f"""
                <div class="main-card">
                    <p style="margin:0; color:#888;">{idx_name} LIVE PRICE</p>
                    <div class="price-text">₹{data['price']:,.2f}</div>
                    <p style="font-size:22px; color:{'#02c076' if data['change']>0 else '#f84960'};">{data['change']:+.2f}% Today</p>
                    <hr style="border-color:#222;">
                    <div class="{'speed-meter-high' if momentum > 30 else 'speed-meter-low'}">
                        🚀 Speed: {momentum:.1f} {'(ENTRY OK)' if momentum > 30 else '(RUK JAO)'}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # --- HINDI AI ADVISOR ---
            status = "NEUTRAL"
            hindi_advice = "Bhai, market abhi sust hai. Choti candles ban rahi hain, be-fuzool premium mat pighlao."
            
            if momentum > 35 and data['change'] > 0:
                status = "BULLISH"
                hindi_advice = "🔥 BHAAGNE WALA HAI! Speed achhi hai, CE side ka mauka dekh sakte ho. 2% SL pakka lagana."
            elif momentum > 35 and data['change'] < 0:
                status = "BEARISH"
                hindi_advice = "📉 NEECHE JAYEGA! Momentum sellers ke saath hai. PE side par dhyaan do."

            st.markdown(f"""
                <div style="background:rgba(240, 185, 11, 0.1); border-left:5px solid var(--gold); padding:15px; border-radius:10px;">
                    <b style="color:var(--gold);">🤖 GURI AI SALAH (Hindi):</b><br>{hindi_advice}
                </div>
            """, unsafe_allow_html=True)

        with col2 := c2:
            # CHART
            df = data['df']
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                            increasing_line_color='#02c076', decreasing_line_color='#f84960')])
            
            # On-Chart Signal
            if momentum > 40:
                msg = "🚀 ENTRY LO" if data['change'] > 0 else "📉 EXIT / SELL"
                fig.add_annotation(x=df.index[-1], y=df['Close'].iloc[-1], text=msg, showarrow=True, arrowhead=2, arrowcolor="white", bgcolor="#f0b90b")

            fig.update_layout(height=450, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- 5. AI CHATBOX (GURI LIVE ASSISTANT) ---
st.markdown("---")
st.subheader("💬 GURI AI LIVE CHAT (Bhai se pucho)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "ai", "text": "Guri bhai, koi trade li hai? Ya market ke baare mein kuch puchna hai? Yahan likho."}]

chat_col1, chat_col2 = st.columns([2, 1])

with chat_col1:
    user_input = st.chat_input("Apna sawal yahan likho (e.g., 'Bhai Put li hai, kya karun?')")
    
    if user_input:
        # Simple Logic to Respond in Hindi
        response = "Bhai, chart dekh kar lag raha hai ki abhi thoda wait karna chahiye."
        if "put" in user_input.lower() or "pe" in user_input.lower():
            response = "Guri bhai, agar Put li hai toh VIX par nazar rakho. Agar price FII Sell Zone ke niche hai toh hold karo, warna stop-loss trail karo."
        elif "call" in user_input.lower() or "ce" in user_input.lower():
            response = "Bhai, Call ke liye momentum achha chahiye. Speedometer check karo, agar 30 se upar hai toh hi baitho."
        
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        st.session_state.chat_history.append({"role": "ai", "text": response})

    # Display Chat
    for chat in reversed(st.session_state.chat_history):
        color = "#38bdf8" if chat['role'] == "ai" else "#e9eaeb"
        st.markdown(f"<p style='color:{color};'><b>{'🤖 AI' if chat['role']=='ai' else '👤 GURI'}:</b> {chat['text']}</p>", unsafe_allow_html=True)

with chat_col2:
    st.markdown("""
        <div style="background:#111; padding:15px; border-radius:10px; border:1px solid #333;">
            <p style="color:var(--gold); font-weight:800; margin-bottom:5px;">📊 QUICK CHECKLIST</p>
            <ul style="font-size:13px; padding-left:20px;">
                <li>GIFT Nifty Green hai?</li>
                <li>Speed 30 se upar hai?</li>
                <li>Nasdaq support kar raha hai?</li>
                <li>2% SL lagaya hai?</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

terminal_core(selected_idx)
