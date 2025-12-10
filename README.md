# Live Market Data MCP

An MCP server providing real-time stock market data to LLMs via yfinance. Designed for Claude and other MCP-compatible AI assistants to fetch live financial data.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (python package manager)
- Claude Desktop App (or any MCP-compatible client. ChatGPT etc)

## Installation

```bash
# Install uv if you haven't already
# =================================
# Mac/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell):
irm https://astral.sh/uv/install.ps1 | iex

# Install dependencies with uv
cd live-market-data-mcp
uv sync

# Configure Claude Desktop
# ========================
# Mac/Linux:
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
# Windows:
code $env:AppData\Claude\claude_desktop_config.json

# Add the following MCP server configuration:
"mcpServers": {
    "live-market-data": {
        "command": "uv",
        "args": [
            "--directory",
            "path/to/live-market-data-mcp",
            "run",
            "server.py"
        ]
    }
}
```

## Available Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| `get_current_quote` | Real-time price, change, volume, bid/ask | Check current stock price and today's performance |
| `get_price_history` | Historical OHLCV data with configurable period/interval | Technical analysis, charting, trend analysis |
| `get_company_profile` | Business description, sector, industry, CEO | Learn what a company does and its classification |
| `get_key_statistics` | Market cap, 52-week range, beta, short interest | Market sizing and volatility assessment |
| `get_valuation_metrics` | P/E, P/B, PEG, EV/EBITDA ratios | Fundamental analysis, valuation comparison |
| `get_financial_health` | Margins, ROE, ROA, debt ratios, cash flow | Assess financial strength and profitability |
| `get_dividend_info` | Yield, payout ratio, ex-dividend dates | Evaluate income potential and dividend sustainability |
| `get_analyst_targets` | Price targets and buy/sell/hold ratings | See Wall Street analyst consensus |
| `get_stock_news` | Recent headlines and articles (up to 25) | Stay informed on company developments |
| `compare_stocks` | Side-by-side comparison of up to 10 stocks | Compare competitors or portfolio candidates |

## Example Prompts

- "What's the current price of AAPL?"
- "Compare the valuations of MSFT, GOOGL, and AMZN"
- "Show me Tesla's price history for the past 6 months"
- "What do analysts think about NVDA?"
- "Is Disney a good dividend stock?"
- "What does Palantir do as a company?"
