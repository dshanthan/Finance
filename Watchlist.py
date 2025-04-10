import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from MarketOverview import display_market_overview  # Import the new file

st.title("My Stock Watchlist")

# Display the market overview
display_market_overview()

# Your watchlist tickers
tickers = ["AAPL", "TSLA", "BRK-B", "^GSPC"]
start_date = "2025-01-01"
today = datetime.now().strftime("%Y-%m-%d")

# Fetch Dataroma superinvestor count
def get_superinvestor_count(ticker):
    try:
        url = f"https://www.dataroma.com/m/stock.php?s={ticker.replace('^', '')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        held_by = soup.find("div", {"id": "content"}).find("p")
        if held_by and "Held by" in held_by.text:
            count = int(held_by.text.split("Held by ")[1].split(" superinvestor")[0])
            return count
        return 0
    except Exception:
        return "N/A"

# Prepare watchlist data
data = {
    "Ticker": [],
    "Most Recent Price": [],
    "2025 All-Time High": [],
    "Change from ATH": [],
    "Superinvestors Holding": []
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
            superinvestor_count = get_superinvestor_count(ticker)
            
            data["Ticker"].append(ticker)
            data["Most Recent Price"].append(recent_price)
            data["2025 All-Time High"].append(ath_this_year)
            data["Change from ATH"].append(pct_change)
            data["Superinvestors Holding"].append(superinvestor_count)
        else:
            data["Ticker"].append(ticker)
            data["Most Recent Price"].append(None)
            data["2025 All-Time High"].append(None)
            data["Change from ATH"].append(None)
            data["Superinvestors Holding"].append("N/A")
    except Exception:
        data["Ticker"].append(ticker)
        data["Most Recent Price"].append(None)
        data["2025 All-Time High"].append(None)
        data["Change from ATH"].append(None)
        data["Superinvestors Holding"].append("N/A")

# Create DataFrame
df = pd.DataFrame(data)

# Styling function
def style_table(df):
    styled_df = df.style.format({
        "Most Recent Price": lambda x: f"${x:.2f}" if pd.notnull(x) else "N/A",
        "2025 All-Time High": lambda x: f"${x:.2f}" if pd.notnull(x) else "N/A",
        "Change from ATH": lambda x: f"{x:+.2f}%" if pd.notnull(x) else "N/A",
        "Superinvestors Holding": lambda x: str(x) if x != "N/A" else "N/A"
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

# Display styled table and attribution
st.dataframe(style_table(df), use_container_width=True)
st.write("Superinvestor data sourced from [Dataroma.com](https://www.dataroma.com)")
