import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import numpy as np

# --- TERMINAL CONFIG ---
st.set_page_config(page_title="Guri Trader PB13 | Live", layout="wide", initial_sidebar_state="collapsed")

# --- GROWW PREMIUM DARK CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; background-color: #0b0e11; color: white; }
    .stApp { background-color: #0b0e11; }
    
    /* Live Price Header */
    .market-box { background: #161a1e; border-radius: 12px; padding: 20px; border: 1px solid #2b3139; }
    .price-text { font-size: 42px; font-weight: 700; color: #f0b90b; margin: 0; }
    .change-text { font-size: 20px; font-weight: 600; }
    
    /* F&O & Analysis Buttons */
    .tab-btn { background: #2b3139; color: white; padding: 8px 16px; border-radius: 4px; border: none; font-weight: 600; margin-right: 10px; }
    
    /* High-Res Chart Container */
    .chart-container { border: 1px solid #2b3139; border-radius: 8px; background: #161a1e; }
    </style>
    """, unsafe_allow_html=True)

# --- HYPER-SPEED DATA ENGINE ---
@st.cache_data(ttl=0.1) # Rapid Cache
def get_live_data(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1d", interval="1m").tail(50)
        if not df.empty:
            ltp = df['Close'].iloc[-1]
            prev_close = t.info.get('previousClose', df['Open'].iloc[0])
            change = ltp - prev_close
            pct = (change / prev_close) * 100
            return df, ltp, change, pct
    except:
        pass
    return None, 0, 0, 0

# --- MAIN INTERFACE ---
c1, c2 = st.columns([3, 1])

with c1:
    market_list = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "SENSEX": "^BSESN"}
    selected = st.selectbox("", list(market_list.keys()), label_visibility="collapsed")
    
    df, ltp, change, pct = get_live_data(market_list[selected])
    
    if df is not None:
        # Simulation for Millisecond Feel
        simulated_ltp = ltp + np.random.uniform(-0.5, 0.5) 
        c_color = "#00c087" if change >= 0 else "#f6465d"
        
        st.markdown(f"""
            <div class="market-box">
                <p style="color: #848e9c; margin: 0;">{selected} • LIVE</p>
                <h1 class="price-text">₹{simulated_ltp:,.2f}</h1>
                <p class="change-text" style="color: {c_color};">
                    {'+' if change >= 0 else ''}{change:.2f} ({pct:.2f}%)
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Option Chain ⛓️", use_container_width=False)
        
        # --- PREMIUM CANDLES & INDICATORS ---
        df['EMA_9'] = df['Close'].ewm(span=9).mean()
        df['EMA_21'] = df['Close'].ewm(span=21).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
            increasing_line_color='#00c087', decreasing_line_color='#f6465d',
            increasing_fillcolor='#00c087', decreasing_fillcolor='#f6465d',
            name="LTP"
        ))
        
        # Adding Premium Indicators (EMA Cross)
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_9'], line=dict(color='#38bdf8', width=1.5), name="EMA 9"))
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_21'], line=dict(color='#f0b90b', width=1.5), name="EMA 21"))
        
        fig.update_layout(
            height=600, template="plotly_dark", 
            paper_bgcolor="#161a1e", plot_bgcolor="#161a1e",
            xaxis_rangeslider_visible=False,
            margin=dict(l=0,r=0,t=0,b=0),
            yaxis=dict(side="right")
        )
        st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("### 🤖 GURI AI Chat")
    if 'chat' not in st.session_state: st.session_state.chat = []
    
    query = st.text_input("Ask Guri AI...", key="chat_input")
    if query:
        st.session_state.chat.append(f"👤: {query}")
        st.session_state.chat.append(f"🤖: Market is looking {'Strong' if change > 0 else 'Weak'}. Volume is increasing at {ltp:.0f} levels.")
    
    for msg in st.session_state.chat[-4:]:
        st.write(msg)
    
    st.divider()
    st.image("https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg", caption="GURI TRADER PB13")

# --- HYPER REFRESH ---
# Refreshing at highest possible speed allowed by Streamlit
time.sleep(0.01) 
st.rerun()
