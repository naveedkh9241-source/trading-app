import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="Gold Live Trading Bot - Naveed")
st.title("Gold Live Trading Bot - Naveed")
st.markdown("Live BUY / SELL Signals - Abu Dhabi Time")

symbol = "GC=F"
df = yf.download(symbol, period="5d", interval="5m")

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

if len(df) < 50:
    st.warning("Market data loading, please wait...")
    st.stop()

close = df['Close']
if isinstance(close, pd.DataFrame):
    close = close.iloc[:, 0]

df['EMA9'] = ta.trend.ema_indicator(close, window=9)
df['EMA21'] = ta.trend.ema_indicator(close, window=21)
df['RSI'] = ta.momentum.rsi(close, window=14)

last = df.iloc[-1]
price = float(last['Close'])
ema9 = float(last['EMA9'])
ema21 = float(last['EMA21'])
rsi = float(last['RSI'])

st.metric("GOLD Price", f"${price:.2f}")
col1, col2, col3 = st.columns(3)
col1.metric("EMA9", f"{ema9:.2f}")
col2.metric("EMA21", f"{ema21:.2f}")
col3.metric("RSI", f"{rsi:.2f}")

if ema9 > ema21 and rsi > 50:
    st.success("BUY SIGNAL")
elif ema9 < ema21 and rsi < 50:
    st.error("SELL SIGNAL")
else:
    st.warning("WAIT / NEUTRAL")

st.line_chart(df[['Close', 'EMA9', 'EMA21']])
