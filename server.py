"""
MCP Server with SSE transport — deploy to Fly.io, connect to Smithery.
"""
import json, httpx, asyncio
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route

server = Server("viv-data")
BASE = "https://mega-api-mellowed-tidepool-1271.fly.dev"

async def get(path):
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.get(f"{BASE}{path}")
        return r.json()

@server.tool()
async def steam_game(appid: int = 730) -> dict:
    """Steam game details: name, price, developer, genres, release date. Use appid=730 for CS2."""
    return await get(f"/steam/game?appid={appid}")

@server.tool()
async def steam_players(appid: int = 730) -> dict:
    """Live player count for any Steam game."""
    return await get(f"/steam/players?appid={appid}")

@server.tool()
async def steam_reviews(appid: int = 730) -> dict:
    """Steam review summary: score, positive/negative counts."""
    return await get(f"/steam/reviews?appid={appid}")

@server.tool()
async def steam_deals() -> dict:
    """Current Steam sales and discounted games."""
    return await get(f"/steam/deals")

@server.tool()
async def steam_player_history(appid: int = 730) -> dict:
    """90-day player count history for any Steam game."""
    return await get(f"/steam/players/history?appid={appid}")

@server.tool()
async def whois_lookup(domain: str) -> dict:
    """Domain WHOIS/RDAP: registrar, creation/expiry dates, nameservers."""
    return await get(f"/whois/lookup?domain={domain}")

@server.tool()
async def email_validate(email: str) -> dict:
    """Validate email: MX records, syntax, disposable domain, catch-all."""
    return await get(f"/email/validate?email={email}")

@server.tool()
async def ip_geolocation(ip: str) -> dict:
    """IP geolocation: country, city, ISP, timezone."""
    return await get(f"/ipgeo?ip={ip}")

@server.tool()
async def currency_convert(amount: float, from_curr: str, to_curr: str) -> dict:
    """Convert between 170+ currencies in real-time."""
    return await get(f"/currency/convert?amount={amount}&from={from_curr}&to={to_curr}")

@server.tool()
async def stock_price(symbol: str) -> dict:
    """Real-time stock quote: price, change, volume, 52-week high/low."""
    return await get(f"/stock/quote?symbol={symbol}")

@server.tool()
async def qrcode_generate(text: str, size: int = 200) -> dict:
    """Generate a QR code image URL for any text or URL."""
    return await get(f"/qrcode/generate?text={text}&size={size}")

@server.tool()
async def company_lookup(domain: str) -> dict:
    """Company registration info by domain."""
    return await get(f"/company?domain={domain}")

sse = SseServerTransport("/messages/")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(streams[0], streams[1])

async def handle_messages(request):
    await sse.handle_post_message(request.scope, request.receive, request._send)

app = Starlette(debug=False, routes=[
    Route("/sse", endpoint=handle_sse),
    Route("/messages/", endpoint=handle_messages, methods=["POST"]),
])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
