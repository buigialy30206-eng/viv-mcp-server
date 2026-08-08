# Viv Data MCP Server

23 free APIs accessible by AI agents via the Model Context Protocol.

## APIs available to AI

- **Steam** — game details, player counts, reviews, deals
- **Domain WHOIS** — registrar, dates, nameservers
- **Email Validator** — MX, DNS, disposable check
- **IP Geolocation** — country, city, ISP
- **Currency Converter** — 170+ currencies
- **Stock Price** — real-time quotes

## Quick Start

```bash
pip install mcp httpx
git clone https://github.com/buigialy30206-eng/viv-mcp-server
```

## Connect to Claude Desktop

Add to `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "viv-data": {
      "command": "python",
      "args": ["path/to/viv-mcp-server.py"]
    }
  }
}
```

Then ask Claude: *"How many people are playing CS2 right now?"* — it'll use the API.

## Register on MCP Marketplaces

- [Smithery](https://smithery.ai) — submit `viv-mcp-server`
- [Model Context Protocol Hub](https://github.com/modelcontextprotocol/servers) — submit a PR
