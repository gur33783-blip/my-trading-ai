import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time
import random

# --- PRO THEME CONFIG ---
st.set_page_config(page_title="Guri AI Terminal", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Sora', sans-serif; background-color: #f8fafc; }
    
    /* Signal Cards */
    .sig-card {
        padding: 20px; border-radius: 12px; margin-bottom: 15px; text-align: center;
        border: 2px solid transparent; transition: 0.3s;
    }
    .call-bg { background: #ecfdf5; border-color: #10b981; color: #065f46; }
    .put-bg { background: #fef2f2; border-color: #ef4444; color: #991b1b; }
    .wait-bg { background: #f1f5f9; border-color: #94a3b8; color: #475569; }

    /* Buttons */
    .action-btn { font-weight: 700; border-radius: 8px; padding: 10px 20px; }
    
    /* Price Header */
    .live-price { font-size: 38px; font-weight: 800; color: #1e293b; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE: NO-DELAY DATA ---
@st.cache_data(ttl=0.1)
def get_clean_data(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="1m").tail(30) # Chhota graph window
        if not df.empty:
            ltp = df['Close'].iloc[-1]
            prev = t.info.get('previousClose', df['Open'].iloc[0])
            return df, ltp, ltp - prev, ((ltp - prev) / prev) * 100
    except: pass
    return None, 0, 0, 0

# --- MAIN LAYOUT ---
col_sig, col_chart = st.columns([1, 2.5])

# Fetch Data
m_map = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK"}
selected = st.sidebar.selectbox("Select Index", list(m_map.keys()))
df, ltp, change, pct = get_clean_data(m_map[selected])

with col_sig:
    st.image("https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg", width=80)
    st.markdown("### AI Scalper Sign")
    
    # AI STRATEGY LOGIC (Entry/Exit)
    rsi = 55 # Simulated RSI
    trend = "BUY CALL" if ltp > df['Close'].mean() and rsi < 70 else "BUY PUT" if ltp < df['Close'].mean() and rsi > 30 else "WAIT"
    
    if trend == "BUY CALL":
        st.markdown(f"""<div class="sig-card call-bg">
            <h2>🚀 CALL ENTRY</h2>
            <p>ENTRY: {ltp:.2f}<br><b>TARGET: {ltp+35:.2f}</b><br>SL: {ltp-15:.2f}</p>
        </div>""", unsafe_allow_html=True)
    elif trend == "BUY PUT":
        st.markdown(f"""<div class="sig-card put-bg">
            <h2>📉 PUT ENTRY</h2>
            <p>ENTRY: {ltp:.2f}<br><b>TARGET: {ltp-35:.2f}</b><br>SL: {ltp+15:.2f}</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="sig-card wait-bg"><h2>⌛ WAIT</h2><p>Market Sideways</p></div>', unsafe_allow_html=True)

    # EXIT ANALYSIS
    st.info(f"**AI Exit Tip:** {'Hold position with trailing SL' if abs(pct) > 1 else 'Book small profits & Exit'}")

with col_chart:
    # Top Live Info
    c_color = "#10b981" if change >= 0 else "#ef4444"
    st.markdown(f"""
        <div>
            <p style="margin:0; color:#64748b;">{selected} Live</p>
            <h1 class="live-price">₹{ltp:,.2f}</h1>
            <p style="color:{c_color}; font-weight:700;">{'+' if change>=0 else ''}{change:.2f} ({pct:.2f}%)</p>
        </div>
    """, unsafe_allow_html=True)
    
    # SMALL PROFESSIONAL CHART
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                                 increasing_line_color='#10b981', decreasing_line_color='#ef4444', name="Price"))
    # Entry line indicator
    fig.add_hline(y=ltp, line_dash="dot", line_color="#94a3b8", annotation_text="Current Entry")
    
    fig.update_layout(height=350, template="plotly_white", margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

# --- CHAT & OPTION CHAIN (Bottom Strip) ---
st.divider()
c_chat, c_opt = st.columns([1, 2])

with c_chat:
    st.markdown("#### 💬 Guri AI Chat")
    q = st.text_input("Ask Market Move...", key="main_chat")
    if q: st.write(f"🤖: {selected} is showing {'strength' if change > 0 else 'weakness'} at {ltp:.0f}. Follow the signal.")

with c_opt:
    st.markdown("#### ⛓️ Quick Option Chain")
    atm = round(ltp/50)*50
    oc = pd.DataFrame({
        "CALL (CE)": [random.randint(80, 150) for _ in range(3)],
        "STRIKE": [atm-50, atm, atm+50],
        "PUT (PE)": [random.randint(80, 150) for _ in range(3)]
    })
    st.table(oc)

time.sleep(0.5)
st.rerun()
