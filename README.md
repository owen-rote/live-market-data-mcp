# Live Market Data MCP

## Requirements:

- Python 3.10+
- Claude Desktop App (Or any other MCP-compatible LLM client)

## Usage:

```bash
# Create and Activate Python virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install
pip install -e .

# Get MCP server path
which live-market-data-mcp

# 4. Configure Claude Desktop
# Edit: 
# Mac/Linux: ~/Library/Application Support/Claude/claude_desktop_config.json
# Windows: %APPDATA%\Claude\claude_desktop_config.json
# Add:
{
  "mcpServers": {
    "finance": {
      "command": "/your/path/from/step3/venv/bin/live-market-data-mcp"
    }
  }
}
```