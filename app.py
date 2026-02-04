import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

# --- 1. CONFIG ---
st.set_page_config(page_title="GURI GHOST V5.9", layout="wide")

st.markdown("""
    <style>
    :root { --gold: #f0b90b; --bg: #030303; --green: #02c076; --red: #f84960; }
    .stApp { background-color: var(--bg); color: #eee; }
    .price-box { background: #0d0d0d; padding: 25px; border-radius: 20px; border: 1px solid #333; text-align: center; }
    .price-val { font-family: 'JetBrains Mono'; font-size: 52px; color: var(--gold); font-weight: 800; }
    .ai-box { background: rgba(56, 189, 248, 0.05); border-left: 5px solid #38bdf8; padding: 15px; border-radius: 12px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE SMART AI BRAIN ---
def get_market_wisdom(query, price, change, momentum):
    q = query.lower()
    if "call" in q or "ce" in q:
        if momentum > 30 and change > 0:
            return f"Guri bhai, momentum tez hai (Speed: {momentum:.1f}). Call side ka setup ban raha hai, ₹{price} par nazar rakho!"
        return "Bhai, market sust hai ya niche ja raha hai. Call mein premium pighal jayega, abhi mat lo."
    
    if "put" in q or "pe" in q:
        if change < 0:
            return f"Bhai, trend bearish hai. Nifty ₹{price} ke niche aur speed pakad sakta hai. Put side focus karo."
        return "Guri bhai, market gir nahi raha. Put side mein trap ho sakte ho, wait karo."
    
    return f"Guri bhai, abhi Nifty ₹{price} par hai. Speedometer {momentum:.1f} dikha raha hai. Thoda wait karna hi samajhdari hai."

# --- 3. FAST DATA ENGINE ---
@st.cache_data(ttl=1)
def fetch_fast_data(idx):
    try:
        sym = "^NSEI" if idx == "NIFTY" else "^NSEBANK"
        t = yf.Ticker(sym)
        # Fast Info for Price
        curr = t.fast_info.last_price
        prev_close = t.fast_info.previous_close
        change = ((curr - prev_close)/prev_close)*100
        # History for Chart & Momentum
        hist = t.history(period="1d", interval="1m").tail(60)
        
        # Momentum calculation safety
        momentum = 0.0
        if len(hist) >= 3:
            momentum = abs(hist['Close'].iloc[-1] - hist['Close'].iloc[-3]) * 15
            
        return {"df": hist, "price": curr, "change": change, "momentum": momentum}
    except Exception as e:
        return None

# --- 4. SIDEBAR CHAT ---
with st.sidebar:
    st.title("🧠 GURI AI CHAT")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Accurate Data for AI
    current_idx = st.selectbox("Market Select", ["NIFTY", "BANKNIFTY"])
    live = fetch_fast_data(current_idx)
    
    user_input = st.chat_input("Live advice lo...")
    if user_input and live:
        reply = get_market_wisdom(user_input, live['price'], live['change'], live['momentum'])
        st.session_state.messages.append({"role": "user", "text": user_input})
        st.session_state.messages.append({"role": "ai", "text": reply})
    
    if st.button("🗑️ CLEAR"): st.session_state.messages = []
    
    for m in reversed(st.session_state.messages):
        color = "#f0b90b" if m["role"] == "ai" else "#eee"
        st.markdown(f"<p style='color:{color}; font-size:14px;'><b>{'🤖 AI' if m['role']=='ai' else '👤 GURI'}:</b> {m['text']}</p>", unsafe_allow_html=True)

# --- 5. MAIN TERMINAL ---
@st.fragment(run_every=1)
def render_terminal(idx_name):
    data = fetch_fast_data(idx_name)
    if data:
        # Header Info
        st.markdown(f"""
            <div style="display:flex; gap:15px; margin-bottom:20px;">
                <div style="background:#111; padding:10px 15px; border-radius:10px; border:1px solid #333; font-weight:800;">
                    🚀 SPEED: <span style="color:#f0b90b">{data['momentum']:.1f}</span>
                </div>
                <div style="background:#111; padding:10px 15px; border-radius:10px; border:1px solid #333; font-weight:800;">
                    📡 STATUS: <span style="color:#02c076">LIVE</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1, 2.3])
        with c1:
            st.markdown(f"""
                <div class="price-box">
                    <p style="margin:0; color:#888;">{idx_name} PRICE</p>
                    <div class="price-val">₹{data['price']:,.2f}</div>
                    <p style="font-size:22px; font-weight:800; color:{'#02c076' if data['change']>0 else '#f84960'};">{data['change']:+.2f}%</p>
                </div>
            """, unsafe_allow_html=True)
            
            # AI Salah Section
            color = "#02c076" if data['momentum'] > 30 else "#f84960"
            st.markdown(f"""
                <div class="ai-box" style="border-left-color:{color};">
                    <b style="color:{color};">🤖 GURI AI SALAH:</b><br>
                    {'🔥 Momentum fast hai, setup dhoondo!' if data['momentum']>30 else '💤 Market sust hai, trap mat hona.'}
                </div>
            """, unsafe_allow_html=True)

        with c2:
            fig = go.Figure(data=[go.Candlestick(x=data['df'].index, open=data['df']['Open'], high=data['df']['High'], low=data['df']['Low'], close=data['df']['Close'],
                            increasing_line_color='#02c076', decreasing_line_color='#f84960')])
            fig.update_layout(height=480, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

render_terminal(current_idx)
