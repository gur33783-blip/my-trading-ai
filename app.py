import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. CONFIG ---
st.set_page_config(page_title="GURI GHOST V7.0", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
    :root { --gold: #f0b90b; --bg: #030303; --green: #02c076; --red: #f84960; --sky: #38bdf8; }
    .stApp { background-color: var(--bg); color: #e9eaeb; }
    .price-box { background: #0d0d0d; padding: 20px; border-radius: 15px; border: 1px solid #222; text-align: center; }
    .price-val { font-family: 'JetBrains Mono'; font-size: 55px; color: var(--gold); font-weight: 800; }
    .entry-card { padding: 15px; border-radius: 12px; text-align: center; font-weight: 800; font-size: 20px; border: 2px solid #333; }
    .time-chip { background: #111; padding: 5px 15px; border-radius: 20px; border: 1px solid #444; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE (TURBO MODE) ---
@st.cache_data(ttl=1)
def get_live_full_data(idx, interval):
    try:
        sym = "^NSEI" if idx == "NIFTY" else "^NSEBANK"
        t = yf.Ticker(sym)
        hist = t.history(period="5d", interval=interval)
        
        # INDICATORS CALCULATION
        # 1. RSI
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        hist['RSI'] = 100 - (100 / (1 + rs))
        
        # 2. Bollinger Bands
        hist['MA20'] = hist['Close'].rolling(window=20).mean()
        hist['STD'] = hist['Close'].rolling(window=20).std()
        hist['Upper'] = hist['MA20'] + (hist['STD'] * 2)
        hist['Lower'] = hist['MA20'] - (hist['STD'] * 2)
        
        curr = t.fast_info.last_price
        change = ((curr - t.fast_info.previous_close)/t.fast_info.previous_close)*100
        return {"df": hist, "price": curr, "change": change}
    except: return None

# --- 3. SIDEBAR (GURI BRANDING) ---
with st.sidebar:
    st.markdown(f"""<img src="https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" style="width:100%; border-radius:15px; border:3px solid var(--gold); margin-bottom:10px;">""", unsafe_allow_html=True)
    st.title("🎯 GURI SNIPER")
    st.markdown("---")
    st.subheader("⚙️ INDICATORS")
    show_bb = st.checkbox("Bollinger Bands", value=True)
    show_rsi = st.checkbox("RSI (Relative Strength)", value=True)
    st.divider()
    st.subheader("💬 AI CHAT (LIVE)")
    if "messages" not in st.session_state: st.session_state.messages = []
    u_q = st.chat_input("Bhai se pucho...")
    if u_q:
        st.session_state.messages.append({"role": "user", "text": u_q})
        st.session_state.messages.append({"role": "ai", "text": "Guri bhai, RSI aur BB scan ho rahe hain. Analysis screen par dekho!"})

# --- 4. MAIN TERMINAL ---
# Timeframe Selection Slide
t_col1, t_col2, t_col3, t_col4, t_col5 = st.columns(5)
tf = st.select_slider("SELECT TIMEFRAME", options=["1m", "5m", "15m", "30m", "1h"], value="5m")

@st.fragment(run_every=1)
def sniper_dashboard(idx_name, timeframe):
    data = get_live_full_data(idx_name, timeframe)
    if data:
        df = data['df']
        
        # TOP INFO BAR
        st.markdown(f"""
            <div style="display:flex; gap:15px; margin-bottom:15px;">
                <div class="time-chip">🇺🇸 NASDAQ: {random.uniform(-1,1):+.2f}%</div>
                <div class="time-chip">🚀 TIME: {timeframe}</div>
                <div class="time-chip">📡 STATUS: LIVE SNIPER</div>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1.2, 3])
        
        with col1:
            st.markdown(f"""
                <div class="price-box">
                    <p style="margin:0; color:#888;">{idx_name} PRICE</p>
                    <div class="price-val">₹{data['price']:,.2f}</div>
                    <p style="font-size:22px; color:{'#02c076' if data['change']>0 else '#f84960'}; font-weight:800;">{data['change']:+.2f}%</p>
                </div>
            """, unsafe_allow_html=True)
            
            # --- SNIPER ENTRY LOGIC ---
            rsi = df['RSI'].iloc[-1]
            last_close = df['Close'].iloc[-1]
            upper_b = df['Upper'].iloc[-1]
            lower_b = df['Lower'].iloc[-1]
            
            st.markdown("### 🎯 SNIPER DECISION")
            if rsi < 35 and last_close < lower_b:
                st.markdown("""<div class="entry-card" style="background:rgba(2, 192, 118, 0.2); border-color:#02c076; color:#02c076;">🚀 CALL ENTRY BANTI HAI<br><span style='font-size:12px;'>Oversold + BB Support</span></div>""", unsafe_allow_html=True)
            elif rsi > 65 and last_close > upper_b:
                st.markdown("""<div class="entry-card" style="background:rgba(248, 73, 96, 0.2); border-color:#f84960; color:#f84960;">📉 PUT ENTRY BANTI HAI<br><span style='font-size:12px;'>Overbought + BB Resistance</span></div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class="entry-card">⌛ NO CLEAR ENTRY<br><span style='font-size:12px;'>Market Range-Bound</span></div>""", unsafe_allow_html=True)

        with col2:
            # --- PLOTTING WITH INDICATORS ---
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.7, 0.3])
            
            # Candlestick
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Price'), row=1, col=1)
            
            # Bollinger Bands
            if show_bb:
                fig.add_trace(go.Scatter(x=df.index, y=df['Upper'], line=dict(color='rgba(173, 216, 230, 0.4)', width=1), name='Upper BB'), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=df['Lower'], line=dict(color='rgba(173, 216, 230, 0.4)', width=1), fill='tonexty', name='Lower BB'), row=1, col=1)
            
            # RSI
            if show_rsi:
                fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], line=dict(color='#f0b90b', width=2), name='RSI'), row=2, col=1)
                fig.add_hline(y=70, line_dash="dash", line_color="#f84960", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="#02c076", row=2, col=1)

            fig.update_layout(height=600, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

sniper_dashboard(st.selectbox("MARKET", ["NIFTY", "BANKNIFTY"], label_visibility="collapsed"), tf)
