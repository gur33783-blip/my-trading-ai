import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import numpy as np
import random

# --- GURI PREMIUM INTERFACE CONFIG ---
st.set_page_config(page_title="GURI AI ALPHA", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@700;800&family=JetBrains+Mono:wght@700&display=swap');
    html, body, [class*="st-"] { font-family: 'Sora', sans-serif; background: #f1f5f9; }
    
    .main-header {
        display: flex; align-items: center; justify-content: space-between;
        background: white; padding: 20px 35px; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-bottom: 20px;
        border-left: 10px solid #00d09c;
    }
    .profile-img { width: 75px; height: 75px; border-radius: 50%; border: 4px solid #00d09c; object-fit: cover; }
    
    .signal-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.02); border: 2px solid #e2e8f0; }
    .price-text { font-family: 'JetBrains Mono', monospace; font-size: 60px; font-weight: 800; color: #1e293b; letter-spacing: -3px; }
    
    .hindi-alert { background: #fff9db; border-left: 6px solid #fab005; padding: 15px; border-radius: 12px; font-size: 18px; font-weight: 700; color: #856404; }
    .buy-zone { background: #ecfdf5; border-left: 6px solid #10b981; color: #065f46; padding: 15px; border-radius: 12px; font-weight: 800; }
    .sell-zone { background: #fef2f2; border-left: 6px solid #ef4444; color: #991b1b; padding: 15px; border-radius: 12px; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# --- THE ENGINE: ANALYSIS & SIGNALS ---
def get_alpha_signals(df):
    # Logic: EMA Cross + RSI Sentiment
    df['EMA9'] = df['Close'].ewm(span=9).mean()
    df['EMA21'] = df['Close'].ewm(span=21).mean()
    last_close = df['Close'].iloc[-1]
    
    # Simple Signal Logic
    if df['EMA9'].iloc[-1] > df['EMA21'].iloc[-1]:
        return "BUY", "Call lelo bhai, trend upar hai!", "#10b981"
    else:
        return "SELL", "Put ka setup ban raha hai, neeche ja sakta hai!", "#ef4444"

# --- NO-FLICKER CONTAINER ---
app_view = st.empty()

while True:
    try:
        # Fetching Data
        ticker = yf.Ticker("^NSEI")
        df = ticker.history(period="1d", interval="1m").tail(50)
        ltp = ticker.fast_info.last_price
        prev_close = ticker.fast_info.previous_close
        
        if not df.empty:
            sig_type, hindi_msg, sig_color = get_alpha_signals(df)
            change = ltp - prev_close
            pct = (change / prev_close) * 100
            
            with app_view.container():
                # 1. PREMIUM HEADER
                st.markdown(f"""
                    <div class="main-header">
                        <div style="display:flex; align-items:center; gap:20px;">
                            <img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" class="profile-img">
                            <div>
                                <h1 style="margin:0; font-size:35px;">GURI <span style="color:#00d09c;">ALPHA AI</span></h1>
                                <p style="margin:0; color:#64748b; font-weight:800;">LIVE ANALYSIS MODE ON</p>
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <p style="margin:0; font-weight:800; color:#94a3b8;">NIFTY 50 INDEX</p>
                            <h2 style="margin:0; color:{sig_color};">{sig_type} SIGNAL</h2>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # 2. MAIN HUB (Price + Chart + AI Guidance)
                c1, c2 = st.columns([1.5, 2.5])
                
                with c1:
                    st.markdown(f"""
                        <div class="signal-card">
                            <p style="margin:0; color:#94a3b8; font-weight:800;">LIVE PRICE</p>
                            <div class="price-text">₹{ltp:,.2f}</div>
                            <div style="font-size:24px; font-weight:800; color:{sig_color};">
                                {'+' if change >= 0 else ''}{change:.2f} ({pct:.2f}%)
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # AI HINDI ADVICE CARD
                    zone_style = "buy-zone" if sig_type == "BUY" else "sell-zone"
                    st.markdown(f"""
                        <div class="{zone_style}">
                            <h3 style="margin:0;">🤖 Guri AI Advice:</h3>
                            <p style="font-size:20px; margin:10px 0;">{hindi_msg}</p>
                            <hr>
                            <p><b>Capital:</b> 30% Use Karo<br>
                            <b>Target:</b> {ltp + (35 if sig_type == "BUY" else -35):.2f}<br>
                            <b>Strike:</b> {round(ltp/50)*50} {'CE' if sig_type == "BUY" else 'PE'}</p>
                        </div>
                    """, unsafe_allow_html=True)

                with c2:
                    # LIVE PROFESSIONAL CHART
                    fig = go.Figure(data=[go.Candlestick(
                        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                        increasing_line_color='#10b981', decreasing_line_color='#ef4444'
                    )])
                    fig.update_layout(height=450, template="plotly_white", xaxis_rangeslider_visible=False,
                                      margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=f"alpha_{time.time()}")

                # 3. SENTIMENT METER (Simplified)
                st.markdown("### 🔍 Market Sentiment Analysis")
                cols = st.columns(3)
                cols[0].metric("Market Mood", "Fearful" if pct < -0.5 else "Greedy" if pct > 0.5 else "Neutral")
                cols[1].metric("Volatility", "High" if abs(pct) > 1 else "Normal")
                cols[2].metric("Trend", "Upward" if sig_type == "BUY" else "Downward")

        time.sleep(0.5) # Fast Update
    except Exception as e:
        time.sleep(2)
        continue
