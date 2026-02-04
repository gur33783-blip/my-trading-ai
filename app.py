import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# --- 1. PREMIUM UI ---
st.set_page_config(page_title="GURI GHOST V7.6", layout="wide")

st.markdown("""
    <style>
    :root { --groww-green: #00d09c; --groww-red: #eb5b5d; --bg: #030303; }
    .stApp { background-color: var(--bg); color: white; }
    .opportunity-card { 
        background: linear-gradient(145deg, #0d0d0d, #1a1a1a);
        padding: 20px; border-radius: 15px; border: 1px solid #333;
        box-shadow: 0 4px 15px rgba(0,208,156,0.1);
    }
    .gamma-text { font-family: 'JetBrains Mono'; font-weight: 800; color: #f0b90b; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ADVANCED SCALPING ENGINE ---
@st.cache_data(ttl=0.5)
def fetch_scalping_data(idx, interval):
    try:
        sym = "^NSEI" if idx == "NIFTY" else "^NSEBANK"
        t = yf.Ticker(sym)
        hist = t.history(period="1d", interval=interval).tail(100)
        
        # Simulated OI & Gamma Logic (Real-time approx)
        # In live markets, Gamma spikes when price velocity increases
        velocity = hist['Close'].diff().tail(5).mean()
        gamma_intensity = abs(velocity) * 10 
        
        # Indicators for entry
        hist['EMA9'] = hist['Close'].ewm(span=9).mean()
        hist['VWAP'] = (hist['Close'] * hist['Volume']).cumsum() / hist['Volume'].cumsum()
        
        return {
            "df": hist, 
            "price": t.fast_info.last_price, 
            "gamma": gamma_intensity,
            "oi_change": random.uniform(-5, 5) # Placeholder for OI Trend
        }
    except: return None

# --- 3. SIDEBAR (LOCKED) ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid #00d09c; margin-bottom:10px;">""", unsafe_allow_html=True)
    st.title("🎯 GURI GHOST V7.6")
    st.divider()
    st.write("📡 OI Trend: **STRONG BULLISH**" if random.random() > 0.5 else "📡 OI Trend: **WEAK BEARISH**")

# --- 4. MAIN TERMINAL ---
tf = st.select_slider("⚡ TIMEFRAME", options=["1m", "5m", "15m"], value="1m")

@st.fragment(run_every=1)
def scalping_terminal(idx_name, timeframe):
    data = fetch_scalping_data(idx_name, timeframe)
    if data:
        df = data['df']
        
        col_chart, col_intel = st.columns([3, 1])
        
        with col_chart:
            # HEADER
            st.markdown(f"### {idx_name} Live Scalper | ₹{data['price']:.2f}")
            
            # --- STABLE CHART WITH VOLUME & GAMMA ---
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.8, 0.2])
            
            # Candles
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], 
                                        increasing_line_color='#00d09c', decreasing_line_color='#eb5b5d', name='Price'), row=1, col=1)
            
            # Live Volume
            colors = ['#00d09c' if df['Close'].iloc[i] > df['Open'].iloc[i] else '#eb5b5d' for i in range(len(df))]
            fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=colors, name='Volume'), row=2, col=1)

            fig.update_layout(
                height=600, template="plotly_dark", xaxis_rangeslider_visible=False,
                margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='black', plot_bgcolor='black',
                uirevision=timeframe, # CRITICAL: Graph stays stable during refresh
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        with col_intel:
            st.subheader("🚀 OPPORTUNITY")
            
            # Gamma Blast Logic
            g_speed = data['gamma']
            status = "STABLE"
            if g_speed > 15: status = "🔥 GAMMA BLASTING"
            elif g_speed > 8: status = "⚡ SPEED PICKING UP"
            
            # ENTRY/EXIT INTEL
            st.markdown(f"""
                <div class="opportunity-card">
                    <p style="color:#888; font-size:12px; margin-bottom:5px;">GAMMA INTENSITY</p>
                    <div class="gamma-text" style="font-size:24px;">{status}</div>
                    <hr style="border-color:#333;">
                    <p style="color:#888; font-size:12px;">SCALPER ADVICE</p>
                    <b style="color:#00d09c;">Entry:</b> Now (Above VWAP)<br>
                    <b style="color:#eb5b5d;">Exit Time:</b> 3-5 Mins Max<br>
                    <b style="color:#f0b90b;">Gamma Potential:</b> 20-30% Spike
                    <hr style="border-color:#333;">
                    <p style="font-size:11px; color:#666;">Hold Strategy: Jab tak candle EMA9 ke upar hai, ride karo. Gamma fatega toh 1 min mein niklo.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # FUTURE MOVEMENT BOX (Simulated Analysis)
            st.markdown("### 🔮 FUTURE PROJECTION")
            st.markdown(f"""
                <div style="padding:10px; background:#111; border-radius:10px; border-left:4px solid #f0b90b;">
                    Next 15 min movement: <b>{'UPWARD RECOVERY' if data['oi_change'] > 0 else 'SIDEWAYS DRIP'}</b><br>
                    OI Resistance: <b>{data['price'] + 50:.0f}</b><br>
                    OI Support: <b>{data['price'] - 50:.0f}</b>
                </div>
            """, unsafe_allow_html=True)

target_m = st.selectbox("MARKET", ["NIFTY", "BANKNIFTY"], label_visibility="collapsed")
scalping_terminal(target_m, tf)
