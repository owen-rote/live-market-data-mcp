from mcp.server.fastmcp import FastMCP
import yfinance as yf

# Initialize FastMCP server
mcp = FastMCP("live-market-data-mcp")


@mcp.tool()
def get_stock_price(ticker: str) -> float:
    """Get the current stock price for a given ticker symbol."""
    ticker_data = yf.Ticker(ticker)
    history = ticker_data.history(period="1d")
    if history.empty:
        raise ValueError(f"No data found for ticker {ticker}")
    return history["Close"].iloc[-1]


def main():
    mcp.run()


if __name__ == "__main__":
    main()
