import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.title("My Stock Watchlist")

# Updated ticker list with S&P 500 (^GSPC)
tickers = ["AAPL", "TSLA", "BRK-B", "^GSPC"]

# Set the start of 2025 for YTD data
start_date = "2025-01-01"
today = datetime.now().strftime("%Y-%m-%d")  # Current date

for ticker in tickers:
    st.write(f"Fetching data for {ticker}...")
    try:
        # Fetch YTD data
        stock = yf.Ticker(ticker)
        history = stock.history(start=start_date, end=today)
        
        if not history.empty:
            # Current price (latest close)
            current_price = history["Close"].iloc[-1]
            
            # All-time high this year (max close in 2025)
            ath_this_year = history["Close"].max()
            
            # Percentage down from ATH
            pct_down = ((ath_this_year - current_price) / ath_this_year) * 100
            
            # Display results
            st.write(f"**{ticker}**")
            st.write(f"Current Price: ${current_price:.2f}")
            st.write(f"2025 All-Time High: ${ath_this_year:.2f}")
            st.write(f"Down from ATH: {pct_down:.2f}%")
            st.write("---")  # Separator
        else:
            st.write(f"{ticker}: No data available")
    except Exception as e:
        st.write(f"{ticker}: Error - {str(e)}")
