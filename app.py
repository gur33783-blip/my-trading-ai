import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

# --- 1. GROWW STYLE PREMIUM CSS ---
st.set_page_config(page_title="GURI GHOST V7.3 PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;800&display=swap');
    :root { --groww-green: #00d09c; --groww-red: #eb5b5d; --bg: #030303; --card: #0d0d0d; }
    .stApp { background-color: var(--bg); color: #ffffff; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .price-box { 
        background: var(--card); padding: 25px; border-radius: 16px; 
        border: 1px solid #222; text-align: left; 
    }
    .price-val { font-size: 50px; color: #ffffff; font-weight: 800; letter-spacing: -1px; }
    
    .sniper-status {
        padding: 20px; border-radius: 16px; margin-top: 15px;
        font-weight: 800; font-size: 22px; text-align: center;
    }
    .bull-btn { background: rgba(0, 208, 156, 0.15); color: var(--groww-green); border: 1px solid var(--groww-green); }
    .bear-btn { background: rgba(235, 91, 93, 0.15); color: var(--groww-red); border: 1px solid var(--groww-red); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PROFESSIONAL DATA ENGINE ---
@st.cache_data(ttl=1)
def get_groww_data(idx, interval):
    try:
        sym = "^NSEI" if idx == "NIFTY" else "^NSEBANK"
        t = yf.Ticker(sym)
        hist = t.history(period="5d", interval=interval)
        
        # Groww Style Indicators
        hist['EMA20'] = hist['Close'].ewm(span=20, adjust=False).mean()
        hist['EMA50'] = hist['Close'].ewm(span=50, adjust=False).mean()
        exp1 = hist['Close'].ewm(span=12, adjust=False).mean()
        exp2 = hist['Close'].ewm(span=26, adjust=False).mean()
        hist['MACD'] = exp1 - exp2
        hist['Signal'] = hist['MACD'].ewm(span=9, adjust=False).mean()
        
        # For Bollinger Bands
        hist['MA20'] = hist['Close'].rolling(window=20).mean()
        hist['STD'] = hist['Close'].rolling(window=20).std()
        hist['Upper'] = hist['MA20'] + (hist['STD'] * 2)
        hist['Lower'] = hist['MA20'] - (hist['STD'] * 2)

        curr = t.fast_info.last_price
        change = ((curr - t.fast_info.previous_close)/t.fast_info.previous_close)*100
        return {"df": hist, "price": curr, "change": change}
    except: return None

# --- 3. SIDEBAR BRANDING ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:2px solid #00d09c; margin-bottom:10px;">""", unsafe_allow_html=True)
    st.title("🎯 GURI SNIPER V7.3")
    st.divider()
    v_macd = st.checkbox("MACD (Trend Confirm)", value=True)
    v_ema = st.checkbox("EMA Cloud (Support)", value=True)
    v_bb = st.checkbox("BB (Volatility)", value=True)
    st.divider()
    st.write("Guri bhai, chart par arrows dekh kar entry lo.")

# --- 4. MAIN TERMINAL ---
tf_choice = st.select_slider("⚡ TIMEFRAME", options=["1m", "5m", "15m", "30m", "1h"], value="5m")

@st.fragment(run_every=1)
def groww_terminal(idx_name, timeframe):
    data = get_groww_data(idx_name, timeframe)
    if data:
        df = data['df']
        
        c1, c2 = st.columns([1.2, 3])
        
        with c1:
            color = "#00d09c" if data['change'] > 0 else "#eb5b5d"
            st.markdown(f"""
                <div class="price-box">
                    <p style="margin:0; color:#888; font-size:14px;">{idx_name} INDEX</p>
                    <div class="price-val">₹{data['price']:,.2f}</div>
                    <p style="font-size:20px; color:{color}; font-weight:800;">{data['change']:+.2f}%</p>
                </div>
            """, unsafe_allow_html=True)
            
            # --- SNIPER LOGIC (ENTRY DECISION) ---
            last_macd = df['MACD'].iloc[-1]
            last_sig = df['Signal'].iloc[-1]
            last_price = df['Close'].iloc[-1]
            ema20 = df['EMA20'].iloc[-1]
            
            if last_macd > last_sig and last_price > ema20:
                st.markdown("""<div class="sniper-status bull-btn">🐂 BULL ATTACK<br><span style='font-size:15px;'>CALL ME GOLI CHALAO</span></div>""", unsafe_allow_html=True)
            elif last_macd < last_sig and last_price < ema20:
                st.markdown("""<div class="sniper-status bear-btn">🐻 BEAR TRAP<br><span style='font-size:15px;'>PUT ME GOLI CHALAO</span></div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class="sniper-status" style="border:1px solid #333;">⌛ NO ENTRY<br><span style='font-size:14px; color:#666;'>WAIT FOR SIGNAL</span></div>""", unsafe_allow_html=True)

        with c2:
            # --- GROWW STYLE CHART WITH ARROWS ---
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.75, 0.25])
            
            # 1. Candlestick
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], 
                                        increasing_line_color='#00d09c', decreasing_line_color='#eb5b5d',
                                        increasing_fillcolor='#00d09c', decreasing_fillcolor='#eb5b5d', name='Price'), row=1, col=1)
            
            # 2. Indicators
            if v_ema:
                fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], line=dict(color='#38bdf8', width=1.5), name='EMA 20'), row=1, col=1)
            
            # 3. AUTO ENTRY ARROWS (The Goli Chalao Points)
            # Plotting arrows where MACD crosses
            buy_points = df[(df['MACD'] > df['Signal']) & (df['MACD'].shift(1) <= df['Signal'].shift(1))]
            sell_points = df[(df['MACD'] < df['Signal']) & (df['MACD'].shift(1) >= df['Signal'].shift(1))]
            
            fig.add_trace(go.Scatter(x=buy_points.index, y=buy_points['Low'] * 0.999, mode='markers', 
                                     marker=dict(symbol='triangle-up', size=15, color='#00d09c'), name='Buy Arrow'), row=1, col=1)
            fig.add_trace(go.Scatter(x=sell_points.index, y=sell_points['High'] * 1.001, mode='markers', 
                                     marker=dict(symbol='triangle-down', size=15, color='#eb5b5d'), name='Sell Arrow'), row=1, col=1)

            if v_macd:
                colors = ['#00d09c' if val > 0 else '#eb5b5d' for val in (df['MACD'] - df['Signal'])]
                fig.add_trace(go.Bar(x=df.index, y=df['MACD']-df['Signal'], marker_color=colors, name='MACD Hist'), row=2, col=1)

            fig.update_layout(height=650, template="plotly_dark", xaxis_rangeslider_visible=False, 
                              margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='black', plot_bgcolor='black')
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=True, gridcolor='#111')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

target_m = st.selectbox("MARKET", ["NIFTY", "BANKNIFTY"], label_visibility="collapsed")
groww_terminal(target_m, tf_choice)
