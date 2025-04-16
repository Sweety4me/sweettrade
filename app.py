import streamlit as st
import yfinance as yf
import pandas as pd

st.title("SweetTrade: Bava's Advanced Trading Tool")

symbol = st.text_input("Enter Stock Symbol (e.g., TATAMOTORS.NS)", "BPCL.NS")

if symbol:
    with st.spinner("📊 Fetching stock data..."):
        # Download stock data
        stock_data = yf.download(symbol, period="1mo", interval="1d")

        # Check if data exists
        if stock_data.empty:
            st.error("⚠️ No data found for the given symbol.")
        else:
            # Calculate moving averages
            stock_data['SMA_5'] = stock_data['Close'].rolling(window=5).mean()
            stock_data['SMA_20'] = stock_data['Close'].rolling(window=20).mean()

            # Drop rows with NaN
            stock_data.dropna(inplace=True)

            # Ensure we have valid data
            if len(stock_data) < 1:
                st.error("⚠️ Not enough data to calculate SMAs.")
            else:
                # Get the latest row safely
                latest_row = stock_data.iloc[-1]

                # Extract SMA values
                sma_5_latest = latest_row['SMA_5']
                sma_20_latest = latest_row['SMA_20']

                st.write(f"📅 Latest Stock Data")
                st.write(f"📈 Price & Moving Averages")
                st.write(f"SMA_5: {sma_5_latest}")
                st.write(f"SMA_20: {sma_20_latest}")

                # Compare SMAs
                if pd.notna(sma_5_latest) and pd.notna(sma_20_latest):
                    if sma_5_latest > sma_20_latest:
                        st.success("📈 BUY Signal - Short-term uptrend detected.")
                    elif sma_5_latest < sma_20_latest:
                        st.error("📉 SELL Signal - Short-term downtrend detected.")
                    else:
                        st.warning("⚖️ HOLD - No clear trend.")
                else:
                    st.error("⚠️ SMA values are not valid for comparison.")
