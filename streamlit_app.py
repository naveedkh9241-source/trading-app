import streamlit as st
import yfinance as yf
import ta
st.set_page_config(page_title="Gold Bot", layout="wide")
st.title("Gold Live Trading Bot - Naveed")
st.markdown("Live BUY / SELL Signals - Abu Dhabi")
symbol = st.sidebar.selectbox("Symbol", ["GC=F", "XAUUSD=X", "EURUSD=X", "BTC-USD"])
@st.cache_data(ttl=60)
def get_data(sym):
    return yf.download(sym, period="5d", interval="15m", auto_adjust=True)
df = get_data(symbol)
df['EMA9'] = ta.trend.ema_indicator(df['Close'], window=9)
df['EMA21'] = ta.trend.ema_indicator(df['Close'], window=21)
df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
df.dropna(inplace=True)
close = float(df['Close'].iloc[-1])
ema9 = float(df['EMA9'].iloc[-1])
ema21 = float(df['EMA21'].iloc[-1])
rsi = float(df['RSI'].iloc[-1])
if ema9 > ema21 and rsi > 55:
    signal = "STRONG BUY"
elif ema9 < ema21 and rsi < 45:
    signal = "STRONG SELL"
else:
    signal = "WAIT"
c1,c2,c3,c4 = st.columns(4)
c1.metric("Price", f"${close:.2f}")
c2.metric("EMA9", f"${ema9:.2f}")
c3.metric("EMA21", f"${ema21:.2f}")
c4.metric("RSI", f"{rsi:.2f}")
st.header(signal)
st.line_chart(df[['Close','EMA9','EMA21']].tail(100))
