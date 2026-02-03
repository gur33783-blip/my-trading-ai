import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import random

# --- HIGH VISIBILITY THEME CONFIG ---
st.set_page_config(page_title="Guri AI Terminal", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@500;700;900&display=swap');
    
    /* Global Font and Contrast */
    html, body, [class*="st-"] { 
        font-family: 'Roboto', sans-serif; 
        background-color: #f0f2f6; 
        color: #1a202c; 
    }
    .stApp { background-color: #f0f2f6; }
    
    /* Header Card */
    .main-header { 
        display: flex; align-items: center; gap: 20px; 
        background: #ffffff; padding: 20px; border-radius: 15px; 
        box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-bottom: 4px solid #00d09c;
    }
    .profile-img { width: 65px; height: 65px; border-radius: 50%; border: 3px solid #00d09c; object-fit: cover; }

    /* Signal Cards with High Contrast */
    .sig-card { 
        padding: 25px; border-radius: 16px; margin-bottom: 20px; 
        text-align: center; border: 3px solid #cbd5e0; background: white;
    }
    .call-text { color: #059669; font-weight: 900; font-size: 28px; }
    .put-text { color: #dc2626; font-weight: 900; font-size: 28px; }
    
    /* Bold Labels */
    label, p, span { font-weight: 700 !important; color: #2d3748 !important; }
    h1 { font-weight: 900 !important; color: #1a202c !important; font-size: 50px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HYPER-SPEED ENGINE ---
@st.cache_data(ttl=0.01) # Near-zero latency caching
def get_ultra_fast_data(symbol):
    try:
        t = yf.Ticker(symbol)
        # Fetch only what's needed for 0.001s feel
        df = t.history(period="1d", interval="1m").tail(35)
        if not df.empty:
            info = t.fast_info
            ltp = info.last_price
            prev = info.previous_close
            change = ltp - prev
            pct = (change / prev) * 100
            return df, float(ltp), float(change), float(pct)
    except:
        pass
    return None, 0.0, 0.0, 0.0

# --- HEADER SECTION ---
st.markdown(f"""
    <div class="main-header">
        <img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" class="profile-img">
        <div>
            <h1 style="margin:0; font-size:32px !important; color:#1a202c !important;">GURI TERMINAL <span style="color:#00d09c;">AI PRO</span></h1>
            <p style="margin:0; color:#4a5568 !important;">Hyper-Speed Live Analysis</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- DASHBOARD LAYOUT ---
col_left, col_right = st.columns([1, 2.5])

m_list = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "SENSEX": "^BSESN"}
selected = st.sidebar.selectbox("INDEX SELECT", list(m_list.keys()))
df, ltp, change, pct = get_ultra_fast_data(m_list[selected])

if df is not None and ltp > 0:
    with col_left:
        # AI SIGNAL - HIGH VISIBILITY
        avg_p = df['Close'].mean()
        if ltp > avg_p:
            st.markdown(f"""<div class="sig-card" style="border-color:#059669;">
                <span class="call-text">🚀 BUY CALL</span><br>
                <p style="font-size:20px;">ENTRY: {ltp:.2f}<br><b>TGT: {ltp+45:.2f}</b><br>SL: {ltp-20:.2f}</p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="sig-card" style="border-color:#dc2626;">
                <span class="put-text">📉 BUY PUT</span><br>
                <p style="font-size:20px;">ENTRY: {ltp:.2f}<br><b>TGT: {ltp-45:.2f}</b><br>SL: {ltp+20:.2f}</p>
            </div>""", unsafe_allow_html=True)
        
        # CHULBULI TIP (Persistent)
        if 'tip' not in st.session_state or (time.time() - st.session_state.get('t_time', 0)) > 120:
            st.session_state.tip = random.choice(["Lalach mat kar bhai! 💰", "SL helmet hai, lagao! ⛑️", "Chai piyo, chill karo! ☕"])
            st.session_state.t_time = time.time()
        st.warning(f"💡 **TIP:** {st.session_state.tip}")

    with col_right:
        # PRICE DISPLAY
        c_color = "#059669" if change >= 0 else "#dc2626"
        st.markdown(f"""
            <div style="background:white; padding:20px; border-radius:15px; box-shadow:0 2px 10px rgba(0,0,0,0.05);">
                <h1 style="margin:0;">₹{ltp:,.2f}</h1>
                <p style="color:{c_color} !important; font-size:24px; margin:0;">
                    {'+' if change>=0 else ''}{change:.2f} ({pct:.2f}%)
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # CLEAN HIGH-RES CHART
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
            increasing_line_color='#059669', decreasing_line_color='#dc2626'
        )])
        fig.update_layout(
            height=480, template="plotly_white", xaxis_rangeslider_visible=False,
            margin=dict(l=0,r=0,t=10,b=0), font=dict(family="Roboto", size=14, color="#2d3748")
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Connecting to Exchange... Wait 2 Seconds.")

# --- SIDEBAR AI CHAT ---
with st.sidebar:
    st.divider()
    st.markdown("### 💬 GURI AI CHAT")
    if 'history' not in st.session_state: st.session_state.history = []
    
    q = st.text_input("Ask Guri...", key="sidebar_q")
    if q:
        st.session_state.history.append(f"👤: {q}")
        st.session_state.history.append(f"🤖: {selected} range mein hai, levels ka wait kar.")
    
    for msg in st.session_state.history[-4:]: st.info(msg)

# --- HYPER REFRESH ---
time.sleep(0.01)
st.rerun()
