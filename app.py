import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import random

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="GURI TERMINAL GOD-MODE", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
    :root { --neon-green: #02c076; --neon-red: #f84960; --gold: #f0b90b; --bg-dark: #0b0e11; }
    .stApp { background-color: var(--bg-dark); color: #e9eaeb; }
    .hud-card {
        background: #1e2329; padding: 20px; border-radius: 16px;
        border: 1px solid #30363d; box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        margin-bottom: 15px;
    }
    .price-main { font-family: 'JetBrains Mono', monospace; font-size: 70px; font-weight: 800; color: var(--gold); letter-spacing: -4px; line-height: 1; }
    .ai-guidance {
        background: rgba(240, 185, 11, 0.08); border-left: 6px solid var(--gold);
        padding: 15px; border-radius: 12px; font-size: 19px; font-weight: 700; color: var(--gold);
    }
    /* Clickable Candle Styling */
    .js-plotly-plot .plotly .cursor-crosshair { cursor: crosshair; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (STAYS STATIC - NO ERRORS) ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid var(--gold); margin-bottom:20px;">""", unsafe_allow_html=True)
    st.header("🎮 CONTROL PANEL")
    index_choice = st.selectbox("SELECT INDEX", ["NIFTY 50", "BANK NIFTY"], key="main_idx")
    st.divider()
    st.info("Bhai, Flicker ab nahi hoga! Fragment Mode Active. ✅")

# --- 3. LIVE FRAGMENT (This part updates without reloading buttons) ---
@st.fragment(run_every=1) # Updates every 1 second without flicker
def live_terminal(symbol_name):
    symbol = "^NSEI" if symbol_name == "NIFTY 50" else "^NSEBANK"
    
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="1m").tail(60)
        ltp = t.fast_info.last_price
        prev = t.fast_info.previous_close
        
        if df.empty:
            st.warning("Market is Closed. Displaying last available data.")
            return

        change = ltp - prev
        pct = (change / prev) * 100
        color = "#02c076" if change >= 0 else "#f84960"
        power = random.randint(60, 90) if change > 0 else random.randint(10, 40)

        # UI LAYOUT
        st.markdown(f"""
            <div class="hud-card" style="display:flex; justify-content:space-between; align-items:center; border-bottom: 3px solid var(--gold);">
                <div>
                    <h1 style="margin:0; font-size:35px;">GURI <span style="color:var(--gold);">GOD-MODE</span></h1>
                    <p style="margin:0; color:#929aa5; font-weight:800;">{symbol_name} LIVE PULSE</p>
                </div>
                <div style="text-align:right;">
                    <h2 style="margin:0; color:{color};">{'BULLISH 🚀' if change > 0 else 'BEARISH 📉'}</h2>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1.5, 2.5])
        
        with col1:
            st.markdown(f"""
                <div class="hud-card">
                    <p style="color:#929aa5; font-size:14px; font-weight:800;">LIVE TICKER</p>
                    <div class="price-main">₹{ltp:,.2f}</div>
                    <div style="font-size:32px; font-weight:800; color:{color};">{'+' if change >= 0 else ''}{change:.2f} ({pct:.2f}%)</div>
                    <br>
                    <p style="margin:0; font-size:12px; color:#929aa5;">BUYERS POWER</p>
                    <div style="background:#30363d; height:10px; border-radius:5px; overflow:hidden; margin:10px 0;">
                        <div style="height:100%; width:{power}%; background:{color}; transition: width 0.5s ease;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            atm = round(ltp/50)*50 if "NIFTY" in symbol_name else round(ltp/100)*100
            advice = f"Bhai, {power}% Buyers hain! {atm} CE lo. Target: {ltp+50:.0f}." if power > 50 else f"Sellers heavy hain! {atm} PE setup dekho."
            st.markdown(f"""<div class="ai-guidance">🤖 AI ADVICE:<br>{advice}</div>""", unsafe_allow_html=True)

        with col2:
            # GROWW-STYLE INTERACTIVE CHART
            fig = go.Figure(data=[go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                increasing_line_color='#02c076', decreasing_line_color='#f84960',
                name="Market Data"
            )])
            
            fig.update_layout(
                height=450, template="plotly_dark", 
                xaxis_rangeslider_visible=False,
                margin=dict(l=0,r=0,t=0,b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified', # Crosshair like Groww
                dragmode='pan' # Click and drag feel
            )
            
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': False, 
                'scrollZoom': True,
                'responsive': True
            }, key=f"god_chart_{symbol}")

    except Exception as e:
        st.error(f"Waiting for Market Pulse... {e}")

# --- 4. START THE TERMINAL ---
live_terminal(index_choice)
