import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import random
from datetime import datetime

# --- BRANDING & STYLE ---
st.set_page_config(page_title="GURI TRADER PB13 - SUPREME", layout="wide")
my_photo_url = "https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg" 

# Custom CSS for News Ticker & UI
st.markdown("""
    <style>
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker-wrap { background: #ff4b4b; color: white; padding: 10px; overflow: hidden; border-radius: 10px; font-weight: bold; margin-bottom: 20px;}
    .ticker-text { display: inline-block; white-space: nowrap; animation: ticker 25s linear infinite; }
    .stMetric { background-color: #1e1e1e; border: 1px solid #333; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ENGINE (Zero Lag Logic) ---
@st.cache_data(ttl=1)
def get_market_data(ticker):
    df = yf.download(ticker, period="1d", interval="1m", progress=False)
    if not df.empty and isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df

# --- SIDEBAR CONTROL ---
st.sidebar.image(my_photo_url, width=150)
st.sidebar.title("GURI CONTROL")
ticker_choice = st.sidebar.selectbox("Market", ["NIFTY 50", "BANK NIFTY"])
ticker = "^NSEI" if ticker_choice == "NIFTY 50" else "^NSEBANK"
risk_mode = st.sidebar.select_slider("Risk Protection Level", options=["Standard", "High", "Ultra-Safe"])

# --- PROCESSING ---
data = get_market_data(ticker)
vix_data = get_market_data("^INDIAVIX")

if not data.empty:
    S = float(data['Close'].iloc[-1])
    # Indicators (Hidden Backend)
    data['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
    vwap = data['VWAP'].iloc[-1]
    vol_avg = data['Volume'].rolling(10).mean().iloc[-1]
    vix = vix_data['Close'].iloc[-1] if not vix_data.empty else 15
    
    # --- DYNAMIC SENTIMENT LOGIC ---
    if S > vwap:
        status, color, icon, msg = "BULLISH ATTACK 🐂", "#00FF00", "🐂", "Bulls full power mein hain, trend ke sath chalo!"
    else:
        status, color, icon, msg = "BEARISH GRIP 🐻", "#FF3131", "🐻", "Bears ne dabocha hai, selling ka mauka dekho."

    # --- TOP NEWS TICKER ---
    st.markdown(f'<div class="ticker-wrap"><div class="ticker-text">🚨 GURI TRADER PB13 ALERT: Support at {round((S-100)/50)*50} | Resistance at {round((S+100)/50)*50} | VIX is {vix:.2f} | Trading System Locked & Loaded 🚨</div></div>', unsafe_allow_html=True)

    # --- MAIN HEADER ---
    st.markdown(f"""
        <div style='display: flex; align-items: center; background-color: #1e1e1e; padding: 20px; border-radius: 20px; border: 4px solid {color};'>
            <img src='{my_photo_url}' style='width: 90px; height: 90px; border-radius: 50%; border: 3px solid {color}; object-fit: cover; margin-right: 25px;'>
            <div>
                <h1 style='color: {color}; margin: 0;'>{status}</h1>
                <p style='color: #eee; font-size: 1.2rem; margin: 0;'>{msg}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- SIGNAL BOX (Triple Confirmation + AI) ---
    st.write("###")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Live LTP", f"₹{S:.2f}")
    c2.metric("VIX (Fear)", f"{vix:.2f}")
    c3.metric("Target", f"{round((S+70)/10)*10}")
    c4.metric("SL (Safety)", f"{round((S-35)/10)*10}")

    # --- SIGNAL GENERATOR ---
    st.divider()
    if S > vwap and data['Volume'].iloc[-1] > vol_avg:
        st.success(f"💎 **SIGNAL:** {ticker_choice} {round(S/50)*50} CE BUY (Confirmed by Volume & VWAP)")
    elif S < vwap and data['Volume'].iloc[-1] > vol_avg:
        st.error(f"📉 **SIGNAL:** {ticker_choice} {round(S/50)*50} PE BUY (Confirmed by Volume & VWAP)")
    else:
        st.warning("⚠️ **WAIT:** Fake move ho sakta hai ya volume kam hai. No clear signal.")

    # --- CHART ---
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name="Price")])
    fig.add_trace(go.Scatter(x=data.index, y=data['VWAP'], name="Guri's VWAP", line=dict(color='cyan', width=2)))
    fig.update_layout(height=550, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

    # --- CHULBULI TIPS ---
    tips = [
        "Arey bhai, profit ho gaya toh ghar leke jao, market ko wapas mat dena! 💰",
        "Overtrading mat karna, warna broker ameer ho jayega tum nahi! 😂",
        "Chart par dhyan do, padosi ki baaton par nahi! 📈",
        "Market aaj thoda 'nakhre' kar raha hai, thoda sabar rakho! 💃",
        "Stop-loss lagaya? Ki bina helmet ke bike chala rahe ho? ⛑️"
    ]
    st.info(f"💡 **Guri's Secret Tip:** {random.choice(tips)}")

else:
    st.error("Bhai, data nahi aa raha. Internet check karo ya refresh dabao!")
