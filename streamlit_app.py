import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import pytz
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=1000, key="live_clock")

st.set_page_config(page_title="Gold Live Bot - Naveed", page_icon="🪙")

dubai_tz = pytz.timezone('Asia/Dubai')
live_time = datetime.now(dubai_tz)
st.success(f"📍 Sharjah Area 6 | 🕒 Dubai Live: {live_time.strftime('%d-%m-%Y %H:%M:%S')} - Auto Updating")

st.title("Gold Live Trading Bot - Naveed")
st.markdown("Live BUY / SELL Signals - Sharjah (GMT+4)")

symbol = "GC=F"

try:
    df = yf.download(symbol, period="5d", interval="15m", auto_adjust=True)
    if df.empty:
        st.warning("Market data loading... Wait")
        st.stop()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    if len(df) < 50:
        st.warning("Not enough data")
        st.stop()

    df['RSI'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()
    last_price = float(df['Close'].iloc[-1])
    last_rsi = float(df['RSI'].iloc[-1])

    st.metric("Gold Price", f"${last_price:.2f}", f"RSI: {last_rsi:.1f}")

    if last_rsi >= 55:
        st.markdown(f'<div style="background:red;padding:25px;border-radius:15px;text-align:center"><h1 style="color:white">🔴 SELL NOW</h1><h2 style="color:white">RSI: {last_rsi:.1f}</h2></div>', unsafe_allow_html=True)
    elif last_rsi <= 45:
        st.markdown(f'<div style="background:green;padding:25px;border-radius:15px;text-align:center"><h1 style="color:white">🟢 BUY NOW</h1><h2 style="color:white">RSI: {last_rsi:.1f}</h2></div>', unsafe_allow_html=True)
    else:
        if last_rsi > 50:
            st.markdown(f'<div style="background:#ff7f7f;padding:25px;border-radius:15px;text-align:center"><h1 style="color:white">🔴 SELL (Weak)</h1><h2>RSI: {last_rsi:.1f}</h2></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:#90EE90;padding:25px;border-radius:15px;text-align:center"><h1 style="color:black">🟢 BUY (Weak)</h1><h2>RSI: {last_rsi:.1f}</h2></div>', unsafe_allow_html=True)

    st.write("---")
    st.dataframe(df.tail(10))

except Exception as e:
    st.error(f"Error: {e}")
