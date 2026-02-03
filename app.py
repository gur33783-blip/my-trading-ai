import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import random

# --- 1. HIGH-PROFESSIONAL UI CONFIG ---
st.set_page_config(page_title="GURI AI ALPHA", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@800&display=swap');
    
    /* Overall Background */
    .stApp { background-color: #f0f2f5; }
    
    /* Main Card Styling */
    .premium-card {
        background: #ffffff;
        padding: 25px;
        border-radius: 24px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.04);
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Ultra-Visible Fonts */
    .header-text { font-family: 'Inter', sans-serif; font-weight: 900; color: #1e293b; font-size: 34px; letter-spacing: -1px; }
    .price-val { font-family: 'JetBrains Mono', monospace; font-size: 72px; font-weight: 800; color: #0f172a; letter-spacing: -4px; line-height: 1; }
    .label-text { font-family: 'Inter', sans-serif; font-weight: 700; color: #64748b; text-transform: uppercase; font-size: 14px; letter-spacing: 1px; }
    
    /* Neon Signal Buttons */
    .buy-btn { background: #10b981; color: white; padding: 12px 24px; border-radius: 12px; font-weight: 900; font-size: 20px; display: inline-block; box-shadow: 0 4px 15px rgba(16,185,129,0.3); }
    .sell-btn { background: #ef4444; color: white; padding: 12px 24px; border-radius: 12px; font-weight: 900; font-size: 20px; display: inline-block; box-shadow: 0 4px 15px rgba(239,68,68,0.3); }
    
    /* Hindi Advice Box */
    .advice-box {
        background: #1e293b;
        color: #f8fafc;
        padding: 20px;
        border-radius: 18px;
        border-left: 8px solid #38bdf8;
        font-size: 20px;
        line-height: 1.6;
        font-weight: 600;
    }
    
    /* Profile Image Glow */
    .p-img { width: 80px; height: 80px; border-radius: 50%; border: 4px solid #00d09c; box-shadow: 0 0 20px rgba(0,208,156,0.2); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FAST DATA ENGINE ---
def get_live_pulse():
    try:
        ticker = yf.Ticker("^NSEI")
        df = ticker.history(period="1d", interval="1m").tail(45)
        if df.empty: return None, 0, 0
        ltp = float(ticker.fast_info.last_price)
        prev = float(ticker.fast_info.previous_close)
        return df, ltp, prev
    except:
        return None, 0, 0

# --- 3. THE LIVE SCREEN ---
placeholder = st.empty()

while True:
    df, ltp, prev = get_live_pulse()
    
    with placeholder.container():
        if df is not None:
            change = ltp - prev
            pct = (change / prev) * 100
            color = "#10b981" if change >= 0 else "#ef4444"
            btn_html = f'<div class="buy-btn">🚀 BUY CALL</div>' if change >= 0 else f'<div class="sell-btn">📉 BUY PUT</div>'
            
            # --- HEADER ---
            st.markdown(f"""
                <div class="premium-card" style="display:flex; align-items:center; justify-content:space-between; padding:15px 35px;">
                    <div style="display:flex; align-items:center; gap:20px;">
                        <img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" class="p-img">
                        <div>
                            <div class="header-text">GURI <span style="color:#00d09c;">ALPHA AI</span></div>
                            <div style="color:#64748b; font-weight:700;">INSTITUTIONAL GRADE TERMINAL</div>
                        </div>
                    </div>
                    <div>{btn_html}</div>
                </div>
            """, unsafe_allow_html=True)

            # --- MAIN GRID ---
            c1, c2 = st.columns([1.4, 2.6])
            
            with c1:
                st.markdown(f"""
                    <div class="premium-card">
                        <div class="label-text">Live Market Price</div>
                        <div class="price-val">₹{ltp:,.2f}</div>
                        <div style="font-size:32px; font-weight:800; color:{color}; margin-top:10px;">
                            {'+' if change >= 0 else ''}{change:.2f} ({pct:.2f}%)
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # HINDI AI GUIDANCE
                atm_strike = round(ltp/50)*50
                if change > 0:
                    advice_msg = f"Bhai, Nifty majboot hai! {atm_strike} CE par dhyan do. Target: {ltp+40:.0f}"
                else:
                    advice_msg = f"Market mein girawat hai! {atm_strike} PE setup ban raha hai. SL sakht rakho."
                
                st.markdown(f"""
                    <div class="advice-box">
                        <span style="color:#38bdf8; font-size:14px; text-transform:uppercase;">🤖 AI Predictor Alert</span><br>
                        {advice_msg}
                    </div>
                """, unsafe_allow_html=True)

            with c2:
                # CANDLESTICK GRAPH (SHARP LOOK)
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                    increasing_line_color='#10b981', decreasing_line_color='#ef4444',
                    increasing_fillcolor='#10b981', decreasing_fillcolor='#ef4444'
                )])
                fig.update_layout(
                    height=450, template="plotly_white", 
                    xaxis_rangeslider_visible=False, 
                    margin=dict(l=0,r=0,t=0,b=0),
                    font=dict(family="Inter", size=12)
                )
                st.plotly_chart(fig, use_container_width=True, key=f"v16_{time.time()}")

            # --- FOOTER METRICS ---
            st.markdown("### 📊 Market Depth Simulation")
            mc1, mc2, mc3 = st.columns(3)
            mc1.metric("VOLATILITY", "HIGH" if abs(pct) > 0.8 else "NORMAL")
            mc2.metric("TREND", "BULLISH" if change > 0 else "BEARISH")
            mc3.metric("STRIKE FOCUS", f"{atm_strike}")

        else:
            st.error("Market Data Offline. Trading Hours: 9:15 AM - 3:30 PM")

    time.sleep(0.5)
