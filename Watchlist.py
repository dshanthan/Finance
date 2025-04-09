import streamlit as st  # Ensure this line is present
import yfinance as yf
import pandas as pd

st.title("My Stock Watchlist")
tickers = ["AAPL", "TSLA", "BRK-B"]  # Your watchlist

for ticker in tickers:
    st.write(f"Fetching data for {ticker}...")
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1d")  # Get 1 day of data
        st.write(f"Raw data for {ticker}:")
        st.write(history)  # Show the full DataFrame to debug Econôm

        if not history.empty:
            price = history["Close"].iloc[-1]
            st.write(f"{ticker}: ${price:.2f}")
        else:
            st.write(f"{ticker}: No data available")
    except Exception as e:
        st.write(f"{ticker}: Error - {str(e)}")
