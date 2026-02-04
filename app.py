import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import numpy as np

# --- 1. UI & PULSE DOT CSS ---
st.set_page_config(page_title="GURI GHOST V7.8", layout="wide")

st.markdown("""
    <style>
    :root { --groww-green: #00d09c; --groww-red: #eb5b5d; --bg: #030303; }
    .stApp { background-color: var(--bg); color: white; }
    
    /* Live Pulse Dot Animation */
    .pulse-dot {
        height: 15px; width: 15px; border-radius: 50%; display: inline-block;
        margin-right: 10px; box-shadow: 0 0 10px;
        animation: pulse-animation 1s infinite;
    }
    @keyframes pulse-animation {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 208, 156, 0.7); }
        70% { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(0, 208, 156, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 208, 156, 0); }
    }
    
    .opportunity-card { 
        background: linear-gradient(145deg, #0d0d0d, #1a1a1a);
        padding: 20px; border-radius: 15px; border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE SNIPER STRATEGY ENGINE ---
@st.cache_data(ttl=0.5)
def sniper_engine(idx, interval):
    try:
        sym = "^NSEI" if idx == "NIFTY" else "^NSEBANK"
        t = yf.Ticker(sym)
        hist = t.history(period="1d", interval=interval).tail(100)
        
        # Strategy Layer 1: Velocity (Gamma)
        velocity = hist['Close'].diff().tail(3).mean()
        gamma = abs(velocity) * 20
        
        # Strategy Layer 2: EMA 9 & MACD
        hist['EMA9'] = hist['Close'].ewm(span=9).mean()
        exp1 = hist['Close'].ewm(span=12).mean()
        exp2 = hist['Close'].ewm(span=26).mean()
        macd = exp1 - exp2
        sig = macd.ewm(span=9).mean()
        
        # Strategy Layer 3: Volume Spike
        vol_spike = hist['Volume'].iloc[-1] > hist['Volume'].tail(10).mean() * 1.5
        
        # FINAL DECISION
        decision = "WAIT"
        if velocity > 0.5 and macd.iloc[-1] > sig.iloc[-1] and vol_spike:
            decision = "CALL"
        elif velocity < -0.5 and macd.iloc[-1] < sig.iloc[-1] and vol_spike:
            decision = "PUT"
            
        return {
            "df": hist, "price": t.fast_info.last_price, "gamma": gamma,
            "change": ((t.fast_info.last_price - t.fast_info.previous_close)/t.fast_info.previous_close)*100,
            "decision": decision
        }
    except: return None

# --- 3. SIDEBAR (LOCKED) ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid #00d09c; margin-bottom:10px;">""", unsafe_allow_html=True)
    st.title("🎯 GURI GHOST V7.8")
    st.divider()
    st.write("🛠 Strategy: **Triple-Layer Sniper**")
    st.write("📡 Speed: **Turbo High**")

# --- 4. MAIN TERMINAL ---
tf = st.select_slider("⚡ TIMEFRAME", options=["1m", "5m", "15m"], value="1m")

@st.fragment(run_every=1)
def locked_terminal_v78(idx_name, timeframe):
    data = sniper_engine(idx_name, timeframe)
    if data:
        df = data['df']
        
        # HEADER WITH LIVE PULSE DOT
        dot_color = "#00d09c" if data['decision'] == "CALL" else "#eb5b5d" if data['decision'] == "PUT" else "#333"
        st.markdown(f"""
            <div style="display:flex; align-items:center;">
                <span class="pulse-dot" style="background-color:{dot_color}; box-shadow: 0 0 10px {dot_color};"></span>
                <span style="font-size:35px; font-weight:800;">₹{data['price']:,.2f}</span>
                <span style="font-size:18px; color:{'#00d09c' if data['change']>0 else '#eb5b5d'}; margin-left:15px;">{data['change']:+.2f}%</span>
            </div>
        """, unsafe_allow_html=True)

        col_chart, col_intel = st.columns([3, 1])
        
        with col_chart:
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.8, 0.2])
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], 
                                        increasing_line_color='#00d09c', decreasing_line_color='#eb5b5d', name='Price'), row=1, col=1)
            
            # Volume
            colors = ['#00d09c' if df['Close'].iloc[i] > df['Open'].iloc[i] else '#eb5b5d' for i in range(len(df))]
            fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=colors, name='Volume'), row=2, col=1)

            fig.update_layout(height=600, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0), 
                              paper_bgcolor='black', plot_bgcolor='black', uirevision='constant', hovermode='x unified')
            fig.update_yaxes(side="right", gridcolor='#111')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        with col_intel:
            # DYNAMIC SCALPER ALERT
            if data['decision'] != "WAIT":
                st.markdown(f"""
                    <div class="opportunity-card" style="border-color:{dot_color};">
                        <h3 style="color:{dot_color}; margin:0;">🚀 {data['decision']} ENTRY</h3>
                        <p style="font-size:14px; margin-top:10px;">
                            <b>Gamma:</b> High Blast<br>
                            <b>Target:</b> 12-18 Points<br>
                            <b>Exit:</b> 3 min scalp
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""<div class="opportunity-card">⌛ Waiting for Strategy Setup...</div>""", unsafe_allow_html=True)
            
            # FUTURE ANALYSIS
            st.markdown("### 🔮 PROJECTION")
            st.markdown(f"""
                <div style="padding:15px; background:#111; border-radius:10px; border-left:4px solid #f0b90b;">
                    Next Move: <b>{'Accumulation' if data['gamma'] < 5 else 'Explosion Imminent'}</b><br>
                    Hold Time: <b>Strict 3 Mins</b><br>
                    <span style="font-size:11px; color:#666;">*Based on EMA9 + Volume Spike Analysis</span>
                </div>
            """, unsafe_allow_html=True)

target = st.selectbox("MARKET", ["NIFTY", "BANKNIFTY"], label_visibility="collapsed")
locked_terminal_v78(target, tf)
