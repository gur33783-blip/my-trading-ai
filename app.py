# --- SAB KUCH MERGE KAR DIYA HAI (OLD + NEW) ---
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Branding (Wahi Purani Photo)
st.set_page_config(page_title="GURI TRADER PB13 - SUPREME", layout="wide")
my_photo_url = "https://i.ibb.co/ZRDTjDgT/f9f75864-c999-4d88-ad0f-c89b2e65dffc.jpg"

# Side Menu for Switching (Sab features yahi hain)
st.sidebar.image(my_photo_url, width=100)
mode = st.sidebar.selectbox("Kya Dekhna Hai?", ["Sab Kuch (All-in-One)", "Scalping Mode", "Institutional View"])
ticker = st.sidebar.selectbox("Market", ["^NSEI", "^NSEBANK"])

# Data Fetching with NO-DELAY Logic
@st.cache_data(ttl=2) # 2 second refresh
def get_live_data(symbol):
    d = yf.download(symbol, period="1d", interval="1m", progress=False)
    if not d.empty and isinstance(d.columns, pd.MultiIndex): d.columns = d.columns.get_level_values(0)
    return d

data = get_live_data(ticker)

if not data.empty:
    S = float(data['Close'].iloc[-1])
    # Indicators (Old + New)
    data['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
    data['EMA_20'] = data['Close'].ewm(span=20).mean()
    
    # --- ALL-IN-ONE DASHBOARD ---
    if mode == "Sab Kuch (All-in-One)":
        st.header("🚀 GURI MASTER DASHBOARD")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("LIVE", f"₹{S:.2f}")
        with col2: st.success(f"PUT OI SUPPORT: {round((S-100)/100)*100}")
        with col3: st.error(f"CALL OI RESISTANCE: {round((S+100)/100)*100}")

        # Final Signal with Fake Move Check
        vol_avg = data['Volume'].rolling(10).mean().iloc[-1]
        if S > data['VWAP'].iloc[-1] and data['Volume'].iloc[-1] > vol_avg:
            st.success(f"💎 JACKPOT BUY: {round(S/50)*50} CE (Volume Confirmed)")
        elif S < data['VWAP'].iloc[-1] and data['Volume'].iloc[-1] > vol_avg:
            st.error(f"📉 JACKPOT SELL: {round(S/50)*50} PE (Volume Confirmed)")
        else:
            st.warning("⚠️ FAKE MOVE ALERT: Volume kam hai, wait karo.")

    # --- CHART ---
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
    fig.add_trace(go.Scatter(x=data.index, y=data['VWAP'], name="VWAP", line=dict(color='cyan')))
    fig.update_layout(height=600, template="plotly_dark", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
