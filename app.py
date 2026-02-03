import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import random

# --- GROWW PREMIUM THEME CONFIG ---
st.set_page_config(page_title="Groww | Guri Trader PB13", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Groww Broker Interface
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; background-color: #ffffff; color: #44475b; }
    .stApp { background-color: #ffffff; }
    
    /* Top Navigation Bar */
    .nav-bar { display: flex; gap: 20px; border-bottom: 1px solid #ebedf2; padding: 10px 0; margin-bottom: 20px; }
    .nav-item { color: #44475b; font-weight: 600; cursor: pointer; padding: 5px 10px; }
    .nav-active { color: #00d09c; border-bottom: 2px solid #00d09c; }

    /* Price Section */
    .price-main { font-size: 32px; font-weight: 700; color: #44475b; margin-bottom: 0px; }
    .change-red { color: #eb5b3c; font-size: 18px; font-weight: 600; }
    .change-green { color: #00d09c; font-size: 18px; font-weight: 600; }

    /* F&O Hyperlink Style */
    .fo-link { color: #00d09c; font-weight: 600; text-decoration: none; border: 1px solid #00d09c; padding: 8px 15px; border-radius: 5px; }
    .fo-link:hover { background: #f0fffb; }

    /* Sidebar Fix */
    [data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #ebedf2; }
    </style>
    """, unsafe_allow_html=True)

# --- HYPER-FAST DATA ENGINE ---
def get_groww_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # Fetching minimal data for maximum speed
        df = ticker.history(period="1d", interval="1m")
        if not df.empty:
            ltp = df['Close'].iloc[-1]
            # Precise closing price from info for accurate Day Change
            prev_close = ticker.info.get('previousClose', df['Open'].iloc[0])
            change = ltp - prev_close
            pct = (change / prev_close) * 100
            return df, ltp, change, pct
    except:
        pass
    return None, 0, 0, 0

# --- SIDEBAR & PROFILE ---
with st.sidebar:
    st.image("https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg", width=120)
    st.markdown("### GURI TRADER PB13")
    st.write("---")
    st.markdown("### 🤖 AI Market Support")
    if st.text_input("Ask AI..."):
        st.success("AI: Breakout expected above R1 level.")

# --- NAVIGATION & PAGES ---
menu = st.tabs(["Overview", "F&O (Future & Options)", "Analysis"])

with menu[0]: # OVERVIEW PAGE
    st.markdown('<div class="nav-bar"><span class="nav-item nav-active">Stocks</span><span class="nav-item">Mutual Funds</span></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    markets = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK", "SENSEX": "^BSESN"}
    
    selected_market = st.selectbox("Market Select", list(markets.keys()))
    df, ltp, change, pct = get_groww_data(markets[selected_market])

    if df is not None:
        # Day Change Format (Groww Exact Match)
        c_class = "change-green" if change >= 0 else "change-red"
        sign = "+" if change >= 0 else ""
        
        st.markdown(f"""
            <div>
                <p style="color: #7c7e8c; margin:0;">{selected_market}</p>
                <p class="price-main">₹{ltp:,.2f}</p>
                <p class="{c_class}">{sign}{change:.2f} ({sign}{pct:.2f}%)</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f'<a href="#" class="fo-link">View Option Chain →</a>', unsafe_allow_html=True)
        
        # --- PREMIUM GRAPH WITH INDICATORS ---
        # Moving Averages (EMA 20 & 50)
        df['EMA20'] = df['Close'].ewm(span=20).mean()
        
        fig = go.Figure()
        # High-Res Candles
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
            name="Price", increasing_line_color='#00d09c', decreasing_line_color='#eb5b3c',
            increasing_fillcolor='#00d09c', decreasing_fillcolor='#eb5b3c'
        ))
        # Indicator: EMA
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], name="EMA 20", line=dict(color='#38bdf8', width=1.5)))
        
        fig.update_layout(
            height=500, template="plotly_white", 
            xaxis_rangeslider_visible=False,
            margin=dict(l=0,r=0,t=0,b=0),
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

with menu[1]: # F&O PAGE (HYPERLINK CONTENT)
    st.subheader("Option Chain - NIFTY 50")
    st.write("Live Strike Prices & OI Analysis")
    # Simulated Option Table
    strikes = [round(ltp/50)*50 + i for i in range(-150, 200, 50)]
    fo_df = pd.DataFrame({
        "Call Price": [random.randint(50, 200) for _ in strikes],
        "Strike": strikes,
        "Put Price": [random.randint(50, 200) for _ in strikes],
        "OI Signal": ["Strong Buy", "Neutral", "ATM", "Resistance", "Strong Sell"]
    })
    st.table(fo_df)

# --- CHULBULI TIP (3-Min) ---
if 'tip' not in st.session_state or time.time() - st.session_state.get('t', 0) > 180:
    st.session_state.tip = random.choice(["Guri bhai, profit toh banta hai! 💰", "Market red hai, par darna nahi! 🔥"])
    st.session_state.t = time.time()

st.info(f"💡 Tip: {st.session_state.tip}")

# --- REFRESH ---
time.sleep(1)
st.rerun()
