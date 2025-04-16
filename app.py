import streamlit as st
import yfinance as yf
import pandas as pd

# Title and branding
st.image("https://img.icons8.com/?size=256&id=85078&format=png", width=60)
st.markdown("## 💹 SweetTrade: Bava's Advanced Trading Tool")

# Input box
symbol = st.text_input("Enter Stock Symbol (e.g., TATAMOTORS.NS)")

if st.button("Get Signal") and symbol:
    st.info("Fetching stock data...")

    # Get 30 days of historical data
    data = yf.download(symbol, period="30d", interval="1d")
    
    if data.empty:
        st.error("No data found. Please check the symbol and try again.")
    else:
        # Signal logic (very basic)
        data['SMA_5'] = data['Close'].rolling(window=5).mean()
        data['SMA_20'] = data['Close'].rolling(window=20).mean()

        latest = data.iloc[-1]

        signal = ""
        if latest['SMA_5'] > latest['SMA_20']:
            signal = "📈 BUY Signal"
            st.success(f"{signal} - Short term uptrend detected.")
        elif latest['SMA_5'] < latest['SMA_20']:
            signal = "📉 SELL Signal"
            st.error(f"{signal} - Short term downtrend detected.")
        else:
            signal = "⚖️ HOLD"
            st.warning(f"{signal} - No clear trend yet.")
        
        # Show table
        st.subheader("Latest Data")
        st.dataframe(data.tail(5))
