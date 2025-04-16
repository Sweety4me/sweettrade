# Get the latest row from the stock data
latest = stock_data.iloc[-1]  # This line should come BEFORE using `latest`

# Extract SMA values as floats
sma_5_latest = latest['SMA_5'].item() if hasattr(latest['SMA_5'], 'item') else latest['SMA_5']
sma_20_latest = latest['SMA_20'].item() if hasattr(latest['SMA_20'], 'item') else latest['SMA_20']

# Debug info
st.write(f"SMA_5 latest value: {sma_5_latest}")
st.write(f"SMA_20 latest value: {sma_20_latest}")

# Signal logic
if isinstance(sma_5_latest, (int, float)) and isinstance(sma_20_latest, (int, float)):
    if sma_5_latest > sma_20_latest:
        signal = "📈 BUY Signal"
        st.success(f"{signal} - Short-term uptrend detected.")
    elif sma_5_latest < sma_20_latest:
        signal = "📉 SELL Signal"
        st.error(f"{signal} - Short-term downtrend detected.")
    else:
        signal = "⚖️ HOLD"
        st.warning(f"{signal} - No clear trend yet.")
else:
    st.error("⚠️ Unable to compare SMA values. Check for missing or incorrect data.")
