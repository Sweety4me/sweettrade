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

    # Download 30-day data with 1d interval
    try:
        df = yf.download(symbol, period="30d", interval="1d")

        if df.empty:
            st.error("No data found. Please check the symbol and try again.")
        else:
            # Calculate SMAs
            df['SMA_5'] = df['Close'].rolling(window=5).mean()
            df['SMA_20'] = df['Close'].rolling(window=20).mean()

            # Take last row for signal
            latest = df.iloc[-1]

            # Signal Logic
            if latest['SMA_5'] > latest['SMA_20']:
                signal = "📈 BUY Signal"
                st.success(f"{signal} - Short-term uptrend detected.")
            elif latest['SMA_5'] < latest['SMA_20']:
                signal = "📉 SELL Signal"
                st.error(f"{signal} - Short-term downtrend detected.")
            else:
                signal = "⚖️ HOLD"
                st.warning(f"{signal} - No clear trend yet.")

            # Show last 5 rows
            st.subheader("📅 Latest Stock Data")
            st.dataframe(df.tail(5))

            # Plot chart
            st.subheader("📈 Price & Moving Averages")
            fig, ax = plt.subplots()
            df[['Close', 'SMA_5', 'SMA_20']].plot(ax=ax, linewidth=2)
            ax.set_title(f"{symbol} - Close Price with SMA(5) & SMA(20)")
            ax.set_ylabel("Price")
            ax.grid(True)
            st.pyplot(fig)

    except Exception as e:
        st.exception(f"⚠️ Error fetching data: {e}")
