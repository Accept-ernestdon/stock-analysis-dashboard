import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Financial Market Dashboard", layout="wide")

# ----------------------------
# HEADER (UPGRADED)
# ----------------------------
st.title("📊 Financial Market Analysis Dashboard")
st.markdown("### Built by Acceptable Ernest Donkoh")

st.markdown("""
This dashboard provides insights into stock performance using real financial data.
It includes trend analysis, moving averages, volatility (risk), and correlation between assets.
""")

# ----------------------------
# STOCK SELECTION
# ----------------------------
stocks = ['AAPL', 'MSFT', 'TSLA']

selected_stocks = st.multiselect(
    "Select Stocks",
    stocks,
    default=['AAPL', 'MSFT']  # cleaner default
)

# Prevent empty selection
if len(selected_stocks) == 0:
    st.warning("Please select at least one stock.")
    st.stop()

# ----------------------------
# LOAD DATA FUNCTION
# ----------------------------
@st.cache_data
def load_data(tickers):
    df = yf.download(tickers, start="2022-01-01", end="2025-01-01", progress=False)

    if df.empty:
        return None

    # Handle MultiIndex safely
    if isinstance(df.columns, pd.MultiIndex):
        df = df['Close']
    else:
        df = df[['Close']]

    return df

data = load_data(selected_stocks)

if data is None:
    st.error("Failed to load data. Please try again.")
    st.stop()

# ----------------------------
# SHOW DATA
# ----------------------------
st.subheader("📈 Latest Prices")
st.dataframe(data.tail())

# ----------------------------
# PRICE COMPARISON
# ----------------------------
st.subheader("📊 Stock Price Comparison")
st.line_chart(data)

# ----------------------------
# MOVING AVERAGES
# ----------------------------
st.subheader("📉 Moving Averages (Trend Indicator)")

selected_stock_ma = st.selectbox("Select Stock for Analysis", selected_stocks)

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
# RISK ANALYSIS (IMPROVED)
# ----------------------------
st.subheader("⚠️ Risk (Volatility)")

risk = returns.std()

st.dataframe(risk.rename("Volatility"))

# Highlight highest risk
highest_risk_stock = risk.idxmax()
st.markdown(f"🔴 **Highest Risk Stock:** {highest_risk_stock}")

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

st.markdown("""
- Compare multiple stocks side-by-side  
- Moving averages help identify trends and signals  
- Correlation shows relationships between stocks  
- Volatility indicates risk level of each stock  
""")

# ----------------------------
# FOOTER (PROFESSIONAL TOUCH)
# ----------------------------
st.markdown("---")
st.markdown("📌 *Data Source: Yahoo Finance | Built with Streamlit*")
