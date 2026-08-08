"""
Viv Data MCP Server — 23 free APIs accessible by AI agents.
Install: uv pip install mcp httpx
Run: python viv-mcp-server.py
Connect: Claude Desktop, Cursor, Continue, etc.
"""
import json, httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("viv-data")
BASE = "https://mega-api-mellowed-tidepool-1271.fly.dev"

async def get(url):
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.get(url)
        return r.json()

# === STEAM ===
@server.tool()
async def steam_game(appid: int = 730) -> dict:
    """Get Steam game details: name, price, developer, genres, release date.

Use the Steam app ID — e.g., 730 for CS2, 271590 for GTA V, 1245620 for Elden Ring."""
    return await get(f"{BASE}/steam/game?appid={appid}")

@server.tool()
async def steam_players(appid: int = 730) -> dict:
    """Get current live player count for any Steam game."""
    return await get(f"{BASE}/steam/players?appid={appid}")

@server.tool()
async def steam_reviews(appid: int = 730) -> dict:
    """Get review summary: total positive/negative reviews, overall score."""
    return await get(f"{BASE}/steam/reviews?appid={appid}")

@server.tool()
async def steam_deals() -> dict:
    """Get current Steam sales and discounted games."""
    return await get(f"{BASE}/steam/deals")

# === WHOIS ===
@server.tool()
async def whois_lookup(domain: str) -> dict:
    """Look up domain WHOIS/RDAP info: registrar, creation date, expiration, nameservers."""
    return await get(f"{BASE}/whois/lookup?domain={domain}")

# === EMAIL ===
@server.tool()
async def email_validate(email: str) -> dict:
    """Validate email: check MX records, syntax, disposable domains, catch-all."""
    return await get(f"{BASE}/email/validate?email={email}")

# === IP GEO ===
@server.tool()
async def ip_geolocation(ip: str) -> dict:
    """Get geolocation, ISP, and timezone for any IP address."""
    return await get(f"{BASE}/ipgeo?ip={ip}")

# === CURRENCY ===
@server.tool()
async def currency_convert(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convert currency between 170+ world currencies in real-time."""
    return await get(f"{BASE}/currency/convert?amount={amount}&from={from_currency}&to={to_currency}")

# === STOCK ===
@server.tool()
async def stock_price(symbol: str) -> dict:
    """Get real-time stock quote: price, change, volume, 52-week high/low."""
    return await get(f"{BASE}/stock/quote?symbol={symbol}")

async def main():
    async with stdio_server() as streams:
        await server.run(streams)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
