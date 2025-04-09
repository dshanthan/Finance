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
    "Change from ATH": []  # Renamed column
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
            
            # Percentage change from ATH (positive if up, negative if down)
            pct_change = ((recent_price - ath_this_year) / ath_this_year) * 100
            
            # Add to data dictionary
            data["Ticker"].append(ticker)
            data["Most Recent Price"].append(recent_price)
            data["2025 All-Time High"].append(ath_this_year)
            data["Change from ATH"].append(pct_change)
        else:
            data["Ticker"].append(ticker)
            data["Most Recent Price"].append(None)
            data["2025 All-Time High"].append(None)
            data["Change from ATH"].append(None)
    except Exception as e:
        data["Ticker"].append(ticker)
        data["Most Recent Price"].append(None)
        data["2025 All-Time High"].append(None)
        data["Change from ATH"].append(None)

# Create DataFrame
df = pd.DataFrame(data)

# Define styling function with conditional coloring
def style_table(df):
    # Format numbers, handle None values
    styled_df = df.style.format({
        "Most Recent Price": lambda x: f"${x:.2f}" if pd.notnull(x) else "N/A",
        "2025 All-Time High": lambda x: f"${x:.2f}" if pd.notnull(x) else "N/A",
        "Change from ATH": lambda x: f"{x:+.2f}%" if pd.notnull(x) else "N/A"  # + or - sign
    })
    
    # General table properties
    styled_df = styled_df.set_properties(**{
        'text-align': 'center',
        'border': '1px solid #ddd',
        'background-color': '#f9f9f9',
        'padding': '5px'
    })
    
    # Style specific columns
    styled_df = styled_df.set_properties(
        subset=["Most Recent Price", "2025 All-Time High"],
        **{'color': '#2ecc71'}  # Green for prices
    )
    
    # Conditional coloring for Change from ATH
    def color_change(val):
        if pd.notnull(val):
            return 'color: #2ecc71' if val > 0 else 'color: #e74c3c'  # Green if up, red if down
        return 'color: black'
    
    styled_df = styled_df.applymap(color_change, subset=["Change from ATH"])
    
    # Bold headers
    styled_df = styled_df.set_table_styles([
        {'selector': 'th',
         'props': [('font-weight', 'bold'),
                   ('text-align', 'center'),
                   ('background-color', '#34495e'),
                   ('color', 'white'),
                   ('border', '1px solid #ddd')]}
    ])
    
    return styled_df

# Display styled table
st.dataframe(style_table(df), use_container_width=True)
