import sys
import os

# Add project root to PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

import streamlit as st
import plotly.express as px

from backend.database import load_symbol, resample
from backend.analytics import (
    price_stats,
    hedge_ratio,
    spread,
    zscore,
    rolling_corr,
    adf_test
)
from backend.alerts import zscore_alert
from backend.config import TIMEFRAMES

st.set_page_config(layout="wide")
st.title("Real-Time Quant Analytics Dashboard")

symbols = ["btcusdt", "ethusdt"]

sym_y = st.selectbox("Symbol Y", symbols)
sym_x = st.selectbox("Symbol X", symbols)
tf = st.selectbox("Timeframe", list(TIMEFRAMES.keys()))
window = st.slider("Rolling Window", 10, 100, 30)
alert_level = st.number_input("Z-score Alert", value=2.0)

df_y = resample(load_symbol(sym_y), TIMEFRAMES[tf])
df_x = resample(load_symbol(sym_x), TIMEFRAMES[tf])

if df_y.empty or df_x.empty:
    st.warning("Waiting for live data...")
    st.stop()

beta = hedge_ratio(df_y["price"], df_x["price"])
spr = spread(df_y["price"], df_x["price"], beta)
z = zscore(spr, window)
corr = rolling_corr(df_y["price"], df_x["price"], window)

alert = zscore_alert(z, alert_level)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Price")
    st.plotly_chart(px.line(df_y, y="price"), use_container_width=True)

with col2:
    st.subheader("Z-Score")
    st.plotly_chart(px.line(z), use_container_width=True)

st.subheader("Rolling Correlation")
st.plotly_chart(px.line(corr), use_container_width=True)

st.subheader("Price Stats")
st.json(price_stats(df_y["price"]))

st.subheader("ADF Test")
st.json(adf_test(spr))

if alert:
    st.error(alert)

st.subheader("Download Data")
st.download_button("Download CSV", spr.to_csv(), "spread.csv")
