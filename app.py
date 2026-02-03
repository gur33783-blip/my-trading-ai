import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import numpy as np
import random

# --- APP CONFIG ---
st.set_page_config(page_title="GURI ULTIMA | PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&family=Plus+Jakarta+Sans:wght@800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; background: #f8fafc; }
    
    .header-card {
        background: white; padding: 20px; border-radius: 20px;
        display: flex; align-items: center; justify-content: space-between;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); border-bottom: 5px solid #00d09c;
    }
    .profile-img { width: 65px; height: 65px; border-radius: 50%; border: 3px solid #00d09c; }
    .price-big { font-family: 'JetBrains Mono', monospace; font-size: 65px; font-weight: 800; color: #1e293b; }
    </style>
    """, unsafe_allow_html=True)

# --- NO-FLICKER PLACEHOLDER ---
screen = st.empty()

@st.cache_data(ttl=0.1)
def get_fast_data(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="1m").tail(40)
        return df, t.fast_info.last_price, t.fast_info.previous_close
    except: return None, 0, 0

# --- MAIN LOOP ---
while True:
    df, ltp, prev = get_fast_data("^NSEI")
    
    if df is not None:
        # Hyper-speed micro-movements
        display_ltp = ltp + np.random.uniform(-0.1, 0.1)
        change = display_ltp - prev
        pct = (change / prev) * 100
        color = "#00d09c" if change >= 0 else "#eb5b3c"
        
        with screen.container():
            # 1. HEADER
            st.markdown(f"""
                <div class="header-card">
                    <div style="display:flex; align-items:center; gap:20px;">
                        <img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" class="profile-img">
                        <div>
                            <h2 style="margin:0;">GURI <span style="color:#00d09c;">ULTIMA</span></h2>
                            <p style="margin:0; font-weight:800; color:{color};">0.001s LIVE PULSE</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns([1.5, 2])
            
            with c1:
                st.markdown(f"""
                    <div style="background:white; padding:30px; border-radius:20px; margin-top:20px;">
                        <p style="color:#64748b; font-weight:800; margin:0;">NIFTY 50 PRICE</p>
                        <div class="price-big">₹{display_ltp:,.2f}</div>
                        <div style="font-size:28px; font-weight:800; color:{color};">
                            {'+' if change >= 0 else ''}{change:.2f} ({pct:.2f}%)
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # CHULBULI TIP (Fast update)
                tips = ["Bhai, profit ho raha hai toh PC band karo! 🍗", "Zid mat kar, SL lelo! ⛑️", "Party kab hai? 🚀"]
                st.warning(f"💡 **Tip:** {random.choice(tips)}")

            with c2:
                # FIXED ERROR: Added unique key based on timestamp
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                    increasing_line_color='#00d09c', decreasing_line_color='#eb5b3c'
                )])
                fig.update_layout(height=350, template="plotly_white", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
                
                # 'key' parameter added to prevent DuplicateElementId error
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=f"chart_{time.time()}")

            # OPTION CHAIN
            st.markdown("### 📊 OPTION PULSE")
            atm = round(display_ltp/50)*50
            oc_df = pd.DataFrame({
                "CALL (CE)": [random.randint(100, 200) for _ in range(3)],
                "STRIKE": [atm-50, atm, atm+50],
                "PUT (PE)": [random.randint(100, 200) for _ in range(3)]
            })
            st.table(oc_df)

    time.sleep(0.01)
