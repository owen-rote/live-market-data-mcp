import json
import logging
import sys
import yfinance as yf
from mcp.server.fastmcp import FastMCP

# Configure logging to write to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("live-market-data-mcp")

# Initialize FastMCP server
mcp = FastMCP("live-market-data")


@mcp.tool()
async def get_stock_price(symbol: str) -> str:
    """Get the current stock price and basic info for a given ticker symbol.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL, GOOGL, MSFT)
    """
    ticker = yf.Ticker(symbol)
    info = ticker.info

    data = {
        "symbol": symbol.upper(),
        "name": info.get("shortName", "N/A"),
        "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
        "previous_close": info.get("previousClose"),
        "open": info.get("open") or info.get("regularMarketOpen"),
        "day_high": info.get("dayHigh") or info.get("regularMarketDayHigh"),
        "day_low": info.get("dayLow") or info.get("regularMarketDayLow"),
        "volume": info.get("volume") or info.get("regularMarketVolume"),
        "market_cap": info.get("marketCap"),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        "currency": info.get("currency", "USD"),
    }

    return json.dumps(data, indent=2)


@mcp.tool()
async def get_stock_history(
    symbol: str,
    period: str = "1mo",
    interval: str = "1d",
) -> str:
    """Get historical price data for a stock.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL, GOOGL)
        period: Time period (e.g. 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        interval: Data interval (e.g. 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
    """
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, interval=interval)

    if hist.empty:
        return json.dumps({"error": f"No historical data found for {symbol}"})

    records = []
    for date, row in hist.iterrows():
        records.append(
            {
                "date": str(date),
                "open": round(row["Open"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "close": round(row["Close"], 2),
                "volume": int(row["Volume"]),
            }
        )

    data = {
        "symbol": symbol.upper(),
        "period": period,
        "interval": interval,
        "data_points": len(records),
        "history": records,
    }

    return json.dumps(data, indent=2)


@mcp.tool()
async def get_company_info(symbol: str) -> str:
    """Get detailed company information for a stock.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL, GOOGL)
    """
    ticker = yf.Ticker(symbol)
    info = ticker.info

    data = {
        "symbol": symbol.upper(),
        "name": info.get("longName") or info.get("shortName", "N/A"),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "country": info.get("country", "N/A"),
        "website": info.get("website", "N/A"),
        "description": info.get("longBusinessSummary", "N/A"),
        "employees": info.get("fullTimeEmployees"),
        "ceo": info.get("companyOfficers", [{}])[0].get("name") if info.get("companyOfficers") else "N/A",
    }

    return json.dumps(data, indent=2)


@mcp.tool()
async def get_financial_metrics(symbol: str) -> str:
    """Get key financial metrics and ratios for a stock.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL, GOOGL)
    """
    ticker = yf.Ticker(symbol)
    info = ticker.info

    data = {
        "symbol": symbol.upper(),
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "peg_ratio": info.get("pegRatio"),
        "price_to_book": info.get("priceToBook"),
        "eps": info.get("trailingEps"),
        "forward_eps": info.get("forwardEps"),
        "dividend_yield": info.get("dividendYield"),
        "dividend_rate": info.get("dividendRate"),
        "beta": info.get("beta"),
        "profit_margin": info.get("profitMargins"),
        "revenue": info.get("totalRevenue"),
        "gross_profit": info.get("grossProfits"),
        "ebitda": info.get("ebitda"),
        "free_cash_flow": info.get("freeCashflow"),
        "debt_to_equity": info.get("debtToEquity"),
        "return_on_equity": info.get("returnOnEquity"),
        "return_on_assets": info.get("returnOnAssets"),
    }

    return json.dumps(data, indent=2)


@mcp.tool()
async def get_multiple_quotes(symbols: list[str]) -> str:
    """Get current prices for multiple stocks at once.

    Args:
        symbols: List of stock ticker symbols (e.g. AAPL, GOOGL, MSFT)
    """
    results = []
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            results.append(
                {
                    "symbol": symbol.upper(),
                    "name": info.get("shortName", "N/A"),
                    "price": info.get("currentPrice") or info.get("regularMarketPrice"),
                    "change": info.get("regularMarketChange"),
                    "change_percent": info.get("regularMarketChangePercent"),
                    "volume": info.get("volume") or info.get("regularMarketVolume"),
                }
            )
        except Exception as e:
            results.append({"symbol": symbol.upper(), "error": str(e)})

    return json.dumps(results, indent=2)


@mcp.tool()
async def get_market_news(symbol: str) -> str:
    """Get recent news articles for a stock.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL, GOOGL)
    """
    ticker = yf.Ticker(symbol)
    news = ticker.news

    if not news:
        return json.dumps({"message": f"No recent news found for {symbol}"})

    articles = []
    for item in news[:10]:
        articles.append(
            {
                "title": item.get("title"),
                "publisher": item.get("publisher"),
                "link": item.get("link"),
                "published": item.get("providerPublishTime"),
                "type": item.get("type"),
            }
        )

    return json.dumps(articles, indent=2)


@mcp.tool()
async def get_analyst_recommendations(symbol: str) -> str:
    """Get analyst recommendations and price targets for a stock.

    Args:
        symbol: Stock ticker symbol (e.g. AAPL, GOOGL)
    """
    ticker = yf.Ticker(symbol)
    info = ticker.info

    data = {
        "symbol": symbol.upper(),
        "recommendation": info.get("recommendationKey", "N/A"),
        "recommendation_mean": info.get("recommendationMean"),
        "number_of_analysts": info.get("numberOfAnalystOpinions"),
        "target_high": info.get("targetHighPrice"),
        "target_low": info.get("targetLowPrice"),
        "target_mean": info.get("targetMeanPrice"),
        "target_median": info.get("targetMedianPrice"),
        "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
    }

    # Calculate upside/downside potential
    if data["target_mean"] and data["current_price"]:
        upside = (data["target_mean"] - data["current_price"]) / data["current_price"] * 100
        data["upside_potential"] = round(upside, 2)

    return json.dumps(data, indent=2)


def main():
    logger.info("Starting Live Market Data MCP Server...")
    mcp.run(transport="stdio")
    logger.info("Server stopped")


if __name__ == "__main__":
    main()
 