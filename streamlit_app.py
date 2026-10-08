import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="Gold Live Trading Bot - Naveed", layout="wide")
st.title("Gold Live Trading Bot - Naveed")
st.markdown("Live BUY / SELL Signals - Abu Dhabi - Gulf Time")

symbol = "GC=F"
df = yf.download(symbol, period="1d", interval="5m")

if len(df) < 50:
    st.warning("Market data loading, please refresh in 1 min")
    st.stop()

close = df['Close']
if isinstance(close, pd.DataFrame):
    close = close.iloc[:, 0]

df['EMA9'] = ta.trend.ema_indicator(close, window=9)
df['EMA21'] = ta.trend.ema_indicator(close, window=21)
df['RSI'] = ta.momentum.rsi(close, window=14)

price = float(close.iloc[-1])
ema9 = float(df['EMA9'].iloc[-1])
ema21 = float(df['EMA21'].iloc[-1])
rsi = float(df['RSI'].iloc[-1])

st.metric("GOLD Price", f"${price:.2f}")

col1, col2, col3 = st.columns(3)
col1.metric("EMA 9", f"{ema9:.2f}")
col2.metric("EMA 21", f"{ema21:.2f}")
col3.metric("RSI", f"{rsi:.2f}")

if ema9 > ema21 and rsi > 50 and rsi < 70:
    st.success("### 🟢 BUY SIGNAL")
elif ema9 < ema21 and rsi < 50 and rsi > 30:
    st.error("### 🔴 SELL SIGNAL")
else:
    st.info("### 🟡 WAIT SIGNAL")

st.line_chart(df[['Close','EMA9','EMA21']].tail(100))
st.dataframe(df.tail(10))
