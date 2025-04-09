import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.title("My Stock Watchlist")

# Ticker list with S&P 500
tickers = ["AAPL", "TSLA", "BRK-B", "^GSPC"]

# Set the start of 2025 for YTD data
start_date = "2025-01-01"
today = datetime.now().strftime("%Y-%m-%d")

# Prepare data for the table
data = {
    "Ticker": [],
    "Most Recent Price": [],
    "2025 All-Time High": [],
    "Down from ATH (%)": []
}

for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        
        # Fetch YTD data for all-time high this year
        history = stock.history(start=start_date, end=today)
        
        # Fetch most recent price (intraday, last 1 minute)
        intraday = stock.history(period="1d", interval="1m")
        
        if not history.empty and not intraday.empty:
            # Most recent price
            recent_price = intraday["Close"].iloc[-1]
            
            # All-time high this year
            ath_this_year = history["Close"].max()
            
            # Percentage down from ATH
            pct_down = ((ath_this_year - recent_price) / ath_this_year) * 100
            
            # Add to data dictionary
            data["Ticker"].append(ticker)
            data["Most Recent Price"].append(f"${recent_price:.2f}")
            data["2025 All-Time High"].append(f"${ath_this_year:.2f}")
            data["Down from ATH (%)"].append(f"{pct_down:.2f}")
        else:
            # Handle no data case
            data["Ticker"].append(ticker)
            data["Most Recent Price"].append("N/A")
            data["2025 All-Time High"].append("N/A")
            data["Down from ATH (%)"].append("N/A")
    except Exception as e:
        # Handle errors
        data["Ticker"].append(ticker)
        data["Most Recent Price"].append("Error")
        data["2025 All-Time High"].append("Error")
        data["Down from ATH (%)"].append(f"{str(e)}")

# Create DataFrame and display as table
df = pd.DataFrame(data)
st.table(df)
