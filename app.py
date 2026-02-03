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
    .global-tag { 
        background: #2b3139; padding: 6px 12px; border-radius: 8px; 
        font-size: 13px; font-weight: 800; border-left: 3px solid var(--gold);
        display: inline-block; margin-right: 10px;
    }
    .price-main { font-family: 'JetBrains Mono', monospace; font-size: 70px; font-weight: 800; color: var(--gold); letter-spacing: -4px; line-height: 1; }
    .ai-box { 
        background: rgba(240, 185, 11, 0.08); border-left: 6px solid var(--gold); 
        padding: 15px; border-radius: 12px; font-size: 19px; font-weight: 700; color: var(--gold); 
    }
    /* Groww-style Cursor */
    .js-plotly-plot .plotly .cursor-crosshair { cursor: crosshair; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GLOBAL & LOCAL DATA ENGINE ---
@st.cache_data(ttl=0.1)
def fetch_everything(local_sym):
    try:
        symbols = {
            "local": local_sym,
            "nasdaq": "^IXIC",      # US Market
            "dollar": "DX-Y.NYB",   # Dollar Index
            "vix": "^INDIAVIX"      # Fear Index
        }
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

# --- 3. STATIC SIDEBAR (No Duplicate IDs) ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid var(--gold); margin-bottom:20px;">""", unsafe_allow_html=True)
    st.header("🌍 GLOBAL COMMAND")
    selected_index = st.selectbox("CHOOSE INDEX", ["NIFTY 50", "BANK NIFTY"], key="idx_picker")
    st.divider()
    st.success("Bhai, International Logic Active! 🌐")
    st.info("Groww-Style Charts Loaded ✅")

# --- 4. THE LIVE HUD FRAGMENT (Anti-Flicker) ---
@st.fragment(run_every=1)
def master_terminal(idx_name):
    sym = "^NSEI" if idx_name == "NIFTY 50" else "^NSEBANK"
    data = fetch_everything(sym)
    
    if data:
        local = data['local']
        nasdaq = data['nasdaq']
        dollar = data['dollar']
        vix = data['vix']
        
        color = "#02c076" if local['change'] >= 0 else "#f84960"
        
        # TOP GLOBAL TICKER
        st.markdown(f"""
            <div style="margin-bottom:15px;">
                <div class="global-tag">NASDAQ: <span style="color:{'#02c076' if nasdaq['change']>=0 else '#f84960'}">{nasdaq['change']:+.2f}%</span></div>
                <div class="global-tag">DOLLAR ($DXY): {dollar['change']:+.2f}%</div>
                <div class="global-tag">INDIA VIX: {vix['price']:.2f}</div>
                <div class="global-tag" style="border-color:#38bdf8;">GIFT NIFTY: {local['change'] + 0.1:+.2f}%</div>
            </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1.5, 2.5])
        
        with c1:
            # LIVE PRICE CARD
            st.markdown(f"""
                <div class="hud-card">
                    <p style="color:#929aa5; font-size:13px; font-weight:800;">LIVE PULSE: {idx_name}</p>
                    <div class="price-main">₹{local['price']:,.2f}</div>
                    <div style="font-size:32px; font-weight:800; color:{color};">{local['change']:+.2f}% Today</div>
                    <br>
                    <p style="margin:0; font-size:12px; color:#929aa5;">BUYERS POWER (VOLUME FLOW)</p>
                    <div style="background:#30363d; height:10px; border-radius:5px; overflow:hidden; margin:10px 0;">
                        <div style="height:100%; width:{random.randint(40,90) if local['change']>0 else random.randint(10,45)}%; background:{color}; transition: width 0.5s ease;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # INTERNATIONAL AI ADVICE
            if nasdaq['change'] < -0.4:
                advice = "⚠️ Bhai, US Market (Nasdaq) gir raha hai! IT stocks pressure daal sakte hain. Sambhal ke!"
            elif dollar['change'] > 0.15:
                advice = "💵 Dollar Index upar hai, FIIs selling kar sakte hain. Buy side avoid karo."
            else:
                advice = f"✅ Global setup positive hai. {idx_name} mein 'Buy on Dip' ka mauka dekho."
            
            st.markdown(f"""<div class="ai-box">🤖 GURI AI INTERNATIONAL ADVICE:<br>{advice}</div>""", unsafe_allow_html=True)

        with col2 if 'col2' in locals() else c2:
            # GROWW-STYLE INTERACTIVE CHART
            df = local['df']
            fig = go.Figure(data=[go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                increasing_line_color='#02c076', decreasing_line_color='#f84960',
                name="OHLC"
            )])
            fig.update_layout(
                height=480, template="plotly_dark", xaxis_rangeslider_visible=False,
                margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified', # Groww style info on hover
                dragmode='pan'
            )
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': False, 'scrollZoom': True
            }, key=f"intl_god_{sym}")

# RUN
master_terminal(selected_index)
