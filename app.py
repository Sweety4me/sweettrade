import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="SweetTrade - Signal App", page_icon="💹", layout="centered")

# Branding
st.image("https://img.icons8.com/?size=256&id=85078&format=png", width=60)
st.markdown("## 💹 SweetTrade: Bava's Advanced Trading Tool")

# Input box
symbol = st.text_input("Enter Stock Symbol (e.g., TATAMOTORS.NS)")

if st.button("Get Signal") and symbol:
    st.info("📊 Fetching stock data...")

    try:
        # Fetch 30 days of data with 1-day intervals
        df = yf.download(symbol, period="30d", interval="1d")
        
        # Check if data is empty
        if df.empty:
            st.error("No data found. Please check the symbol and try again.")
        else:
            # Calculate the Simple Moving Averages (SMA)
            df['SMA_5'] = df['Close'].rolling(window=5).mean()
            df['SMA_20'] = df['Close'].rolling(window=20).mean()

            # Get the latest row (last trading day)
            latest = df.iloc[-1]

            # Signal Logic based on SMA comparison
            # Use the latest values for SMA_5 and SMA_20
            sma_5_latest = latest['SMA_5']
            sma_20_latest = latest['SMA_20']

            # Now compare the values directly (latest values only)
            if sma_5_latest > sma_20_latest:
                signal = "📈 BUY Signal"
                st.success(f"{signal} - Short-term uptrend detected.")
            elif sma_5_latest < sma_20_latest:
                signal = "📉 SELL Signal"
                st.error(f"{signal} - Short-term downtrend detected.")
            else:
                signal = "⚖️ HOLD"
                st.warning(f"{signal} - No clear trend yet.")

            # Show the latest 5 rows of the data
            st.subheader("📅 Latest Stock Data")
            st.dataframe(df.tail(5))

            # Plot Close Price and SMAs
            st.subheader("📈 Price & Moving Averages")
            fig, ax = plt.subplots()
            df[['Close', 'SMA_5', 'SMA_20']].plot(ax=ax, linewidth=2)
            ax.set_title(f"{symbol} - Close Price with SMA(5) & SMA(20)")
            ax.set_ylabel("Price")
            ax.grid(True)
            st.pyplot(fig)

    except Exception as e:
        st.exception(f"⚠️ Error: {e}")  # Displaying the actual error message
