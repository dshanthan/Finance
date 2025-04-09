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
            data["Most Recent Price"].append(recent_price)  # Raw numbers for styling
            data["2025 All-Time High"].append(ath_this_year)
            data["Down from ATH (%)"].append(pct_down)
        else:
            data["Ticker"].append(ticker)
            data["Most Recent Price"].append(None)
            data["2025 All-Time High"].append(None)
            data["Down from ATH (%)"].append(None)
    except Exception as e:
        data["Ticker"].append(ticker)
        data["Most Recent Price"].append(None)
        data["2025 All-Time High"].append(None)
        data["Down from ATH (%)"].append(None)

# Create DataFrame
df = pd.DataFrame(data)

# Define styling function
def style_table(df):
    # Convert numbers to formatted strings for display, handle None values
    styled_df = df.style.format({
        "Most Recent Price": lambda x: f"${x:.2f}" if pd.notnull(x) else "N/A",
        "2025 All-Time High": lambda x: f"${x:.2f}" if pd.notnull(x) else "N/A",
        "Down from ATH (%)": lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A"
    })
    
    # Apply styles
    styled_df = styled_df.set_properties(**{
        'text-align': 'center',           # Center all text
        'border': '1px solid #ddd',       # Light gray borders
        'background-color': '#f9f9f9',    # Subtle gray background
        'padding': '5px'                  # Spacing inside cells
    })
    
    # Style specific columns
    styled_df = styled_df.set_properties(
        subset=["Most Recent Price", "2025 All-Time High"],
        **{'color': '#2ecc71'}  # Green for prices
    )
    styled_df = styled_df.set_properties(
        subset=["Down from ATH (%)"],
        **{'color': '#e74c3c'}  # Red for percentage drop
    )
    
    # Bold headers
    styled_df = styled_df.set_table_styles([
        {'selector': 'th',
         'props': [('font-weight', 'bold'),
                   ('text-align', 'center'),
                   ('background-color', '#34495e'),  # Dark blue header
                   ('color', 'white'),
                   ('border', '1px solid #ddd')]}
    ])
    
    return styled_df

# Display styled table
st.dataframe(style_table(df), use_container_width=True)
