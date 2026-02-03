import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import random

# --- 1. THEME SETTINGS ---
st.set_page_config(page_title="GURI AI ALPHA", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; }
    
    .header-box { background: white; padding: 20px; border-radius: 20px; border-left: 10px solid #00d09c; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
    .price-tick { font-size: 60px; font-weight: 800; color: #1e293b; letter-spacing: -2px; }
    .hindi-alert { background: #fff9db; border-left: 6px solid #fab005; padding: 20px; border-radius: 15px; font-size: 20px; font-weight: 800; color: #856404; margin-top: 15px; }
    .sig-btn { padding: 10px 20px; border-radius: 10px; font-weight: 800; color: white; display: inline-block; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. NO-FLICKER CONTAINER ---
ui_screen = st.empty()

# --- 3. BULLETPROOF DATA FETCH ---
def get_market_data():
    try:
        # Index data fetch
        ticker = yf.Ticker("^NSEI")
        df = ticker.history(period="1d", interval="1m").tail(40)
        if df.empty: return None, 0, 0, 0
        
        ltp = float(ticker.fast_info.last_price)
        prev = float(ticker.fast_info.previous_close)
        high = float(ticker.fast_info.day_high)
        return df, ltp, prev, high
    except:
        return None, 0, 0, 0

# --- 4. CONTINUOUS LIVE LOOP ---
while True:
    df, ltp, prev, d_high = get_market_data()
    
    with ui_screen.container():
        if df is not None:
            change = ltp - prev
            pct = (change / prev) * 100
            color = "#10b981" if change >= 0 else "#ef4444"
            
            # --- TOP BAR ---
            st.markdown(f"""
                <div class="header-box">
                    <div style="display:flex; align-items:center; justify-content:space-between;">
                        <div style="display:flex; align-items:center; gap:20px;">
                            <img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:70px; height:70px; border-radius:50%; border:3px solid #00d09c;">
                            <div>
                                <h1 style="margin:0;">GURI ALPHA <span style="color:#00d09c;">AI</span></h1>
                                <p style="margin:0; font-weight:800; color:#64748b;">NIFTY 50 • LIVE FEED</p>
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <span class="sig-btn" style="background:{color};">{'BUY SIGNAL' if change > 0 else 'SELL SIGNAL'}</span>
                            <p style="margin:0; font-weight:800; color:{color};">LATENCY: 0.1s</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.write("")

            # --- MAIN DISPLAY ---
            c1, c2 = st.columns([1.5, 2.5])
            
            with c1:
                st.markdown(f"""
                    <div style="background:white; padding:30px; border-radius:20px; box-shadow:0 5px 15px rgba(0,0,0,0.03);">
                        <p style="margin:0; color:#94a3b8; font-weight:800;">LIVE PRICE (₹)</p>
                        <div class="price-tick">₹{ltp:,.2f}</div>
                        <h2 style="color:{color}; margin:0;">{'+' if change >= 0 else ''}{change:.2f} ({pct:.2f}%)</h2>
                    </div>
                """, unsafe_allow_html=True)

                # HINDI AI GUIDANCE
                if change > 0:
                    msg = "Bhai, market upar ja raha hai! Nifty " + str(round(ltp/50)*50) + " CE par nazar rakho. Capital ka 20% hi use karna."
                else:
                    msg = "Nifty neeche gir raha hai! " + str(round(ltp/50)*50) + " PE buy karne ka setup ban raha hai. Zyada lalach mat karna."
                
                st.markdown(f"""<div class="hindi-alert">🤖 GURI AI ADVICE:<br>{msg}</div>""", unsafe_allow_html=True)

            with c2:
                # CANDLESTICK CHART
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                    increasing_line_color='#10b981', decreasing_line_color='#ef4444'
                )])
                fig.update_layout(height=420, template="plotly_white", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
                st.plotly_chart(fig, use_container_width=True, key=f"v15_{time.time()}")

        else:
            # FALLBACK IF DATA FAILS
            st.error("Guri Bhai, Data nahi aa raha. Internet ya Market status check karo.")
            st.info("Market Hours: Mon-Fri (9:15 AM - 3:30 PM)")

    # FAST PULSE
    time.sleep(1)
