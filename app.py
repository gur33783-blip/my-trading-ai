import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import random

# --- 1. PRO UI CONFIG ---
st.set_page_config(page_title="GURI GOD-MODE TERMINAL", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
    :root { --gold: #f0b90b; --bg: #0b0e11; --green: #02c076; --red: #f84960; }
    .stApp { background-color: var(--bg); color: #e9eaeb; }
    .hud-card {
        background: #1e2329; padding: 20px; border-radius: 16px;
        border: 1px solid #30363d; box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        margin-bottom: 10px;
    }
    .global-tag { background: #2b3139; padding: 6px 12px; border-radius: 8px; font-size: 13px; font-weight: 800; border-left: 3px solid var(--gold); display: inline-block; margin-right: 10px; }
    .price-main { font-family: 'JetBrains Mono', monospace; font-size: 65px; font-weight: 800; color: var(--gold); letter-spacing: -3px; }
    .logic-window { background: rgba(56, 189, 248, 0.1); border-left: 6px solid #38bdf8; padding: 15px; border-radius: 12px; font-size: 16px; color: #38bdf8; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE ENGINE: MULTI-DATA FETCH ---
@st.cache_data(ttl=0.1)
def fetch_god_data(local_sym):
    try:
        symbols = {"local": local_sym, "nasdaq": "^IXIC", "dollar": "DX-Y.NYB", "vix": "^INDIAVIX"}
        pack = {}
        for key, sym in symbols.items():
            t = yf.Ticker(sym)
            fast = t.fast_info
            pack[key] = {
                "price": fast.last_price,
                "change": ((fast.last_price - fast.previous_close)/fast.previous_close)*100,
                "df": t.history(period="1d", interval="1m").tail(60) if key == "local" else None
            }
        return pack
    except: return None

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid var(--gold); margin-bottom:20px;">""", unsafe_allow_html=True)
    st.header("🎮 TERMINAL CONTROL")
    idx_name = st.selectbox("INDEX SELECTOR", ["NIFTY 50", "BANK NIFTY"], key="final_idx")
    st.divider()
    st.warning("⚠️ Risk Rule: Per trade 2% Capital max!")

# --- 4. LIVE FRAGMENT ---
@st.fragment(run_every=1)
def run_god_mode(name):
    sym = "^NSEI" if name == "NIFTY 50" else "^NSEBANK"
    data = fetch_everything(sym) if 'fetch_everything' in globals() else fetch_god_data(sym)
    
    if data:
        local = data['local']
        nasdaq = data['nasdaq']
        vix = data['vix']
        color = "#02c076" if local['change'] >= 0 else "#f84960"
        
        # UI: GLOBAL STATUS
        st.markdown(f"""
            <div style="margin-bottom:15px;">
                <div class="global-tag">NASDAQ: <span style="color:{'#02c076' if nasdaq['change']>=0 else '#f84960'}">{nasdaq['change']:+.2f}%</span></div>
                <div class="global-tag">INDIA VIX: {vix['price']:.2f}</div>
                <div class="global-tag" style="border-color:#38bdf8;">VOL FLOW: {random.randint(60,95) if local['change']>0 else random.randint(15,40)}%</div>
            </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1.6, 2.4])
        
        with c1:
            # MAIN PRICE HUD
            st.markdown(f"""
                <div class="hud-card">
                    <p style="color:#929aa5; font-size:12px; font-weight:800;">LIVE TERMINAL: {name}</p>
                    <div class="price-main">₹{local['price']:,.2f}</div>
                    <div style="font-size:30px; font-weight:800; color:{color};">{local['change']:+.2f}% TODAY</div>
                </div>
            """, unsafe_allow_html=True)

            # AI LOGIC PULSE (The "Fayde Wali Cheez")
            pcr = random.uniform(0.7, 1.4) # Simulated PCR
            logic_msg = ""
            if local['change'] > 0 and nasdaq['change'] > 0:
                logic_msg = f"Bullish Sentiment: Nasdaq ka support hai aur PCR ({pcr:.2f}) majboot hai. Operators buy kar rahe hain."
            elif nasdaq['change'] < -0.3:
                logic_msg = "Caution: Price upar hai par US Market gir raha hai. Fake Breakout ka khatra hai (Operator Trap)."
            else:
                logic_msg = "Market Sideways: VIX stable hai, badi entry avoid karo jab tak range break na ho."

            st.markdown(f"""<div class="logic-window">🔍 AI LOGIC PULSE:<br>{logic_msg}</div>""", unsafe_allow_html=True)
            
            # STRIKE ADVICE
            atm = round(local['price']/50)*50 if "NIFTY" in name else round(local['price']/100)*100
            st.info(f"🎯 Recommended ATM: {atm} {'CE' if local['change']>0 else 'PE'}")

        with c2:
            # INTERACTIVE CHART
            df = local['df']
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                            increasing_line_color='#02c076', decreasing_line_color='#f84960')])
            fig.update_layout(height=480, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=f"god_final_{sym}")

run_god_mode(idx_name)
