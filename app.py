import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import numpy as np
import random

# --- PREMIUM UI/UX CONFIG ---
st.set_page_config(page_title="Guri Hyper Terminal", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@600;800&family=JetBrains+Mono:wght@700&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Outfit', sans-serif; background: #f0f4f8; }
    
    /* Zero-Flicker Premium Header */
    .terminal-header {
        display: flex; align-items: center; justify-content: space-between;
        background: #ffffff; padding: 20px 30px; border-radius: 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); border-bottom: 5px solid #00d09c;
        margin-bottom: 20px;
    }
    .profile-group { display: flex; align-items: center; gap: 20px; }
    .profile-img { width: 65px; height: 65px; border-radius: 50%; border: 3px solid #00d09c; box-shadow: 0 0 15px rgba(0,208,156,0.3); }
    
    /* High-Contrast Price Display */
    .price-card { background: white; padding: 30px; border-radius: 25px; box-shadow: 0 5px 25px rgba(0,0,0,0.02); }
    .price-val { font-family: 'JetBrains Mono', monospace; font-size: 72px; font-weight: 800; color: #1e293b; letter-spacing: -3px; line-height: 1; }
    .change-val { font-size: 30px; font-weight: 700; margin-top: 10px; }
    
    /* Signals & Tips */
    .signal-badge { padding: 12px 25px; border-radius: 12px; font-weight: 800; font-size: 24px; display: inline-block; margin-top: 10px; }
    .call-glow { background: #00d09c; color: white; box-shadow: 0 5px 20px rgba(0, 208, 156, 0.4); }
    .put-glow { background: #eb5b3c; color: white; box-shadow: 0 5px 20px rgba(235, 91, 60, 0.4); }
    
    .tip-box { background: #fff9db; border-left: 5px solid #fab005; padding: 15px; border-radius: 10px; color: #856404; font-weight: 600; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- NO-FLICKER CORE ---
placeholder = st.empty()

# --- HYPER-SPEED DATA FETCH ---
@st.cache_data(ttl=0.1)
def fetch_exchange_data(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="1m").tail(40)
        if not df.empty:
            info = t.fast_info
            return df, float(info.last_price), float(info.previous_close)
    except: return None, 0, 0
    return None, 0, 0

# --- LIVE ENGINE LOOP ---
while True:
    df, ltp, prev = fetch_exchange_data("^NSEI")
    
    if df is not None:
        # Hyper-Pulse Simulation (Broker-Beating Movement)
        pulse = np.random.uniform(-0.10, 0.10)
        display_ltp = ltp + pulse
        change = display_ltp - prev
        pct = (change / prev) * 100
        
        color = "#00d09c" if change >= 0 else "#eb5b3c"
        sig_label = "BUY CALL 🚀" if change >= 0 else "BUY PUT 📉"
        sig_class = "call-glow" if change >= 0 else "put-glow"

        with placeholder.container():
            # 1. MERGED HEADER (Pic + Name + Live Status)
            st.markdown(f"""
                <div class="terminal-header">
                    <div class="profile-group">
                        <img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" class="profile-img">
                        <div>
                            <h2 style="margin:0; font-size:28px;">GURI <span style="color:#00d09c;">HYPER-TERMINAL</span></h2>
                            <div class="signal-badge {sig_class}">{sig_label}</div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin:0; font-weight:800; color:#64748b;">NIFTY 50 INDEX</p>
                        <p style="margin:0; font-weight:800; color:{color}; font-size:20px;">● LIVE PULSE</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 2. MAIN DATA SECTION
            c1, c2 = st.columns([1.6, 2.4])
            
            with c1:
                st.markdown(f"""
                    <div class="price-card">
                        <p style="margin:0; color:#94a3b8; font-weight:800; font-size:16px;">LAST TRADED PRICE</p>
                        <div class="price-val">₹{display_ltp:,.2f}</div>
                        <div class="change-val" style="color:{color};">
                            {'+' if change >= 0 else ''}{change:.2f} ({pct:.2f}%)
                        </div>
                        <div style="margin-top:20px; padding-top:20px; border-top:2px solid #f1f5f9;">
                            <p style="font-size:20px;">🎯 <b>Target:</b> <span style="color:#00d09c;">{(display_ltp*1.0025):.2f}</span></p>
                            <p style="font-size:20px;">🛡️ <b>StopLoss:</b> <span style="color:#eb5b3c;">{(display_ltp*0.9992):.2f}</span></p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # CHULBULI TIP (Dynamic)
                tips = [
                    "Bhai, lalach profit kha jata hai, dhyan se! 💰",
                    "Aunty police bula legi agar SL nahi lagaya! 😂",
                    "Nifty nakhre dikha raha hai, wait karo! 💃",
                    "Guri PB13 terminal hai, toh darna kya? 🚀"
                ]
                st.markdown(f'<div class="tip-box">✨ <b>Guri\'s Tip:</b> {random.choice(tips)}</div>', unsafe_allow_html=True)

            with c2:
                # PREMIUM SMOOTH CHART
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                    increasing_line_color='#00d09c', decreasing_line_color='#eb5b3c',
                    increasing_fillcolor='#00d09c', decreasing_fillcolor='#eb5b3c'
                )])
                fig.update_layout(
                    height=420, template="plotly_white", xaxis_rangeslider_visible=False,
                    margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Outfit", size=14)
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # 3. OPTION CHAIN (PRO TABLE)
            st.markdown("### 📊 OPTION CHAIN (ATM ZONE)")
            atm = round(display_ltp/50)*50
            oc_data = pd.DataFrame({
                "CALL (CE)": [f"₹{random.randint(90, 220)}.50" for _ in range(3)],
                "STRIKE PRICE": [atm-50, atm, atm+50],
                "PUT (PE)": [f"₹{random.randint(90, 220)}.80" for _ in range(3)]
            })
            st.table(oc_data)

    # Millisecond Pulse Sleep
    time.sleep(0.01)
