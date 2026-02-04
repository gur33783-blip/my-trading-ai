import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. PREMIUM CSS & UI ---
st.set_page_config(page_title="GURI GHOST V7.1 PREMIUM", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
    :root { --gold: #f0b90b; --bg: #030303; --green: #02c076; --red: #f84960; --sky: #38bdf8; }
    .stApp { background-color: var(--bg); color: #e9eaeb; }
    
    /* Premium Price Box */
    .price-box { 
        background: linear-gradient(145deg, #0d0d0d, #1a1a1a);
        padding: 30px; border-radius: 25px; border: 1px solid #333; 
        text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }
    .price-val { font-family: 'JetBrains Mono'; font-size: 58px; color: var(--gold); font-weight: 800; }
    
    /* Sniper Alert Animation */
    .sniper-box {
        padding: 20px; border-radius: 20px; text-align: center;
        font-weight: 800; font-size: 24px; border: 2px solid #333; margin-top: 20px;
    }
    .bull-logo { color: var(--green); text-shadow: 0 0 15px rgba(2,192,118,0.5); font-size: 40px; }
    .bear-logo { color: var(--red); text-shadow: 0 0 15px rgba(248,73,96,0.5); font-size: 40px; }
    
    .st-emotion-cache-1r6lb05 { background: #111; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ADVANCED DATA ENGINE (PAID INDICATORS) ---
@st.cache_data(ttl=1)
def get_premium_data(idx, interval):
    try:
        sym = "^NSEI" if idx == "NIFTY" else "^NSEBANK"
        t = yf.Ticker(sym)
        hist = t.history(period="5d", interval=interval)
        
        # 1. EMA Cloud (20, 50, 200)
        hist['EMA20'] = hist['Close'].ewm(span=20, adjust=False).mean()
        hist['EMA50'] = hist['Close'].ewm(span=50, adjust=False).mean()
        
        # 2. MACD
        exp1 = hist['Close'].ewm(span=12, adjust=False).mean()
        exp2 = hist['Close'].ewm(span=26, adjust=False).mean()
        hist['MACD'] = exp1 - exp2
        hist['Signal'] = hist['MACD'].ewm(span=9, adjust=False).mean()
        
        # 3. Bollinger Bands
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
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:3px solid var(--gold); margin-bottom:10px;">""", unsafe_allow_html=True)
    st.title("🎯 GURI GHOST PRO")
    st.divider()
    st.subheader("🛠️ PREMIUM TOOLS")
    v_macd = st.checkbox("MACD Indicator", value=True)
    v_ema = st.checkbox("EMA Cloud (20/50)", value=True)
    v_bb = st.checkbox("Bollinger Bands", value=True)
    st.divider()
    st.info("Bhai, har 1 sec mein AI sectors aur trends scan kar raha hai.")

# --- 4. MAIN TERMINAL DASHBOARD ---
tf = st.select_slider("⚡ TIMEFRAME SLIDER", options=["1m", "5m", "15m", "30m", "1h"], value="5m")

@st.fragment(run_every=1)
def render_pro_terminal(idx_name, timeframe):
    data = get_premium_data(idx_name, timeframe)
    if data:
        df = data['df']
        
        c1, c2 = st.columns([1.3, 3])
        
        with c1:
            st.markdown(f"""
                <div class="price-box">
                    <p style="margin:0; color:#888; font-weight:800;">{idx_name} PREMIUM FEED</p>
                    <div class="price-val">₹{data['price']:,.2f}</div>
                    <p style="font-size:24px; color:{'#02c076' if data['change']>0 else '#f84960'}; font-weight:800;">{data['change']:+.2f}%</p>
                </div>
            """, unsafe_allow_html=True)
            
            # --- SUPER SNIPER LOGIC (BULL & BEAR) ---
            last_macd = df['MACD'].iloc[-1]
            last_signal = df['Signal'].iloc[-1]
            last_close = df['Close'].iloc[-1]
            ema20 = df['EMA20'].iloc[-1]
            
            st.markdown("### 🏹 SNIPER RADAR")
            if last_macd > last_signal and last_close > ema20:
                st.markdown(f"""
                    <div class="sniper-box" style="background:rgba(2,192,118,0.1); border-color:#02c076;">
                        <div class="bull-logo">🐂 BULL ATTACK</div>
                        <span style="color:#02c076;">CALL ENTRY CONFIRMED</span><br>
                        <span style="font-size:12px; color:#888;">MACD Crossover + EMA Support</span>
                    </div>
                """, unsafe_allow_html=True)
            elif last_macd < last_signal and last_close < ema20:
                st.markdown(f"""
                    <div class="sniper-box" style="background:rgba(248,73,96,0.1); border-color:#f84960;">
                        <div class="bear-logo">🐻 BEAR TRAP</div>
                        <span style="color:#f84960;">PUT ENTRY CONFIRMED</span><br>
                        <span style="font-size:12px; color:#888;">MACD Breakdown + EMA Resistance</span>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""<div class="sniper-box">⌛ SCANNING...<br><span style='font-size:14px; color:#666;'>No Clear Trend</span></div>""", unsafe_allow_html=True)

        with col2:
            # --- PRO MULTI-CHART ---
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.7, 0.3])
            
            # Candlestick
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Price'), row=1, col=1)
            
            # Premium Indicators
            if v_ema:
                fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], line=dict(color='#38bdf8', width=1.5), name='EMA 20'), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=df['EMA50'], line=dict(color='#f0b90b', width=1.5), name='EMA 50'), row=1, col=1)
            
            if v_bb:
                fig.add_trace(go.Scatter(x=df.index, y=df['Upper'], line=dict(color='rgba(255,255,255,0.1)', width=1), name='BB Upper'), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=df['Lower'], line=dict(color='rgba(255,255,255,0.1)', width=1), fill='tonexty', name='BB Lower'), row=1, col=1)

            # MACD Chart
            if v_macd:
                fig.add_trace(go.Bar(x=df.index, y=df['MACD']-df['Signal'], name='Histogram', marker_color='gray'), row=2, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], line=dict(color='#02c076', width=2), name='MACD'), row=2, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=df['Signal'], line=dict(color='#f84960', width=2), name='Signal'), row=2, col=1)

            fig.update_layout(height=650, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

render_pro_terminal(st.selectbox("MARKET", ["NIFTY", "BANKNIFTY"], label_visibility="collapsed"), tf)
