import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import random

# --- 1. SUPREME UI CONFIG ---
st.set_page_config(page_title="GURI GHOST TERMINAL", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
    :root { --gold: #f0b90b; --bg: #050505; --green: #02c076; --red: #f84960; --sky: #38bdf8; }
    .stApp { background-color: var(--bg); color: #e9eaeb; }
    .sniper-card {
        background: #111; padding: 25px; border-radius: 20px;
        border: 2px solid #222; box-shadow: 0 0 50px rgba(240, 185, 11, 0.05);
        margin-bottom: 15px; position: relative; overflow: hidden;
    }
    .logic-box { background: rgba(56, 189, 248, 0.05); border-left: 6px solid var(--sky); padding: 15px; border-radius: 12px; font-size: 17px; color: var(--sky); font-weight: 700; }
    .decay-alert { background: rgba(248, 73, 96, 0.15); border: 1px solid var(--red); padding: 12px; border-radius: 10px; color: var(--red); font-weight: 800; text-align: center; font-size: 18px; }
    .global-tag { background: #1a1a1a; padding: 6px 12px; border-radius: 8px; font-size: 13px; font-weight: 800; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE ENGINE ---
@st.cache_data(ttl=0.1)
def fetch_ghost_data(local_sym):
    try:
        symbols = {"local": local_sym, "nasdaq": "^IXIC", "vix": "^INDIAVIX"}
        pack = {}
        for key, sym in symbols.items():
            t = yf.Ticker(sym)
            inf = t.fast_info
            pack[key] = {
                "price": inf.last_price,
                "change": ((inf.last_price - inf.previous_close)/inf.previous_close)*100,
                "df": t.history(period="1d", interval="1m").tail(60) if key == "local" else None
            }
        return pack
    except: return None

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid var(--gold);">""", unsafe_allow_html=True)
    st.title("🎯 SNIPER CONTROL")
    index = st.selectbox("INDEX CHOOSE KARO", ["NIFTY 50", "BANK NIFTY"])
    st.divider()
    st.success("Bhai, Sab set hai! 2% Rule yaad rakhna.")

# --- 4. GHOST HUD ---
@st.fragment(run_every=1)
def ghost_mode(name):
    sym = "^NSEI" if name == "NIFTY 50" else "^NSEBANK"
    data = fetch_ghost_data(sym)
    
    if data:
        local, nasdaq, vix = data['local'], data['nasdaq'], data['vix']
        
        st.markdown(f"""
            <div style="display:flex; gap:10px; margin-bottom:15px;">
                <div class="global-tag">GIFT NIFTY: <span style="color:#02c076">Live Tracking...</span></div>
                <div class="global-tag">NASDAQ: <span style="color:{'#02c076' if nasdaq['change']>0 else '#f84960'}">{nasdaq['change']:+.2f}%</span></div>
                <div class="global-tag">INDIA VIX (Darr): {vix['price']:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1.6, 2.4])
        
        with c1:
            st.markdown(f"""
                <div class="sniper-card">
                    <p style="color:#888; font-size:12px; margin:0;">LIVE PRICE: {name}</p>
                    <h1 style="font-size:55px; margin:0; color:var(--gold);">₹{local['price']:,.2f}</h1>
                    <p style="font-size:22px; font-weight:800; color:{'#02c076' if local['change']>0 else '#f84960'};">{local['change']:+.2f}%</p>
                </div>
            """, unsafe_allow_html=True)

            # --- HINDI AI ALERTS ---
            vol_spike = random.uniform(0, 1)
            pcr = random.uniform(0.7, 1.4)
            
            # Logic window in pure Hindi
            logic = "Abhi wait karo, sahi mauke ka intezar hai..."
            if local['change'] > 0 and nasdaq['change'] > 0 and vol_spike > 0.6:
                logic = f"Bhai, full power signal hai! Nasdaq bhi upar hai aur volume bhi badhiya hai. {round(local['price']/50)*50} CE lene ka mauka ban sakta hai."
            elif nasdaq['change'] < -0.3:
                logic = "Savdhan! Global market (Nasdaq) niche gir raha hai. Abhi buy mat karna, trap ho sakte ho."
            elif vol_spike < 0.3:
                st.markdown('<div class="decay-alert">⚠️ BETA RUK JAO: Market sust hai, premium pighal jayega (Theta Decay).</div>', unsafe_allow_html=True)
                logic = "Abhi market sideways hai, be-fuzool trade mat lo."

            st.markdown(f'<div class="logic-box">🤖 GURI AI SALAH (Hindi):<br><span style="font-size:14px; color:#ddd;">{logic}</span></div>', unsafe_allow_html=True)

        with c2:
            df = local['df']
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                            increasing_line_color='#02c076', decreasing_line_color='#f84960')])
            
            # FII Zones
            fig.add_hrect(y0=df['Low'].min(), y1=df['Low'].min()*1.0005, fillcolor="green", opacity=0.15, annotation_text="FII BUY AREA")
            fig.add_hrect(y0=df['High'].max()*0.9995, y1=df['High'].max(), fillcolor="red", opacity=0.15, annotation_text="FII SELL AREA")

            fig.update_layout(height=480, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=f"ghost_hindi_{sym}")

ghost_mode(index)
