import streamlit as st
import yfinance as yf
import fear_and_greed

def display_market_overview():
    # Define tickers for actual indexes and commodities
    market_tickers = {
        "S&P 500": "^GSPC",
        "Dow Jones": "^DJI",
        "Nasdaq": "^IXIC",
        "Crude Oil": "CL=F",
        "Gold": "GC=F"
    }

    market_data = {}
    for name, ticker in market_tickers.items():
        try:
            stock = yf.Ticker(ticker)
            intraday = stock.history(period="1d", interval="1m")
            history = stock.history(period="2d")
            if not intraday.empty and len(history) >= 2:
                current_price = intraday["Close"].iloc[-1]
                prev_close = history["Close"].iloc[-2]
                pct_change = ((current_price - prev_close) / prev_close) * 100
                market_data[name] = {"price": current_price, "change": pct_change}
            else:
                market_data[name] = {"price": "N/A", "change": "N/A"}
        except Exception:
            market_data[name] = {"price": "N/A", "change": "N/A"}

    # Fetch CNN Fear & Greed Index
    try:
        fng_data = fear_and_greed.get()
        sentiment = fng_data.description.capitalize()  # E.g., "Extreme Fear"
        if fng_data.value >= 75:
            sentiment_color = "#2ecc71"  # Extreme Greed
        elif fng_data.value >= 50:
            sentiment_color = "#27ae60"  # Greed
        elif fng_data.value <= 25:
            sentiment_color = "#e74c3c"  # Extreme Fear
        elif fng_data.value < 50:
            sentiment_color = "#c0392b"  # Fear
        else:
            sentiment_color = "#7f8c8d"  # Neutral
    except Exception:
        sentiment = "N/A"
        sentiment_color = "black"

    # Uniform font size with proper brackets
    market_line = (
        f"<span style='font-size: 16px;'>"
        f"S&P 500: ${market_data['S&P 500']['price']:.2f} "
        f"({'+' if market_data['S&P 500']['change'] >= 0 else ''}{market_data['S&P 500']['change']:.2f}%) | "
        f"Dow Jones: ${market_data['Dow Jones']['price']:.2f} "
        f"({'+' if market_data['Dow Jones']['change'] >= 0 else ''}{market_data['Dow Jones']['change']:.2f}%) | "
        f"Nasdaq: ${market_data['Nasdaq']['price']:.2f} "
        f"({'+' if market_data['Nasdaq']['change'] >= 0 else ''}{market_data['Nasdaq']['change']:.2f}%) | "
        f"Crude Oil: ${market_data['Crude Oil']['price']:.2f} "
        f"({'+' if market_data['Crude Oil']['change'] >= 0 else ''}{market_data['Crude Oil']['change']:.2f}%) | "
        f"Gold: ${market_data['Gold']['price']:.2f} "
        f"({'+' if market_data['Gold']['change'] >= 0 else ''}{market_data['Gold']['change']:.2f}%) | "
        f"CNN Fear & Greed: <span style='color:{sentiment_color}'>{sentiment}</span>"
        f"</span>"
    )
    st.markdown(market_line, unsafe_allow_html=True)
    st.markdown("---")

if __name__ == "__main__":
    display_market_overview()
