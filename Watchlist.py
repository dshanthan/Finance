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

        stock = yf.Ticker(ticker)
        
        # Fetch YTD data for all-time high this year
        history = stock.history(start=start_date, end=today)
        
        # Fetch most recent price (intraday, last 1 minute)
        intraday = stock.history(period="1d", interval="1m")  # 1-minute intervals for today
        
        if not history.empty and not intraday.empty:
            # Most recent price (last available price today)
            recent_price = intraday["Close"].iloc[-1]
            
            # All-time high this year (max close in 2025)
            ath_this_year = history["Close"].max()
            
            # Percentage down from ATH
            pct_down = ((ath_this_year - recent_price) / ath_this_year) * 100
            
            # Display results
            st.write(f"**{ticker}**")
            st.write(f"Most Recent Price: ${recent_price:.2f}")
            st.write(f"2025 All-Time High: ${ath_this_year:.2f}")
            st.write(f"Down from ATH: {pct_down:.2f}%")
            st.write("---")
        else:
            st.write(f"{ticker}: No data available")
    except Exception as e:
        st.write(f"{ticker}: Error - {str(e)}")
