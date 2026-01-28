import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ================= PAGE SETUP =================
st.set_page_config(page_title="Tesla Stock Analysis", layout="wide")
plt.style.use("dark_background")

# ================= LOAD DATA =================
train_df = pd.read_csv("TSLA training.csv")
test_df = pd.read_csv("TSLA Testing.csv")

df = pd.concat([train_df, test_df])
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")
df.set_index("Date", inplace=True)

# ================= SIDEBAR (VERY SIMPLE) =================
st.sidebar.title("🔍 Filters")

start_date = st.sidebar.date_input("Start Date", df.index.min())
end_date = st.sidebar.date_input("End Date", df.index.max())

show_ma = st.sidebar.checkbox("Show Moving Average", True)
show_risk = st.sidebar.checkbox("Show Risk Analysis", True)

df = df.loc[start_date:end_date]

# ================= TITLE =================
st.title("🚗 Tesla Stock Financial Analysis")
st.caption("Simple & clear dashboard for stock trend analysis")

# ================= KEY METRICS =================
c1, c2, c3 = st.columns(3)
c1.metric("Latest Price ($)", round(df["Close"].iloc[-1], 2))
c2.metric("Highest Price ($)", round(df["High"].max(), 2))
c3.metric("Lowest Price ($)", round(df["Low"].min(), 2))

# ================= PRICE TREND =================
st.subheader("📈 Price Trend")

fig, ax = plt.subplots(figsize=(10,4))
ax.plot(df.index, df["Close"], color="cyan", linewidth=2, label="Close Price")

if show_ma:
    df["MA20"] = df["Close"].rolling(20).mean()
    ax.plot(df.index, df["MA20"], color="yellow", linewidth=2, label="20-Day MA")

ax.set_xlabel("Date")
ax.set_ylabel("Price ($)")
ax.grid(alpha=0.3)
ax.legend()
st.pyplot(fig)

# ================= VOLUME =================
st.subheader("📊 Trading Volume")

fig, ax = plt.subplots(figsize=(10,3))
ax.bar(df.index, df["Volume"], color="orange")
ax.set_ylabel("Volume")
ax.grid(alpha=0.3)
st.pyplot(fig)

# ================= RISK ANALYSIS =================
if show_risk:
    st.subheader("📉 Risk Analysis")

    col1, col2 = st.columns(2)

    # Daily Returns
    df["Daily Return (%)"] = df["Close"].pct_change() * 100

    with col1:
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(df.index, df["Daily Return (%)"], color="lime")
        ax.axhline(0, color="white", linestyle="--")
        ax.set_title("Daily Returns (%)")
        ax.grid(alpha=0.3)
        st.pyplot(fig)

    # Volatility
    df["Volatility"] = df["Daily Return (%)"].rolling(20).std()

    with col2:
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(df.index, df["Volatility"], color="magenta")
        ax.set_title("Volatility (20 Days)")
        ax.grid(alpha=0.3)
        st.pyplot(fig)

# ================= DATA PREVIEW =================
st.subheader("📋 Recent Data")
st.dataframe(df.tail(10))
