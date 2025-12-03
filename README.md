# Live Market Data MCP

An MCP server for connecting LLMs to live market data via yfinance.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Claude Desktop App (or any MCP-compatible client)

## Installation

```bash
# Install dependencies with uv
uv sync
```

## Configure Claude Desktop

Edit your Claude Desktop config:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Standard (Mac/Linux)

```json
{
  "mcpServers": {
    "finance": {
      "command": "uv",
      "args": ["--directory", "/path/to/live-market-data-mcp", "run", "live-market-data-mcp"]
    }
  }
}
```

### WSL → Windows Claude Desktop

```json
{
  "mcpServers": {
    "finance": {
      "command": "wsl.exe",
      "args": ["-d", "Ubuntu-24.04", "--", "uv", "--directory", "/home/USER/source/live-market-data-mcp", "run", "live-market-data-mcp"]
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_stock_price` | Current price, volume, day range, 52-week range |
| `get_stock_history` | Historical OHLCV data with customizable period/interval |
| `get_company_info` | Company details (sector, industry, description) |
| `get_financial_metrics` | PE ratio, EPS, dividend yield, margins |
| `get_multiple_quotes` | Batch quotes for multiple symbols |
| `get_market_news` | Recent news articles for a stock |
| `get_analyst_recommendations` | Price targets and analyst ratings |