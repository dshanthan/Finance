import streamlit as st
import yfinance as yf

def display_market_overview():
    st.subheader("Market Overview (April 9, 2025)")

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

    # Display in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**S&P 500 (SPY):** ${market_data['S&P 500 (SPY)']:.2f}" if market_data['S&P 500 (SPY)'] != "N/A" else "**S&P 500 (SPY):** N/A")
        st.markdown(f"
