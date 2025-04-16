import streamlit as st
import yfinance as yf
import pandas as pd
import pytz  # ✅ Added for timezone conversion

st.title("SweetTrade: Bava's Advanced Trading Tool")

symbol = st.text_input("Enter Stock Symbol (e.g., TATAMOTORS.NS)", "BPCL.NS")

if symbol:
    with st.spinner("📊 Fetching stock data..."):
        stock_data = yf.download(symbol, period="1mo", interval="1d")

        if stock_data.empty:
            st.error("⚠️ No data found for the given symbol.")
        else:
            # ✅ Convert to IST timezone
            stock_data.index = pd.to_datetime(stock_data.index)
            stock_data.index = stock_data.index.tz_localize('UTC')
            stock_data.index = stock_data.index.tz_convert('Asia/Kolkata')

            stock_data['SMA_5'] = stock_data['Close'].rolling(window=5).mean()
            stock_data['SMA_20'] = stock_data['Close'].rolling(window=20).mean()
            stock_data.dropna(inplace=True)

            if len(stock_data) < 1:
                st.error("⚠️ Not enough data to calculate SMAs.")
            else:
                latest_row = stock_data.iloc[-1]

                try:
                    sma_5_latest = latest_row['SMA_5'].item() if hasattr(latest_row['SMA_5'], 'item') else float(latest_row['SMA_5'])
                    sma_20_latest = latest_row['SMA_20'].item() if hasattr(latest_row['SMA_20'], 'item') else float(latest_row['SMA_20'])

                    st.write(f"📅 Latest Stock Data (IST)")
                    st.write(stock_data.tail(1))  # Show last row with IST time
                    st.write(f"📈 Price & Moving Averages")
                    st.write(f"SMA_5: {sma_5_latest}")
                    st.write(f"SMA_20: {sma_20_latest}")

                    if sma_5_latest > sma_20_latest:
                        st.success("📈 BUY Signal - Short-term uptrend detected.")
                    elif sma_5_latest < sma_20_latest:
                        st.error("📉 SELL Signal - Short-term downtrend detected.")
                    else:
                        st.warning("⚖️ HOLD - No clear trend.")
                except Exception as e:
                    st.error(f"⚠️ Unable to compare SMA values. Error: {e}")
