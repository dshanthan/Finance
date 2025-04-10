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

    # Use real-time data from system input for SPY, USO, GLD
    realtime_data = {
        "SPY": 548.62,  # Current price from system data
        "USO": 67.58,
        "GLD": 285.38
    }

    market_data = {}
    for name, ticker in market_tickers.items():
        if ticker in realtime_data:
            price = realtime_data[ticker]
            market_data[name] = price
        else:
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
    spy_change = ((548.62 - 496.48) / 496.48) * 100  # From prevDayClose to currentPrice
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

    # Display in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**S&P 500 (SPY):** ${market_data['S&P 500 (SPY)']:.2f}")
        st.markdown(f"**Dow Jones (DIA):** ${market_data['Dow Jones (DIA)']:.2f}")
    with col2:
        st.markdown(f"**Nasdaq (QQQ):** ${market_data['Nasdaq (QQQ)']:.2f}")
        st.markdown(f"**Oil (USO):** ${market_data['Oil (USO)']:.2f}")
    with col3:
        st.markdown(f"**Gold (GLD):** ${market_data['Gold (GLD)']:.2f}")
        st.markdown(f"**Sentiment:** <span style='color:{sentiment_color}'>{sentiment}</span>", unsafe_allow_html=True)

    st.markdown("---")

# Call this function if running standalone
if __name__ == "__main__":
    display_market_overview()
