import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go

st.set_page_config(page_title="AI Option Chain Pro", layout="wide")

# --- Black-Scholes Function for Greeks ---
def calculate_greeks(S, K, T, r, sigma, option_type="call"):
    if T <= 0 or sigma <= 0: return 0, 0, 0
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        delta = norm.cdf(d1)
        theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
    else:
        delta = norm.cdf(d1) - 1
        theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)
    
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    return round(delta, 2), round(gamma, 4), round(theta / 365, 2)

st.title("🎯 Advanced Option Chain AI")

ticker = st.sidebar.selectbox("Select Index", ["^NSEI", "^NSEBANK"])
data = yf.download(ticker, period="2d", interval="5m", progress=False)

if not data.empty:
    S = data['Close'].iloc[-1] # Current Spot Price
    st.subheader(f"Current {ticker} Spot: ₹{S:.2f}")

    # Dummy strike selection for Logic (Simplification for Free API)
    atm_strike = round(S / 50) * 50 if "^NSEI" in ticker else round(S / 100) * 100
    
    st.write(f"### 📊 Option Analysis (ATM Strike: {atm_strike})")
    
    # Assumptions for Calculation (Since Free API doesn't give Live IV)
    r = 0.07 # 7% Interest rate
    iv = 0.15 # 15% Standard IV
    T = 4 / 365 # 4 days to expiry (assumption)

    c_delta, c_gamma, c_theta = calculate_greeks(S, atm_strike, T, r, iv, "call")
    p_delta, p_gamma, p_theta = calculate_greeks(S, atm_strike, T, r, iv, "put")

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"🟢 CALL Side ({atm_strike} CE)")
        st.write(f"**Delta:** {c_delta} | **Theta:** {c_theta}")
        st.write(f"**Gamma:** {c_gamma}")
    
    with col2:
        st.error(f"🔴 PUT Side ({atm_strike} PE)")
        st.write(f"**Delta:** {p_delta} | **Theta:** {p_theta}")
        st.write(f"**Gamma:** {p_gamma}")

    st.divider()
    # Strategy Logic
    if c_delta > 0.55:
        st.balloons()
        st.header("🔥 AI SIGNAL: BUY CALL (Strong Bullish)")
    elif p_delta < -0.55:
        st.header("🧊 AI SIGNAL: BUY PUT (Strong Bearish)")
    else:
        st.info("⌛ AI SIGNAL: MARKET SIDEWAYS - Avoid Options")

else:
    st.error("Market data fetch nahi ho raha.")
