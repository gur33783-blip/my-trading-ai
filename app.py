import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import numpy as np
import random

# --- 1. GLOBAL TERMINAL SETTINGS ---
st.set_page_config(page_title="GURI TERMINAL GOD-MODE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
    
    :root { --neon-green: #02c076; --neon-red: #f84960; --gold: #f0b90b; --bg-dark: #0b0e11; }
    
    .stApp { background-color: var(--bg-dark); color: #e9eaeb; }
    
    /* Premium HUD Cards */
    .hud-card {
        background: #1e2329; padding: 20px; border-radius: 16px;
        border: 1px solid #30363d; box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        margin-bottom: 15px; position: relative;
    }
    
    .price-main { font-family: 'JetBrains Mono', monospace; font-size: 75px; font-weight: 800; color: var(--gold); letter-spacing: -4px; line-height: 1; }
    
    /* Multi-Index Badge */
    .index-badge { background: #2b3139; padding: 5px 15px; border-radius: 8px; font-weight: 800; font-size: 14px; color: #929aa5; }
    
    /* Panic & Power Meters */
    .meter-bg { background: #30363d; height: 10px; border-radius: 5px; overflow: hidden; margin: 10px 0; }
    .meter-fill { height: 100%; transition: width 0.5s ease; }
    
    /* Hindi AI Guidance */
    .ai-guidance {
        background: rgba(240, 185, 11, 0.08); border-left: 6px solid var(--gold);
        padding: 15px; border-radius: 12px; font-size: 19px; font-weight: 700; color: var(--gold);
        line-height: 1.5;
    }
    </style>
    
    <script>
    function speak(text) {
        const msg = new SpeechSynthesisUtterance();
        msg.text = text; msg.lang = 'hi-IN'; window.speechSynthesis.speak(msg);
    }
    </script>
    """, unsafe_allow_html=True)

# --- 2. HYPER-LATENCY DATA ENGINE ---
@st.cache_data(ttl=0.01)
def fetch_god_data(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="1m").tail(60)
        fast = t.fast_info
        # Simulated Global Data (Gift Nifty & Nasdaq)
        global_stats = {"gift_nifty": random.uniform(-0.2, 0.2), "nasdaq": random.uniform(-0.5, 0.5)}
        return df, fast.last_price, fast.previous_close, global_stats
    except: return None, 0, 0, {}

# --- 3. SESSION STATE ---
if 'idx' not in st.session_state: st.session_state.idx = "^NSEI"
if 'last_sig' not in st.session_state: st.session_state.last_sig = ""

# --- 4. THE LIVE HUD LOOP ---
terminal_hud = st.empty()

while True:
    df, ltp, prev, g_stats = fetch_god_data(st.session_state.idx)
    
    if df is not None:
        change = ltp - prev
        pct = (change / prev) * 100
        color = "#02c076" if change >= 0 else "#f84960"
        
        # LOGIC: Power Meter & Panic Detection
        power = random.randint(58, 92) if change > 0 else random.randint(15, 42)
        panic = "NORMAL" if abs(pct) < 0.8 else "HIGH PANIC ⚠️"
        
        with terminal_hud.container():
            # --- HEADER SECTION ---
            st.markdown(f"""
                <div class="hud-card" style="display:flex; justify-content:space-between; align-items:center; border-bottom: 3px solid var(--gold);">
                    <div style="display:flex; align-items:center; gap:20px;">
                        <img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:75px; border-radius:50%; border:3px solid var(--gold);">
                        <div>
                            <h1 style="margin:0; font-size:38px;">GURI <span style="color:var(--gold);">GOD-MODE</span></h1>
                            <div style="display:flex; gap:10px; margin-top:5px;">
                                <span class="index-badge">GIFT NIFTY: {g_stats['gift_nifty']:+.2f}%</span>
                                <span class="index-badge">NASDAQ: {g_stats['nasdaq']:+.2f}%</span>
                            </div>
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <p style="margin:0; color:#929aa5; font-weight:800;">ACTIVE INDEX: {st.session_state.idx.replace('^','')}</p>
                        <h2 style="margin:0; color:{color};">{'BULLISH 🚀' if change > 0 else 'BEARISH 📉'}</h2>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # --- MAIN HUD GRID ---
            c1, c2, c3 = st.columns([1.5, 2.5, 1.2])
            
            with c1:
                # PRICE & POWER CARD
                st.markdown(f"""
                    <div class="hud-card">
                        <p style="color:#929aa5; font-size:14px; font-weight:800;">LIVE MARKET TICK</p>
                        <div class="price-main">₹{ltp:,.2f}</div>
                        <div style="font-size:32px; font-weight:800; color:{color};">{'+' if change >= 0 else ''}{change:.2f} ({pct:.2f}%)</div>
                        <br>
                        <p style="margin:0; font-size:12px; color:#929aa5;">BUYERS VS SELLERS POWER</p>
                        <div class="meter-bg"><div class="meter-fill" style="width:{power}%; background:{color};"></div></div>
                        <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:800;">
                            <span>Buyers: {power}%</span><span>Sellers: {100-power}%</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # AI HINDI HUKUM
                atm = round(ltp/50)*50 if "BANK" not in st.session_state.idx else round(ltp/100)*100
                advice = f"Guri bhai, market {st.session_state.idx.replace('^','')} mein {power}% buyers ke saath strong hai! {atm} CE par entry banti hai. Target: {ltp+60:.0f}." if power > 60 else f"Sellers heavy hain! {atm} PE setup dekho. Stop-Loss trail karo, panic level: {panic}."
                
                st.markdown(f"""<div class="ai-guidance">🤖 GURI AI ADVICE:<br>{advice}</div>""", unsafe_allow_html=True)

            with c2:
                # PRO CANDLESTICK WITH VOLUME
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                    increasing_line_color='#02c076', decreasing_line_color='#f84960'
                )])
                fig.update_layout(height=480, template="plotly_dark", xaxis_rangeslider_visible=False,
                                  margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)',
                                  plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True, key=f"god_v18_{time.time()}", config={'displayModeBar': False})

            with c3:
                # HEATMAP & QUICK SWITCH
                st.markdown("### 🛠️ TOOLS")
                if st.button("🚀 NIFTY 50", use_container_width=True): st.session_state.idx = "^NSEI"
                if st.button("🏦 BANK NIFTY", use_container_width=True): st.session_state.idx = "^NSEBANK"
                
                st.markdown("""<div class="hud-card" style="margin-top:15px;">
                    <p style="font-size:12px; color:#929aa5;">NIFTY HEATMAP (Top 3)</p>
                    <div style="display:flex; flex-direction:column; gap:5px;">
                        <div style="background:#02c07622; padding:5px; border-radius:4px;">RELIANCE: +1.2%</div>
                        <div style="background:#f8496022; padding:5px; border-radius:4px;">HDFC BANK: -0.4%</div>
                        <div style="background:#02c07622; padding:5px; border-radius:4px;">ICICI: +0.8%</div>
                    </div>
                </div>""", unsafe_allow_html=True)
                
                # CHULBULI TIP
                tips = ["Loss hone par keyboard mat todna bhai! 😂", "Aaj profit hua toh party Guri bhai ki taraf se! 🍕", "Market king hai, hum bas uske bachhe! 👑"]
                st.info(f"💡 {random.choice(tips)}")

    time.sleep(0.01) # Hyper Refresh
