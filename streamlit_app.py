import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="Gold Live Trading Bot", layout="centered")
st.title("Gold Live Trading Bot - Naveed")
st.markdown("Live BUY / SELL Signals - Abu Dhabi (GMT+4)")

symbol = "GC=F"

try:
    df = yf.download(symbol, period="5d", interval="15m", auto_adjust=True, progress=False)
    
    if df.empty:
        st.warning("Market data loading... Yahoo is slow, please wait 30 sec and refresh.")
        st.stop()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    if len(df) < 50:
        st.warning("Not enough data yet. Refresh after 1 minute.")
        st.stop()

    close = df['Close']
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    df['EMA9'] = ta.trend.ema_indicator(close, window=9)
    df['EMA21'] = ta.trend.ema_indicator(close, window=21)
    df['RSI'] = ta.momentum.rsi(close, window=14)

    df = df.dropna()
    last = df.iloc[-1]
    prev = df.iloc[-2]

    price = float(last['Close'])
    ema9 = float(last['EMA9'])
    ema21 = float(last['EMA21'])
    rsi = float(last['RSI'])

    st.metric("Gold Price", f"${price:.2f}")

    # Signal Logic
    if ema9 > ema21 and prev['EMA9'] <= prev['EMA21'] and rsi > 50:
        st.success(f"🟢 BUY SIGNAL - Price ${price:.2f} | RSI {rsi:.1f}")
    elif ema9 < ema21 and prev['EMA9'] >= prev['EMA21'] and rsi < 50:
        st.error(f"🔴 SELL SIGNAL - Price ${price:.2f} | RSI {rsi:.1f}")
    else:
        st.info(f"🟡 WAIT - No clear signal. RSI {rsi:.1f}")

    st.dataframe(df.tail(10))

except Exception as e:
    st.error(f"Error: {e}")
    st.info("Please refresh after 30 seconds. Yahoo data is busy.")
