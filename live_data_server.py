from mcp.server.fastmcp import FastMCP
import httpx
import yfinance as yf

mcp = FastMCP("LiveInfo")

@mcp.tool()
async def get_weather(city: str):
    """Fetches current weather for a city using Open-Meteo."""
    # Step 1: Geocoding (City name to Lat/Long)
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    async with httpx.AsyncClient() as client:
        geo_res = await client.get(geo_url)
        data = geo_res.json()
        
        if not data.get("results"):
            return f"Could not find coordinates for {city}."
        
        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]

        # Step 2: Get Weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_res = await client.get(weather_url)
        w_data = weather_res.json()["current_weather"]
        
        return f"Current weather in {city}: {w_data['temperature']}°C, Windspeed: {w_data['windspeed']} km/h"

@mcp.tool()
def get_stock_price(ticker: str):
    """Fetches real-time stock price and info (e.g., 'MSFT','AAPL', 'TSLA')."""
    stock = yf.Ticker(ticker)
    info = stock.fast_info
    return {
        "ticker": ticker,
        "price": round(info['last_price'], 2),
        "currency": info['currency'],
        "market_cap": f"{info['market_cap']:,.0f}"
    }

if __name__ == "__main__":
    mcp.run()