import streamlit as st
import yfinance as yf

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

    # Simulate market sentiment based on SPY change
    try:
        spy = yf.Ticker("SPY")
        spy_history = spy.history(period="2d")
        if len(spy_history) >= 2:
            current_price = spy_history["Close"].iloc[-1]
            prev_close = spy_history["Close"].iloc[-2]
            spy_change = ((current_price - prev_close) / prev_close) * 100
            if spy_change > 2:
                sentiment = "Extreme Greed"
                sentiment_color = "#2ecc71"
            elif spy_change > 0:
                sentiment = "Greed"
                sentiment_color = "#27ae60"
            elif spy_change < -2:
                sentiment = "Extreme Fear"
                sentiment_color = "#e74c3c"
            else:
                sentiment = "Fear"
                sentiment_color = "#c0392b"
        else:
            sentiment = "N/A"
            sentiment_color = "black"
    except Exception:
        sentiment = "N/A"
        sentiment_color = "black"

    # Display horizontally with styled markdown
    market_line = (
        f"<b>S&P 500 (SPY):</b> ${market_data['S&P 500 (SPY)']:.2f}  |  "
        f"<b>Dow Jones (DIA):</b> ${market_data['Dow Jones (DIA)']:.2f}  |  "
        f"<b>Nasdaq (QQQ):</b> ${market_data['Nasdaq (QQQ)']:.2f}  |  "
        f"<b>Oil (USO):</b> ${market_data['Oil (USO)']:.2f}  |  "
        f"<b>Gold (GLD):</b> ${market_data['Gold (GLD)']:.2f}  |  "
        f"<b>Sentiment:</b> <span style='color:{sentiment_color}'>{sentiment}</span>"
    )
    st.markdown(f"Market Overview (April 9, 2025): {market_line}", unsafe_allow_html=True)
    st.markdown("---")

if __name__ == "__main__":
    display_market_overview()
