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
        fng_value = fng_data.value  # Numeric value (0-100)
        sentiment = fng_data.description.capitalize()
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
        # Map 0-100 to 0-180 degrees (half-circle gauge)
        needle_angle = (fng_value / 100) * 180 - 90  # -90 to 90 degrees
    except Exception:
        sentiment = "N/A"
        sentiment_color = "black"
        needle_angle = 0  # Default to center if error

    # Horizontal display with percentage changes
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

    # Dial gauge for Fear & Greed
    gauge_html = f"""
    <div style="width: 300px; height: 150px; position: relative; margin: 20px auto;">
        <!-- Semicircle background with color zones -->
        <div style="width: 100%; height: 100%; background: linear-gradient(to right, 
            #e74c3c 0%, #e74c3c 25%, 
            #c0392b 25%, #c0392b 50%, 
            #7f8c8d 50%, #7f8c8d 75%, 
            #27ae60 75%, #27ae60 87.5%, 
            #2ecc71 87.5%, #2ecc71 100%); 
            clip-path: ellipse(50% 100% at 50% 100%); border: 2px solid #333;"></div>
        <!-- Needle -->
        <div style="width: 2px; height: 70%; background: black; position: absolute; bottom: 0; left: 50%; 
            transform-origin: bottom center; transform: rotate({needle_angle}deg);"></div>
    </div>
    <div style="display: flex; justify-content: space-between; width: 300px; margin: 0 auto; font-size: 12px;">
        <span>Extreme Fear</span><span>Fear</span><span>Neutral</span><span>Greed</span><span>Extreme Greed</span>
    </div>
    """
    st.markdown(gauge_html, unsafe_allow_html=True)
    st.markdown("---")

if __name__ == "__main__":
    display_market_overview()
