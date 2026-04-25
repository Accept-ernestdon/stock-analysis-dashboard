import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Advanced Stock Dashboard", layout="wide")

st.title("📊 Advanced Stock Market Dashboard")

st.markdown("Analyze multiple stocks, trends, and risk in one place.")

# ----------------------------
# STOCK SELECTION (MULTI)
# ----------------------------
stocks = ['AAPL', 'MSFT', 'TSLA']
selected_stocks = st.multiselect("Select Stocks", stocks, default=stocks)

# ----------------------------
# LOAD DATA FUNCTION
# ----------------------------
@st.cache_data
def load_data(tickers):
    df = yf.download(tickers, start="2022-01-01", end="2025-01-01", progress=False)
    
    if df.empty:
        return None
    
    # Get Close prices only
    if isinstance(df.columns, pd.MultiIndex):
        df = df['Close']
    else:
        df = df[['Close']]
    
    return df

data = load_data(selected_stocks)

if data is None:
    st.error("Failed to load data")
    st.stop()

# ----------------------------
# SHOW DATA
# ----------------------------
st.subheader("📈 Latest Prices")
st.write(data.tail())

# ----------------------------
# PRICE COMPARISON
# ----------------------------
st.subheader("📊 Stock Price Comparison")

st.line_chart(data)

# ----------------------------
# MOVING AVERAGES
# ----------------------------
st.subheader("📉 Moving Averages (Trend Indicator)")

selected_stock_ma = st.selectbox("Select Stock for MA", selected_stocks)

ma_data = data[selected_stock_ma]

ma_20 = ma_data.rolling(window=20).mean()
ma_50 = ma_data.rolling(window=50).mean()

fig, ax = plt.subplots()
ax.plot(ma_data.index, ma_data, label="Price")
ax.plot(ma_20.index, ma_20, label="20-day MA")
ax.plot(ma_50.index, ma_50, label="50-day MA")

ax.legend()
ax.set_title(f"{selected_stock_ma} Moving Averages")

st.pyplot(fig)

# ----------------------------
# RETURNS
# ----------------------------
returns = data.pct_change().dropna()

st.subheader("📉 Daily Returns")
st.line_chart(returns)

# ----------------------------
# CORRELATION HEATMAP
# ----------------------------
st.subheader("🔥 Correlation Between Stocks")

corr = returns.corr()

fig, ax = plt.subplots()
cax = ax.matshow(corr)
plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
plt.yticks(range(len(corr.columns)), corr.columns)
fig.colorbar(cax)

st.pyplot(fig)

# ----------------------------
# RISK ANALYSIS
# ----------------------------
st.subheader("⚠️ Risk (Volatility)")

risk = returns.std()

st.write(risk)

# ----------------------------
# DOWNLOAD BUTTON
# ----------------------------
st.subheader("📁 Download Data")

csv = data.to_csv().encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name='stock_data.csv',
    mime='text/csv'
)

# ----------------------------
# INSIGHTS
# ----------------------------
st.subheader("🧠 Insights")

st.write("""
- Compare multiple stocks side-by-side  
- Moving averages show trend direction  
- Correlation shows how stocks move together  
- Volatility indicates risk level  
""")