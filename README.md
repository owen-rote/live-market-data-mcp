# Live Market Data MCP

An MCP server for connecting LLMs to live market data via yfinance.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (python package manager)
  - [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
- Claude Desktop App (or any MCP-compatible client)
- nodejs (for MCP server)

## Installation

```bash
# Install uv if you haven't already
# =================================
# Mac/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell):
curl -LsSf https://astral.sh/uv/install.sh | sh

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

| Tool                          | Description                                             |
| ----------------------------- | ------------------------------------------------------- |
| `get_stock_price`             | Current price, volume, day range, 52-week range         |
| `get_stock_history`           | Historical OHLCV data with customizable period/interval |
| `get_company_info`            | Company details (sector, industry, description)         |
| `get_financial_metrics`       | PE ratio, EPS, dividend yield, margins                  |
| `get_multiple_quotes`         | Batch quotes for multiple symbols                       |
| `get_market_news`             | Recent news articles for a stock                        |
| `get_analyst_recommendations` | Price targets and analyst ratings                       |
