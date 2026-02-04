import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

# --- 1. PREMIUM UI (LOCKED) ---
st.set_page_config(page_title="GURI GHOST V7.5", layout="wide")

st.markdown("""
    <style>
    :root { --groww-green: #00d09c; --groww-red: #eb5b5d; --bg: #030303; }
    .stApp { background-color: var(--bg); color: white; }
    .price-card { background: #0d0d0d; padding: 20px; border-radius: 15px; border: 1px solid #222; }
    .pulse-card { background: #111; padding: 10px; border-radius: 8px; border: 1px solid #222; margin-bottom: 5px; font-size: 12px; }
    .sniper-alert { padding: 15px; border-radius: 12px; text-align: center; font-weight: 800; font-size: 20px; border: 2px solid #333; }
    /* Stability Fix: Hide Streamlit elements that cause shifts */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. TURBO DATA ENGINE (NO LAG) ---
@st.cache_data(ttl=0.5) # Fast 0.5s Refresh
def fetch_turbo_data(idx, interval):
    targets = {
        "MAIN": "^NSEI" if idx == "NIFTY" else "^NSEBANK",
        "NASDAQ": "^IXIC", "VIX": "^INDIAVIX",
        "RELIANCE": "RELIANCE.NS", "HDFCBANK": "HDFCBANK.NS", "IT": "^CNXIT"
    }
    res = {}
    for name, sym in targets.items():
        try:
            t = yf.Ticker(sym)
            if name == "MAIN":
                hist = t.history(period="2d", interval=interval)
                hist['EMA20'] = hist['Close'].ewm(span=20, adjust=False).mean()
                exp1 = hist['Close'].ewm(span=12, adjust=False).mean()
                exp2 = hist['Close'].ewm(span=26, adjust=False).mean()
                hist['MACD'] = exp1 - exp2
                hist['Signal'] = hist['MACD'].ewm(span=9, adjust=False).mean()
                res['df'] = hist
            
            info = t.fast_info
            res[name] = {"price": info.last_price, "change": ((info.last_price - info.previous_close)/info.previous_close)*100}
        except: res[name] = {"price": 0, "change": 0}
    return res

# --- 3. SIDEBAR (GURI BRANDING - LOCKED) ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid #00d09c; margin-bottom:10px;">""", unsafe_allow_html=True)
    st.title("🎯 GURI SNIPER PRO")
    st.divider()
    st.success("SYSTEM LOCKED: V7.5")

# --- 4. MAIN DASHBOARD ---
tf = st.select_slider("⚡ TIMEFRAME", options=["1m", "5m", "15m", "30m", "1h"], value="5m")

@st.fragment(run_every=1)
def stable_terminal(idx_name, timeframe):
    data = fetch_turbo_data(idx_name, timeframe)
    if 'df' in data:
        df = data['df']
        
        # HEADER (GLOBAL)
        st.markdown(f"""
            <div style="display:flex; gap:10px; margin-bottom:15px;">
                <div style="background:#111; padding:5px 12px; border-radius:8px; border:1px solid #333;">🇺🇸 NASDAQ: <span style="color:{'#00d09c' if data['NASDAQ']['change']>0 else '#eb5b5d'}">{data['NASDAQ']['change']:+.2f}%</span></div>
                <div style="background:#111; padding:5px 12px; border-radius:8px; border:1px solid #333;">📉 VIX: {data['VIX']['price']:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

        col_pulse, col_chart = st.columns([1, 3.5])
        
        with col_pulse:
            st.subheader("🏛️ MARKET PULSE")
            for item in ["RELIANCE", "HDFCBANK", "IT"]:
                s_data = data[item]
                c = "#00d09c" if s_data['change'] > 0 else "#eb5b5d"
                st.markdown(f"""<div class="pulse-card">{item}<br><b style="color:{c};">₹{s_data['price']:,.1f} ({s_data['change']:+.2f}%)</b></div>""", unsafe_allow_html=True)
            
            st.divider()
            last_macd = df['MACD'].iloc[-1]; last_sig = df['Signal'].iloc[-1]
            if last_macd > last_sig:
                st.markdown("""<div class="sniper-alert" style="color:#00d09c; border-color:#00d09c; background:rgba(0,208,156,0.1);">🚀 CALL GOLI CHALAO</div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class="sniper-alert" style="color:#eb5b5d; border-color:#eb5b5d; background:rgba(235,91,93,0.1);">📉 PUT GOLI CHALAO</div>""", unsafe_allow_html=True)

        with col_chart:
            # Main Price Display
            st.markdown(f"""<div style="font-size:42px; font-weight:800; margin-bottom:-10px;">₹{data['MAIN']['price']:,.2f} <span style="font-size:18px; color:{'#00d09c' if data['MAIN']['change']>0 else '#eb5b5d'};">{data['MAIN']['change']:+.2f}%</span></div>""", unsafe_allow_html=True)
            
            # --- STABLE GRAPH ENGINE ---
            fig = make_subplots(rows=1, cols=1)
            
            # Candlestick
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], 
                                        increasing_line_color='#00d09c', decreasing_line_color='#eb5b5d', name='Live Price'))
            
            # Sniper Arrows
            buy_pts = df[(df['MACD'] > df['Signal']) & (df['MACD'].shift(1) <= df['Signal'].shift(1))]
            sell_pts = df[(df['MACD'] < df['Signal']) & (df['MACD'].shift(1) >= df['Signal'].shift(1))]
            fig.add_trace(go.Scatter(x=buy_pts.index, y=buy_pts['Low']*0.999, mode='markers', marker=dict(symbol='triangle-up', size=13, color='#00d09c'), name='Buy'))
            fig.add_trace(go.Scatter(x=sell_pts.index, y=sell_pts['High']*1.001, mode='markers', marker=dict(symbol='triangle-down', size=13, color='#eb5b5d'), name='Sell'))

            # Fixed Layout for Mouse Stability
            fig.update_layout(
                height=580, template="plotly_dark", xaxis_rangeslider_visible=False,
                margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='black', plot_bgcolor='black',
                hovermode='x unified', # Smooth mouse hover
                uirevision='constant'   # FIX: Prevents graph flicker on refresh
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=True, gridcolor='#111', side="right")
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

target = st.selectbox("MARKET", ["NIFTY", "BANKNIFTY"], label_visibility="collapsed")
stable_terminal(target, tf)
