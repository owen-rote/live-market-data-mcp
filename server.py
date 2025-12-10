# Author: Owen Rotenberg
# Provides real-time stock market data via yfinance as MCP tools.

import json
from typing import Any

import yfinance as yf
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("live-market-data")


def _get_ticker(symbol: str) -> yf.Ticker:
    return yf.Ticker(symbol)


def _json(data: Any) -> str:
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_current_quote(symbol: str) -> str:
    """Get the latest real-time quote for a stock including price, change, and volume.

    Use this to check the current trading price and today's performance of any stock.

    Args:
        symbol: Stock ticker symbol (e.g., AAPL, GOOGL, MSFT, TSLA).

    Returns:
        JSON with current price, price change (absolute and percent), volume,
        bid/ask prices, and today's trading range.
    """
    info = _get_ticker(symbol).info
    current = info.get("currentPrice") or info.get("regularMarketPrice")
    prev_close = info.get("previousClose")

    change = None
    change_pct = None
    if current and prev_close:
        change = round(current - prev_close, 2)
        change_pct = round((change / prev_close) * 100, 2)

    return _json(
        {
            "symbol": symbol.upper(),
            "name": info.get("shortName", "N/A"),
            "price": current,
            "change": change,
            "change_percent": change_pct,
            "previous_close": prev_close,
            "open": info.get("open") or info.get("regularMarketOpen"),
            "day_high": info.get("dayHigh") or info.get("regularMarketDayHigh"),
            "day_low": info.get("dayLow") or info.get("regularMarketDayLow"),
            "volume": info.get("volume") or info.get("regularMarketVolume"),
            "bid": info.get("bid"),
            "ask": info.get("ask"),
            "currency": info.get("currency", "USD"),
        }
    )


@mcp.tool()
async def get_price_history(
    symbol: str,
    period: str = "1mo",
    interval: str = "1d",
) -> str:
    """Get historical OHLCV (Open, High, Low, Close, Volume) price data for charting or analysis.

    Use this for technical analysis, plotting price charts, or analyzing price trends over time.

    Args:
        symbol: Stock ticker symbol (e.g., AAPL, GOOGL).
        period: How far back to retrieve data. Options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max.
        interval: Time between data points. Options: 1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo.
            Note: Intraday intervals (1m-1h) only available for recent periods.

    Returns:
        JSON with array of OHLCV candles, each containing date, open, high, low, close, and volume.
    """
    hist = _get_ticker(symbol).history(period=period, interval=interval)

    if hist.empty:
        return _json({"error": f"No historical data found for {symbol}"})

    records = [
        {
            "date": str(date),
            "open": round(row["Open"], 2),
            "high": round(row["High"], 2),
            "low": round(row["Low"], 2),
            "close": round(row["Close"], 2),
            "volume": int(row["Volume"]),
        }
        for date, row in hist.iterrows()
    ]

    return _json(
        {
            "symbol": symbol.upper(),
            "period": period,
            "interval": interval,
            "data_points": len(records),
            "history": records,
        }
    )


@mcp.tool()
async def get_company_profile(symbol: str) -> str:
    """Get company business description, sector, industry, and corporate details.

    Use this to learn what a company does, its industry classification, and basic corporate info.

    Args:
        symbol: Stock ticker symbol (e.g., AAPL, GOOGL).

    Returns:
        JSON with company name, sector, industry, business description, country,
        website, employee count, and CEO name.
    """
    info = _get_ticker(symbol).info
    officers = info.get("companyOfficers", [])

    return _json(
        {
            "symbol": symbol.upper(),
            "name": info.get("longName") or info.get("shortName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "description": info.get("longBusinessSummary", "N/A"),
            "country": info.get("country", "N/A"),
            "website": info.get("website", "N/A"),
            "employees": info.get("fullTimeEmployees"),
            "ceo": officers[0].get("name") if officers else "N/A",
        }
    )


@mcp.tool()
async def get_key_statistics(symbol: str) -> str:
    """Get market statistics including market cap, 52-week range, beta, and shares outstanding.

    Use this for market sizing, volatility assessment, and understanding stock's market position.

    Args:
        symbol: Stock ticker symbol (e.g., AAPL, GOOGL).

    Returns:
        JSON with market cap, enterprise value, 52-week high/low, beta,
        shares outstanding, float, and short interest data.
    """
    info = _get_ticker(symbol).info
    return _json(
        {
            "symbol": symbol.upper(),
            "market_cap": info.get("marketCap"),
            "enterprise_value": info.get("enterpriseValue"),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
            "fifty_day_average": info.get("fiftyDayAverage"),
            "two_hundred_day_average": info.get("twoHundredDayAverage"),
            "beta": info.get("beta"),
            "shares_outstanding": info.get("sharesOutstanding"),
            "float_shares": info.get("floatShares"),
            "short_ratio": info.get("shortRatio"),
            "short_percent_of_float": info.get("shortPercentOfFloat"),
            "held_percent_insiders": info.get("heldPercentInsiders"),
            "held_percent_institutions": info.get("heldPercentInstitutions"),
        }
    )


@mcp.tool()
async def get_valuation_metrics(symbol: str) -> str:
    """Get valuation ratios like P/E, P/B, PEG, and EV/EBITDA for fundamental analysis.

    Use this to assess if a stock is overvalued or undervalued relative to earnings and assets.

    Args:
        symbol: Stock ticker symbol (e.g., AAPL, GOOGL).

    Returns:
        JSON with trailing P/E, forward P/E, PEG ratio, price-to-book,
        price-to-sales, and EV/EBITDA ratios.
    """
    info = _get_ticker(symbol).info
    return _json(
        {
            "symbol": symbol.upper(),
            "trailing_pe": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "peg_ratio": info.get("pegRatio"),
            "price_to_book": info.get("priceToBook"),
            "price_to_sales": info.get("priceToSalesTrailing12Months"),
            "enterprise_to_revenue": info.get("enterpriseToRevenue"),
            "enterprise_to_ebitda": info.get("enterpriseToEbitda"),
            "trailing_eps": info.get("trailingEps"),
            "forward_eps": info.get("forwardEps"),
            "book_value": info.get("bookValue"),
        }
    )


@mcp.tool()
async def get_financial_health(symbol: str) -> str:
    """Get profitability, margins, returns, and balance sheet health indicators.

    Use this to assess a company's financial strength, profitability, and operational efficiency.

    Args:
        symbol: Stock ticker symbol (e.g., AAPL, GOOGL).

    Returns:
        JSON with profit margins, ROE, ROA, debt-to-equity, current ratio,
        revenue, EBITDA, and cash flow metrics.
    """
    info = _get_ticker(symbol).info
    return _json(
        {
            "symbol": symbol.upper(),
            "profit_margin": info.get("profitMargins"),
            "operating_margin": info.get("operatingMargins"),
            "gross_margin": info.get("grossMargins"),
            "return_on_equity": info.get("returnOnEquity"),
            "return_on_assets": info.get("returnOnAssets"),
            "debt_to_equity": info.get("debtToEquity"),
            "current_ratio": info.get("currentRatio"),
            "quick_ratio": info.get("quickRatio"),
            "total_revenue": info.get("totalRevenue"),
            "revenue_growth": info.get("revenueGrowth"),
            "earnings_growth": info.get("earningsGrowth"),
            "ebitda": info.get("ebitda"),
            "free_cash_flow": info.get("freeCashflow"),
            "operating_cash_flow": info.get("operatingCashflow"),
            "total_cash": info.get("totalCash"),
            "total_debt": info.get("totalDebt"),
        }
    )


@mcp.tool()
async def get_dividend_info(symbol: str) -> str:
    """Get dividend yield, payout ratio, and dividend history details.

    Use this to evaluate a stock's income potential and dividend sustainability.

    Args:
        symbol: Stock ticker symbol (e.g., AAPL, KO, JNJ).

    Returns:
        JSON with dividend yield, annual dividend rate, payout ratio,
        ex-dividend date, and 5-year average yield.
    """
    info = _get_ticker(symbol).info
    return _json(
        {
            "symbol": symbol.upper(),
            "dividend_yield": info.get("dividendYield"),
            "dividend_rate": info.get("dividendRate"),
            "payout_ratio": info.get("payoutRatio"),
            "ex_dividend_date": info.get("exDividendDate"),
            "last_dividend_value": info.get("lastDividendValue"),
            "last_dividend_date": info.get("lastDividendDate"),
            "five_year_avg_dividend_yield": info.get("fiveYearAvgDividendYield"),
            "trailing_annual_dividend_rate": info.get("trailingAnnualDividendRate"),
            "trailing_annual_dividend_yield": info.get("trailingAnnualDividendYield"),
        }
    )


@mcp.tool()
async def get_analyst_targets(symbol: str) -> str:
    """Get Wall Street analyst price targets and buy/sell/hold recommendations.

    Use this to see what professional analysts think about a stock's future price.

    Args:
        symbol: Stock ticker symbol (e.g., AAPL, GOOGL).

    Returns:
        JSON with consensus recommendation, number of analysts, price target
        (high, low, mean, median), and calculated upside potential.
    """
    info = _get_ticker(symbol).info
    current = info.get("currentPrice") or info.get("regularMarketPrice")
    target_mean = info.get("targetMeanPrice")

    data = {
        "symbol": symbol.upper(),
        "recommendation": info.get("recommendationKey", "N/A"),
        "recommendation_mean": info.get("recommendationMean"),
        "number_of_analysts": info.get("numberOfAnalystOpinions"),
        "target_high": info.get("targetHighPrice"),
        "target_low": info.get("targetLowPrice"),
        "target_mean": target_mean,
        "target_median": info.get("targetMedianPrice"),
        "current_price": current,
    }

    if target_mean and current:
        data["upside_percent"] = round((target_mean - current) / current * 100, 2)

    return _json(data)


@mcp.tool()
async def get_stock_news(symbol: str, max_articles: int = 10) -> str:
    """Get recent news headlines and articles about a specific stock.

    Use this to stay informed about company developments, earnings, and market-moving events.

    Args:
        symbol: Stock ticker symbol (e.g., AAPL, GOOGL).
        max_articles: Maximum number of articles to return (default 10, max 25).

    Returns:
        JSON array of news articles with title, publisher, link, and publish timestamp.
    """
    news = _get_ticker(symbol).news
    max_articles = min(max_articles, 25)

    if not news:
        return _json({"message": f"No recent news found for {symbol}"})

    return _json(
        {
            "symbol": symbol.upper(),
            "article_count": min(len(news), max_articles),
            "articles": [
                {
                    "title": item.get("title"),
                    "publisher": item.get("publisher"),
                    "link": item.get("link"),
                    "published": item.get("providerPublishTime"),
                }
                for item in news[:max_articles]
            ],
        }
    )


@mcp.tool()
async def compare_stocks(symbols: list[str]) -> str:
    """Compare key metrics across multiple stocks side-by-side.

    Use this to compare valuations, performance, and fundamentals of competing stocks
    or portfolio candidates.

    Args:
        symbols: List of 2-10 ticker symbols to compare (e.g., ["AAPL", "MSFT", "GOOGL"]).

    Returns:
        JSON array with each stock's price, market cap, P/E, dividend yield,
        and year-to-date performance for easy comparison.
    """
    symbols = symbols[:10]  # Limit to 10 symbols
    results = []

    for symbol in symbols:
        try:
            info = _get_ticker(symbol).info
            current = info.get("currentPrice") or info.get("regularMarketPrice")
            year_high = info.get("fiftyTwoWeekHigh")
            year_low = info.get("fiftyTwoWeekLow")

            ytd_change = None
            if current and year_low:
                ytd_change = round((current - year_low) / year_low * 100, 2)

            results.append(
                {
                    "symbol": symbol.upper(),
                    "name": info.get("shortName", "N/A"),
                    "price": current,
                    "market_cap": info.get("marketCap"),
                    "pe_ratio": info.get("trailingPE"),
                    "forward_pe": info.get("forwardPE"),
                    "dividend_yield": info.get("dividendYield"),
                    "beta": info.get("beta"),
                    "fifty_two_week_high": year_high,
                    "fifty_two_week_low": year_low,
                    "percent_from_52w_low": ytd_change,
                    "profit_margin": info.get("profitMargins"),
                    "revenue_growth": info.get("revenueGrowth"),
                }
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            results.append({"symbol": symbol.upper(), "error": str(e)})

    return _json({"comparison": results, "stocks_compared": len(results)})


if __name__ == "__main__":
    mcp.run(transport="sse")
