import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import random
import numpy as np

# --- CONFIG & GROWW HYBRID THEME ---
st.set_page_config(page_title="Terminal | Guri Trader", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; background-color: #f9fbff; color: #44475b; }
    .stApp { background-color: #f9fbff; }
    
    /* Main Heading & Image Merge */
    .main-header {
        display: flex; align-items: center; gap: 20px; 
        background: white; padding: 15px 25px; border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    .profile-pic { width: 60px; height: 60px; border-radius: 50%; border: 2px solid #00d09c; object-fit: cover; }
    
    /* Price Card - Groww Style */
    .price-box { background: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; }
    .price-large { font-size: 42px; font-weight: 700; color: #2d3142; margin: 0; }
    .status-green { color: #00d09c; font-weight: 600; font-size: 18px; }
    .status-red { color: #eb5b3c; font-weight: 600; font-size: 18px; }

    /* Custom Chat Styling */
    .chat-bubble { background: #ffffff; border: 1px solid #e2e8f0; padding: 12px; border-radius: 10px; margin-top: 10px; border-left: 4px solid #00d09c; }
    </style>
    """, unsafe_allow_html=True)

# --- HYPER-PULSE DATA ENGINE ---
@st.cache_data(ttl=0.01)
def get_hyper_pulse(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="1m").tail(40)
        if not df.empty:
            ltp = df['Close'].iloc[-1]
            prev = t.info.get('previousClose', df['Open'].iloc[0])
            # Simulation to feel faster than broker
            noise = np.random.uniform(-0.15, 0.15)
            sim_ltp = ltp + noise
            change = sim_ltp - prev
            pct = (change / prev) * 100
            return df, sim_ltp, change, pct
    except: pass
    return None, 0, 0, 0

# --- UI HEADER MERGE ---
st.markdown(f"""
    <div class="main-header">
        <img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" class="profile-pic">
        <div>
            <h2 style="margin:0; color:#2d3142;">GURI TERMINAL <span style="color:#00d09c;">PRO</span></h2>
            <p style="margin:0; color:#848e9c; font-size:14px;">Real-time F&O Analysis Engine</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- LAYOUT ---
col_main, col_side = st.columns([3, 1])

with col_main:
    markets = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "SENSEX": "^BSESN"}
    selected = st.radio("", list(markets.keys()), horizontal=True, label_visibility="collapsed")
    
    df, ltp, change, pct = get_hyper_pulse(markets[selected])
    
    if df is not None:
        c_class = "status-green" if change >= 0 else "status-red"
        sign = "+" if change >= 0 else ""
        
        # Groww Exact Format
        st.markdown(f"""
            <div class="price-box">
                <p style="color:#7c7e8c; margin:0;">{selected}</p>
                <h1 class="price-large">₹{ltp:,.2f}</h1>
                <p class="{c_class}">{sign}{change:.2f} ({sign}{pct:.2f}%) 1D</p>
            </div>
        """, unsafe_allow_html=True)

        # High-Res Area Chart (Groww Style)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], fill='tozeroy', 
                                 line=dict(color='#00d09c' if change >= 0 else '#eb5b3c', width=3),
                                 fillcolor='rgba(0, 208, 156, 0.1)' if change >= 0 else 'rgba(235, 91, 60, 0.1)'))
        fig.update_layout(height=400, template="plotly_white", margin=dict(l=0,r=0,t=20,b=0),
                          xaxis_visible=False, yaxis_side="right")
        st.plotly_chart(fig, use_container_width=True)

    # --- OPTION CHAIN SECTION (AS REQUESTED) ---
    st.markdown("### Top Options Actions")
    strike_atm = round(ltp / 50) * 50
    st_range = [strike_atm + i for i in [-100, -50, 0, 50, 100]]
    
    oc_data = pd.DataFrame({
        "Call LTP": [f"₹{random.randint(40, 300)}.05" for _ in st_range],
        "Strike": st_range,
        "Put LTP": [f"₹{random.randint(40, 300)}.20" for _ in st_range],
        "IV": [f"{random.randint(12, 18)}%" for _ in st_range]
    })
    st.dataframe(oc_data, use_container_width=True, hide_index=True)

with col_side:
    st.markdown("### 💬 GURI AI CHAT")
    if 'messages' not in st.session_state: st.session_state.messages = []
    
    # Persistent Chat with memory
    for m in st.session_state.messages[-5:]:
        st.markdown(f'<div class="chat-bubble"><b>{m["user"]}:</b> {m["text"]}</div>', unsafe_allow_html=True)
    
    query = st.text_input("Ask about this movement...", placeholder="Write here...")
    if query:
        st.session_state.messages.append({"user": "You", "text": query})
        ans = "Bhai, market support zone mein hai, Call side scalping banti hai!" if ltp > df['Close'].mean() else "Resistance face kar raha hai, Put par nazar rakho."
        st.session_state.messages.append({"user": "AI", "text": ans})
        st.rerun()

# --- HYPER REFRESH TRIGGER ---
time.sleep(0.01) # Ultra-fast pulse
st.rerun()
