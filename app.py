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
    
    .main-header { display: flex; align-items: center; gap: 15px; background: #fff; padding: 15px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .profile-img { width: 50px; height: 50px; border-radius: 50%; border: 2px solid #00d09c; object-fit: cover; }

    .sig-card { padding: 20px; border-radius: 12px; margin-bottom: 15px; text-align: center; border: 2px solid #e2e8f0; }
    .call-card { background: #f0fdf4; border-color: #00d09c; color: #166534; }
    .put-card { background: #fef2f2; border-color: #eb5b3c; color: #991b1b; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE: SAFE DATA ---
@st.cache_data(ttl=0.1)
def get_clean_data(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="1m").tail(30)
        if not df.empty:
            ltp = float(df['Close'].iloc[-1])
            prev = float(t.info.get('previousClose', df['Open'].iloc[0]))
            change = ltp - prev
            pct = (change / prev) * 100
            return df, ltp, change, pct
    except:
        pass
    return None, 0.0, 0.0, 0.0

# --- HEADER SECTION ---
st.markdown(f"""
    <div class="main-header">
        <img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" class="profile-img">
        <div><h2 style="margin:0;">GURI TERMINAL <span style="color:#00d09c;">AI PRO</span></h2></div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR & CHAT ---
with st.sidebar:
    st.markdown("### 🗨️ AI Chat Memory")
    if 'chat_log' not in st.session_state: st.session_state.chat_log = []
    
    user_q = st.text_input("Guri AI se pucho...", placeholder="Aaj market kaisa hai?")
    if user_q:
        st.session_state.chat_log.append(f"👤: {user_q}")
        st.session_state.chat_log.append(f"🤖: Bhai fikar mat kar, logic setup hai. Entry bante hi batata hoon!")
    
    for m in st.session_state.chat_log[-4:]: st.info(m)
    st.divider()

# --- MAIN DASHBOARD ---
m_list = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "SENSEX": "^BSESN"}
selected = st.selectbox("", list(m_list.keys()), label_visibility="collapsed")
df, ltp, change, pct = get_clean_data(m_list[selected])

col_sig, col_chart = st.columns([1, 2.5])

if df is not None and ltp > 0:
    with col_sig:
        # AI SIGNALS LOGIC
        avg_price = df['Close'].mean()
        
        if ltp > avg_price:
            # FIX: Clean string concatenation to avoid SyntaxError
            msg = f"🚀 BUY CALL<br>Entry: {ltp:.2f}<br>TGT: {ltp+40.0:.2f}<br>SL: {ltp-20.0:.2f}"
            st.markdown(f'<div class="sig-card call-card"><h3>{msg}</h3></div>', unsafe_allow_html=True)
        else:
            msg = f"📉 BUY PUT<br>Entry: {ltp:.2f}<br>TGT: {ltp-40.0:.2f}<br>SL: {ltp+20.0:.2f}"
            st.markdown(f'<div class="sig-card put-card"><h3>{msg}</h3></div>', unsafe_allow_html=True)
        
        # CHULBULI TIPS
        if 't_time' not in st.session_state or (time.time() - st.session_state.t_time) > 180:
            tips = [
                "Guri bhai, profit ho toh screen off, lalach buri bala hai! 💰",
                "SL hit hua? Zid mat karo, market se panga mat lo! ⛑️",
                "Aaj market mood mein lag raha hai, dhyan se! 🚀",
                "Chai peeo aur trade dekho, jaldbazi mein nuksan hota hai! ☕"
            ]
            st.session_state.curr_tip = random.choice(tips)
            st.session_state.t_time = time.time()
        
        st.warning(f"💡 **Chulbuli Tip:** {st.session_state.curr_tip}")

    with col_chart:
        c_color = "#00d09c" if change >= 0 else "#eb5b3c"
        st.markdown(f"<h1 style='margin:0;'>₹{ltp:,.2f}</h1>"
                    f"<p style='color:{c_color}; font-weight:700; font-size:20px;'>{'+' if change>=0 else ''}{change:.2f} ({pct:.2f}%) Today</p>", unsafe_allow_html=True)
        
        # PROFESSIONAL CHART
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                                             increasing_line_color='#00d09c', decreasing_line_color='#eb5b3c')])
        fig.update_layout(height=450, template="plotly_white", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Market data fetch nahi ho raha. Check Internet ya Market Hours.")

# --- HYPER REFRESH ---
time.sleep(0.1)
st.rerun()
