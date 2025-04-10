import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from MarketOverview import display_market_overview

# Display market overview at the absolute top
display_market_overview()

# Main title
st.title("My Stock Watchlist")

# Watchlist tickers
tickers = ["AAPL", "TSLA", "BRK-B", "^GSPC"]
start_date = "2025-01-01"
today = datetime.now().strftime("%Y-%m-%d")

# Prepare watchlist data
data = {
    "Ticker": [],
    "Most Recent Price": [],
    "2025 All-Time High": [],
    "Change from ATH": []
}

for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(start=start_date, end=today)
        intraday = stock.history(period="1d", interval="1m")
        
        if not history.empty and not intraday.empty:
            recent_price = intraday["Close"].iloc[-1]
            ath_this_year = history["Close"].max()
            pct_change = ((recent_price - ath_this_year) / ath_this_year) * 100
            
            data["Ticker"].append(ticker)
            data["Most Recent Price"].append(recent_price)
            data["2025 All-Time High"].append(ath_this_year)
            data["Change from ATH"].append(pct_change)
        else:
            data["Ticker"].append(ticker)
            data["Most Recent Price"].append(None)
            data["2025 All-Time High"].append(None)
            data["Change from ATH"].append(None)
    except Exception:
        data["Ticker"].append(ticker)
        data["Most Recent Price"].append(None)
        data["2025 All-Time High"].append(None)
        data["Change from ATH"].append(None)

# Create DataFrame
df = pd.DataFrame(data)

# Styling function
def style_table(df):
    styled_df = df.style.format({
        "Most Recent Price": lambda x: f"${x:.2f}" if pd.notnull(x) else "N/A",
        "2025 All-Time High": lambda x: f"${x:.2f}" if pd.notnull(x) else "N/A",
        "Change from ATH": lambda x: f"{x:+.2f}%" if pd.notnull(x) else "N/A"
    })
    styled_df = styled_df.set_properties(**{
        'text-align': 'center',
        'border': '1px solid #ddd',
        'background-color': '#f9f9f9',
        'padding': '5px'
    })
    styled_df = styled_df.set_properties(
        subset=["Most Recent Price", "2025 All-Time High"],
        **{'color': '#2ecc71'}
    )
    def color_change(val):
        if pd.notnull(val):
            return 'color: #2ecc71' if val > 0 else 'color: #e74c3c'
        return 'color: black'
    styled_df = styled_df.applymap(color_change, subset=["Change from ATH"])
    styled_df = styled_df.set_table_styles([
        {'selector': 'th',
         'props': [('font-weight', 'bold'),
                   ('text-align', 'center'),
                   ('background-color', '#34495e'),
                   ('color', 'white'),
                   ('border', '1px solid #ddd')]}
    ])
    return styled_df

# Display watchlist title with larger font and table
st.markdown("<h2 style='font-size: 36px;'>My Stock Watchlist</h2>", unsafe_allow_html=True)
st.dataframe(style_table(df), use_container_width=True)
