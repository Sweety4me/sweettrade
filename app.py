import streamlit as st
from signals import generate_trade_signal

st.set_page_config(page_title="SweetTrade", layout="wide")
st.title("💹 SweetTrade: Bava's Advanced Trading Tool")

ticker = st.text_input("Enter Stock Symbol (e.g., TATAMOTORS.NS)")

if st.button("Get Signal"):
    signal, chart = generate_trade_signal(ticker)
    st.success(f"Signal: {signal}")
    st.pyplot(chart)
