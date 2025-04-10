import streamlit as st
import yfinance as yf
import fear_and_greed  # New import

def display_market_overview():
    # Define tickers for major indexes, oil, and gold
    market_tickers = {
        "S&P 500 (SPY)": "SPY",
        "Dow Jones (DIA)": "DIA",
        "Nasdaq (QQQ)": "QQQ",
        "Oil (USO)": "USO",
        "Gold (GLD)": "GLD"
    }

    market_data = {}
    for name, ticker in market_tickers.items():
        try:
            stock = yf.Ticker(ticker)
            intraday = stock.history(period="1d", interval="1m")
            if not intraday.empty:
                price = intraday["Close"].iloc[-1]
                market_data[name] = price
            else:
                market_data[name] = "N/A"
        except Exception:
            market_data[name] = "N/A"

    # Fetch CNN Fear & Greed Index using fear-and-greed package
    try:
        fng_data = fear_and_greed.get()
        fng_value = fng_data.value  # Numeric value (0-100)
        sentiment = fng_data.description.capitalize()  # E.g., "Fear", "Greed"
        if fng_value >= 75:
            sentiment_color = "#2ecc71"  # Extreme Greed
        elif fng_value >= 50:
            sentiment_color = "#27ae60"  # Greed
        elif fng_value <= 25:
            sentiment_color = "#e74c3c"  # Extreme Fear
        elif fng_value < 50:
            sentiment_color = "#c0392b"  # Fear
        else:
            sentiment_color = "#7f8c8d"  # Neutral
    except Exception:
        fng_value = "N/A"
        sentiment = "N/A"
        sentiment_color = "black"

    # Clean horizontal display
    market_line = (
        f"S&P 500 (SPY): ${market_data['S&P 500 (SPY)']:.2f} | "
        f"Dow Jones (DIA): ${market_data['Dow Jones (DIA)']:.2f} | "
        f"Nasdaq (QQQ): ${market_data['Nasdaq (QQQ)']:.2f} | "
        f"Oil (USO): ${market_data['Oil (USO)']:.2f} | "
        f"Gold (GLD): ${market_data['Gold (GLD)']:.2f} | "
        f"CNN Fear & Greed: <span style='color:{sentiment_color}'>{fng_value} ({sentiment})</span>"
    )
    st.markdown(market_line, unsafe_allow_html=True)
    st.markdown("---")

if __name__ == "__main__":
    display_market_overview()
