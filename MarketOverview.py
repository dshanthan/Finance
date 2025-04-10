import streamlit as st
import yfinance as yf
import fear_and_greed

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
            history = stock.history(period="2d")  # For prev close
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
        fng_value = fng_data.value  # Numeric value (0-100) for gauge
        sentiment = fng_data.description.capitalize()  # E.g., "Fear"
        if fng_value >= 75:
            sentiment_color = "#2ecc71"  # Extreme Greed
            gauge_position = 0.875  # 87.5% (center of Extreme Greed)
        elif fng_value >= 50:
            sentiment_color = "#27ae60"  # Greed
            gauge_position = 0.625  # 62.5% (center of Greed)
        elif fng_value <= 25:
            sentiment_color = "#e74c3c"  # Extreme Fear
            gauge_position = 0.125  # 12.5% (center of Extreme Fear)
        elif fng_value < 50:
            sentiment_color = "#c0392b"  # Fear
            gauge_position = 0.375  # 37.5% (center of Fear)
        else:
            sentiment_color = "#7f8c8d"  # Neutral
            gauge_position = 0.5  # 50% (center of Neutral)
    except Exception:
        sentiment = "N/A"
        sentiment_color = "black"
        gauge_position = 0.5  # Default to middle if error

    # Clean horizontal display with percentage changes
    market_line = (
        f"S&P 500 (SPY): ${market_data['S&P 500 (SPY)']['price']:.2f} "
        f"({'+' if market_data['S&P 500 (SPY)']['change'] >= 0 else ''}{market_data['S&P 500 (SPY)']['change']:.2f}%) | "
        f"Dow Jones (DIA): ${market_data['Dow Jones (DIA)']['price']:.2f} "
        f"({'+' if market_data['Dow Jones (DIA)']['change'] >= 0 else ''}{market_data['Dow Jones (DIA)']['change']:.2f}%) | "
        f"Nasdaq (QQQ): ${market_data['Nasdaq (QQQ)']['price']:.2f} "
        f"({'+' if market_data['Nasdaq (QQQ)']['change'] >= 0 else ''}{market_data['Nasdaq (QQQ)']['change']:.2f}%) | "
        f"Oil (USO): ${market_data['Oil (USO)']['price']:.2f} "
        f"({'+' if market_data['Oil (USO)']['change'] >= 0 else ''}{market_data['Oil (USO)']['change']:.2f}%) | "
        f"Gold (GLD): ${market_data['Gold (GLD)']['price']:.2f} "
        f"({'+' if market_data['Gold (GLD)']['change'] >= 0 else ''}{market_data['Gold (GLD)']['change']:.2f}%) | "
        f"CNN Fear & Greed: <span style='color:{sentiment_color}'>{sentiment}</span>"
    )
    st.markdown(market_line, unsafe_allow_html=True)

    # Meter-like gauge for Fear & Greed
    gauge_html = f"""
    <div style="width: 100%; height: 20px; background: linear-gradient(to right, 
        #e74c3c 0%, #e74c3c 25%, 
        #c0392b 25%, #c0392b 50%, 
        #7f8c8d 50%, #7f8c8d 75%, 
        #27ae60 75%, #27ae60 87.5%, 
        #2ecc71 87.5%, #2ecc71 100%); position: relative;">
        <div style="position: absolute; left: {gauge_position * 100}%; top: 0; width: 2px; height: 100%; background: black;"></div>
    </div>
    <div style="display: flex; justify-content: space-between; font-size: 12px;">
        <span>Extreme Fear</span><span>Fear</span><span>Neutral</span><span>Greed</span><span>Extreme Greed</span>
    </div>
    """
    st.markdown(gauge_html, unsafe_allow_html=True)
    st.markdown("---")

if __name__ == "__main__":
    display_market_overview()
