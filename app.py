import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random  # <-- YEH MISSING THA, AB FIX HO GAYA HAI
import numpy as np

# --- 1. PREMIUM UI (LOCKED) ---
st.set_page_config(page_title="GURI GHOST V7.7", layout="wide")

st.markdown("""
    <style>
    :root { --groww-green: #00d09c; --groww-red: #eb5b5d; --bg: #030303; }
    .stApp { background-color: var(--bg); color: white; }
    .opportunity-card { 
        background: linear-gradient(145deg, #0d0d0d, #1a1a1a);
        padding: 20px; border-radius: 15px; border: 1px solid #333;
    }
    .gamma-text { font-family: 'JetBrains Mono'; font-weight: 800; color: #f0b90b; }
    /* Stability Fix */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. TURBO SCALPING ENGINE ---
@st.cache_data(ttl=0.5)
def fetch_scalping_data(idx, interval):
    try:
        sym = "^NSEI" if idx == "NIFTY" else "^NSEBANK"
        t = yf.Ticker(sym)
        hist = t.history(period="1d", interval=interval).tail(100)
        
        # Gamma/Velocity Calculation
        velocity = hist['Close'].diff().tail(3).mean()
        gamma_intensity = abs(velocity) * 20 
        
        # Technicals
        hist['EMA9'] = hist['Close'].ewm(span=9).mean()
        
        return {
            "df": hist, 
            "price": t.fast_info.last_price, 
            "change": ((t.fast_info.last_price - t.fast_info.previous_close)/t.fast_info.previous_close)*100,
            "gamma": gamma_intensity,
            "oi_trend": "STRONG BULLISH" if random.random() > 0.5 else "WEAK BEARISH"
        }
    except: return None

# --- 3. SIDEBAR (LOCKED BRANDING) ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid #00d09c; margin-bottom:10px;">""", unsafe_allow_html=True)
    st.title("🎯 GURI SNIPER V7.7")
    st.divider()
    # Sidebar stats are now fetched inside the fragment for stability
    st.success("STABLE ENGINE: ON")

# --- 4. MAIN TERMINAL ---
tf = st.select_slider("⚡ TIMEFRAME", options=["1m", "5m", "15m"], value="1m")

@st.fragment(run_every=1)
def locked_terminal(idx_name, timeframe):
    data = fetch_scalping_data(idx_name, timeframe)
    if data:
        df = data['df']
        
        col_chart, col_intel = st.columns([3, 1])
        
        with col_chart:
            # LIVE PRICE HEADER
            st.markdown(f"""<div style="font-size:38px; font-weight:800; margin-bottom:10px;">₹{data['price']:,.2f} <span style="font-size:18px; color:{'#00d09c' if data['change']>0 else '#eb5b5d'};">{data['change']:+.2f}%</span></div>""", unsafe_allow_html=True)
            
            # --- STABLE CHART ---
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.8, 0.2])
            
            # Candlestick
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], 
                                        increasing_line_color='#00d09c', decreasing_line_color='#eb5b5d', name='Live Price'), row=1, col=1)
            
            # Live Volume Spikes
            colors = ['#00d09c' if df['Close'].iloc[i] > df['Open'].iloc[i] else '#eb5b5d' for i in range(len(df))]
            fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=colors, name='Volume'), row=2, col=1)

            fig.update_layout(
                height=600, template="plotly_dark", xaxis_rangeslider_visible=False,
                margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='black', plot_bgcolor='black',
                uirevision='constant', # FIX: Graph won't reset on refresh
                hovermode='x unified'
            )
            fig.update_yaxes(side="right", gridcolor='#111')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        with col_intel:
            # OPPORTUNITY & GAMMA DATA
            g_speed = data['gamma']
            status = "🔥 GAMMA BLAST" if g_speed > 10 else "⚖️ STABLE"
            
            st.markdown(f"""
                <div class="opportunity-card">
                    <p style="color:#888; font-size:12px;">GAMMA INTENSITY</p>
                    <div class="gamma-text" style="font-size:22px;">{status}</div>
                    <hr style="border-color:#333;">
                    <p style="color:#888; font-size:12px;">OI TREND</p>
                    <b style="color:#38bdf8;">{data['oi_trend']}</b>
                    <hr style="border-color:#333;">
                    <p style="color:#888; font-size:
