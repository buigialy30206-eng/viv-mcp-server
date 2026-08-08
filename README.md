# Viv Data MCP Server

**23 free APIs — now usable by Claude, Cursor, Continue, and any MCP-compatible AI agent.**

Ask an AI "How many people are playing CS2?" or "Who owns github.com?" and it'll call these APIs directly.

## APIs Available

| Category | Tools | Example |
|----------|-------|---------|
| 🎮 **Steam** | Game details, player counts, reviews, deals, history | CS2 → 850K players, Very Positive |
| 🌐 **Domain WHOIS** | Registrar, dates, nameservers | github.com → MarkMonitor |
| 📧 **Email** | MX records, syntax, disposables | user@example.com → Valid |
| 🌍 **IP Geo** | Country, city, ISP, timezone | 8.8.8.8 → US, Google |
| 💱 **Currency** | 170+ currencies, real-time | 100 USD → 85 EUR |
| 📈 **Stocks** | Real-time quotes | AAPL → $174.50 |
| 📱 **QR Code** | Generate image URL | Any text → PNG/SVG |
| 🏢 **Company** | Business registration | domain → company info |
| ... | 15 more tools | Password, UUID, VAT, Phone, Sentiment, etc. |

## Quick Start

```bash
pip install mcp httpx
git clone https://github.com/buigialy30206-eng/viv-mcp-server
```

## Connect to Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "viv-data": {
      "command": "python",
      "args": ["path/to/viv-mcp-server/viv-mcp-server.py"]
    }
  }
}
```

Restart Claude. Then ask: *"What's the CS2 player count right now?"*

## Connect to Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "viv-data": {
      "command": "python",
      "args": ["path/to/viv-mcp-server/viv-mcp-server.py"]
    }
  }
}
```

## Hosted API

| Server | URL |
|--------|-----|
| MCP (SSE) | `https://viv-mcp-server.fly.dev` |
| REST API | `https://mega-api-mellowed-tidepool-1271.fly.dev` |
| RapidAPI | [buigialy30206](https://rapidapi.com/buigialy30206/api/domain-whois-api1) |
| npm | `npm install github:buigialy30206-eng/steam-api-npm` |

## License

MIT — free forever.
