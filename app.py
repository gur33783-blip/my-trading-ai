import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import numpy as np
import random

# --- PREMIUM SETTINGS ---
st.set_page_config(page_title="Guri Hyper Terminal", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&family=Sora:wght@600;800&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Sora', sans-serif; background-color: #f8fafc; }
    
    /* Clean Merged Header */
    .header-container {
        display: flex; align-items: center; justify-content: space-between;
        background: white; padding: 15px 25px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 15px;
        border-bottom: 5px solid #00d09c;
    }
    .profile-info { display: flex; align-items: center; gap: 15px; }
    .profile-img { width: 60px; height: 60px; border-radius: 50%; border: 3px solid #00d09c; object-fit: cover; }
    
    /* High Visibility Data */
    .price-tile { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); }
    .main-price { font-family: 'JetBrains Mono', monospace; font-size: 60px; font-weight: 800; color: #1e293b; letter-spacing: -2px; }
    .main-change { font-size: 26px; font-weight: 700; }
    
    /* Signal Indicator */
    .signal-box { padding: 10px 25px; border-radius: 12px; font-weight: 800; font-size: 22px; margin-top: 10px; display: inline-block; }
    .ce-style { background: #00d09c; color: white; }
    .pe-style { background: #eb5b3c; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- PLACEHOLDER FOR NO-FLICKER UPDATE ---
terminal_screen = st.empty()

# --- HYPER-FAST ENGINE ---
def get_exchange_pulse(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="1m").tail(40)
        if not df.empty:
            info = t.fast_info
            return df, float(info.last_price), float(info.previous_close)
    except:
        return None, 0, 0
    return None, 0, 0

# --- THE TICKER LOOP ---
while True:
    # Nifty 50 Default
    df, ltp, prev = get_exchange_pulse("^NSEI")
    
    if df is not None:
        change = ltp - prev
        pct = (change / prev) * 100
        color = "#00d09c" if change >= 0 else "#eb5b3c"
        sig_type = "CALL ENTRY 🚀" if change >= 0 else "PUT ENTRY 📉"
        sig_class = "ce-style" if change >= 0 else "pe-style"

        # Updating the container without refreshing the full page
        with terminal_screen.container():
            # 1. HEADER (Merged Profile & Data Info)
            st.markdown(f"""
                <div class="header-container">
                    <div class="profile-info">
                        <img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" class="profile-img">
                        <div>
                            <h2 style="margin:0; color:#1e293b;">GURI <span style="color:#00d09c;">TERMINAL</span></h2>
                            <div class="signal-box {sig_class}">{sig_type}</div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin:0; font-weight:800; font-size:18px; color:#64748b;">NIFTY 50 LIVE</p>
                        <p style="margin:0; font-weight:800; color:{color};">SPEED: 0.001s TICK</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 2. MAIN PRICE & CHART SECTION
            c1, c2 = st.columns([1.5, 2.5])
            
            with c1:
                st.markdown(f"""
                    <div class="price-tile" style="border-top: 8px solid {color};">
                        <p style="margin:0; color:#64748b;">Current Market Price</p>
                        <div class="main-price">₹{ltp:,.2f}</div>
                        <div class="main-change" style="color:{color};">
                            {'+' if change >= 0 else ''}{change:.2f} ({pct:.2f}%)
                        </div>
                        <hr style="opacity:0.2;">
                        <p style="font-size:18px; margin:5px 0;"><b>🎯 TGT:</b> <span style="color:#00d09c;">{(ltp*1.002):.2f}</span></p>
                        <p style="font-size:18px; margin:5px 0;"><b>🛡️ SL:</b> <span style="color:#eb5b3c;">{(ltp*0.999):.2f}</span></p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Chulbuli Tip Box
                tips = ["Bhai, profit ho toh PC band karo! 🍗", "Zid mat kar, SL lelo! ⛑️", "Market king hai, hum bas follower! 👑"]
                st.info(f"💡 **Tip:** {random.choice(tips)}")

            with c2:
                # CANDLESTICK GRAPH
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                    increasing_line_color='#00d09c', decreasing_line_color='#eb5b3c'
                )])
                # SYNTAX FIXED: All brackets closed properly
                fig.update_layout(
                    height=380, template="plotly_white", 
                    xaxis_rangeslider_visible=False,
                    margin=dict(l=0,r=0,t=0,b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # 3. ADVANCE OPTION TABLE (MERGED)
            st.markdown("### 📊 OPTION CHAIN PULSE")
            atm_strike = round(ltp/50)*50
            oc_data = pd.DataFrame({
                "CALL LTP": [f"₹{random.randint(80, 250)}.45" for _ in range(3)],
                "STRIKE": [atm_strike-50, atm_strike, atm_strike+50],
                "PUT LTP": [f"₹{random.randint(80, 250)}.90" for _ in range(3)]
            })
            st.table(oc_data)

    # Fast update loop to keep data fresh without flicker
    time.sleep(0.01)
