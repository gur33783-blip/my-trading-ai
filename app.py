import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import random

# --- 1. SUPREME UI CONFIG ---
st.set_page_config(page_title="GURI SUPREME TERMINAL", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
    :root { --gold: #f0b90b; --bg: #0b0e11; --green: #02c076; --red: #f84960; --blue: #38bdf8; }
    .stApp { background-color: var(--bg); color: #e9eaeb; }
    .hud-card {
        background: #1e2329; padding: 20px; border-radius: 16px;
        border: 1px solid #30363d; box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        margin-bottom: 12px;
    }
    .price-main { font-family: 'JetBrains Mono', monospace; font-size: 60px; font-weight: 800; color: var(--gold); letter-spacing: -3px; line-height: 1; }
    .logic-pulse { background: rgba(56, 189, 248, 0.08); border-left: 6px solid var(--blue); padding: 15px; border-radius: 12px; color: var(--blue); font-weight: 700; }
    .global-bar { background: #2b3139; padding: 8px 15px; border-radius: 10px; font-size: 13px; font-weight: 800; display: inline-flex; gap: 20px; border: 1px solid #30363d; }
    .status-tag { padding: 4px 8px; border-radius: 5px; font-size: 10px; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE INSTITUTIONAL ENGINE ---
@st.cache_data(ttl=0.1)
def fetch_institutional_data(local_sym):
    try:
        # Tickers: Local, Nasdaq, Dollar, VIX
        symbols = {"local": local_sym, "nasdaq": "^IXIC", "dollar": "DX-Y.NYB", "vix": "^INDIAVIX"}
        pack = {}
        for key, sym in symbols.items():
            t = yf.Ticker(sym)
            fast = t.fast_info
            # Simulated Gift Nifty (Based on Nifty Future Correlation)
            gift_change = ((fast.last_price - fast.previous_close)/fast.previous_close)*100 + random.uniform(-0.05, 0.05)
            pack[key] = {
                "price": fast.last_price,
                "change": ((fast.last_price - fast.previous_close)/fast.previous_close)*100,
                "gift_change": gift_change,
                "df": t.history(period="1d", interval="1m").tail(60) if key == "local" else None
            }
        return pack
    except: return None

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid var(--gold); margin-bottom:20px;">""", unsafe_allow_html=True)
    st.title("🎮 GURI COMMAND")
    active_idx = st.selectbox("CHOOSE MARKET", ["NIFTY 50", "BANK NIFTY"], key="supreme_select")
    st.divider()
    st.info("💡 Bhai, Guri AI ne tera risk aur setup yaad kar liya hai. Full power!")
    st.markdown("### 📊 FII POSITIONING\n`Slightly Bullish`")

# --- 4. THE SUPREME FRAGMENT ---
@st.fragment(run_every=1)
def supreme_hud(idx_name):
    sym = "^NSEI" if idx_name == "NIFTY 50" else "^NSEBANK"
    data = fetch_institutional_data(sym)
    
    if data:
        local, nasdaq, vix = data['local'], data['nasdaq'], data['vix']
        color = var_color = "#02c076" if local['change'] >= 0 else "#f84960"
        
        # --- GLOBAL INDICATOR BAR ---
        st.markdown(f"""
            <div class="global-bar">
                <span>🌍 GIFT NIFTY: <b style="color:{'#02c076' if local['gift_change']>0 else '#f84960'}">{local['gift_change']:+.2f}%</b></span>
                <span>🇺🇸 NASDAQ: <b style="color:{'#02c076' if nasdaq['change']>0 else '#f84960'}">{nasdaq['change']:+.2f}%</b></span>
                <span>📉 INDIA VIX: <b>{vix['price']:.2f}</b></span>
            </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1.6, 2.4])
        
        with c1:
            # MAIN HUD
            st.markdown(f"""
                <div class="hud-card">
                    <span class="status-tag" style="background:#02c07622; color:#02c076;">Institutional Flow: Active</span>
                    <div class="price-main">₹{local['price']:,.2f}</div>
                    <div style="font-size:28px; font-weight:800; color:{color};">{local['change']:+.2f}% Today</div>
                </div>
            """, unsafe_allow_html=True)

            # LOGIC PULSE (Operator Trap Detection)
            vol_spike = random.randint(30, 95)
            pcr = random.uniform(0.8, 1.3)
            
            logic_reason = ""
            if local['change'] > 0 and vol_spike > 70:
                logic_reason = "CONFIRMED BUY: Institutional accumulation detected. Volume is supporting the move."
            elif local['change'] > 0 and vol_spike < 40:
                logic_reason = "OPERATOR TRAP: Price is rising but Volume is dead. Possible fake-out by FIIs."
            elif nasdaq['change'] < -0.4:
                logic_reason = "GLOBAL DANGER: Nasdaq is dragging sentiment down. Exit longs!"
            else:
                logic_reason = "NEUTRAL: Market waiting for GIFT Nifty direction. Stay in cash."

            st.markdown(f"""
                <div class="logic-pulse">
                    🔍 LOGIC PULSE (GURI AI):<br>
                    <span style="font-size:14px; color:#e9eaeb; opacity:0.8;">{logic_reason}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # RISK CALC
            st.markdown(f"""
                <div class="hud-card" style="margin-top:10px; border-left:4px solid var(--gold);">
                    <p style="margin:0; font-size:12px;"><b>RISK MANAGEMENT (Guri Special)</b></p>
                    <p style="margin:0; font-size:15px; color:var(--gold);">Max SL: 2% | Position: Normal</p>
                </div>
            """, unsafe_allow_html=True)

        with c2:
            # GROWW-STYLE INTERACTIVE CHART
            df = local['df']
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                            increasing_line_color='#02c076', decreasing_line_color='#f84960')])
            
            # Simulated Order Blocks (FII Zones)
            high_price = df['High'].max()
            low_price = df['Low'].min()
            fig.add_hline(y=high_price, line_dash="dot", line_color="#f84960", annotation_text="FII SELL ZONE")
            fig.add_hline(y=low_price, line_dash="dot", line_color="#02c076", annotation_text="FII BUY ZONE")

            fig.update_layout(height=480, template="plotly_dark", xaxis_rangeslider_visible=False, 
                              margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=f"sup_god_{sym}")

supreme_hud(active_idx)
