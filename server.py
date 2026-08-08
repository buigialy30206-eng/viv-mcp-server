"""MCP Server with SSE transport — all 25 tools deployed to Fly.io."""
import json, httpx
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

async def post(path, data=None):
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.post(f"{BASE}{path}", json=data or {})
        return r.json()

# === STEAM (5) ===
@server.tool()
async def steam_game(appid: int = 730) -> dict:
    """Steam game details: name, price, developer, genres, release date."""
    return await get(f"/steam/game?appid={appid}")

@server.tool()
async def steam_players(appid: int = 730) -> dict:
    """Live player count for any Steam game."""
    return await get(f"/steam/players?appid={appid}")

@server.tool()
async def steam_reviews(appid: int = 730) -> dict:
    """Steam review summary: score, positive, negative, total."""
    return await get(f"/steam/reviews?appid={appid}")

@server.tool()
async def steam_deals() -> dict:
    """Current Steam sales and discounted games."""
    return await get(f"/steam/deals")

@server.tool()
async def steam_player_history(appid: int = 730) -> dict:
    """90-day player count history for any Steam game."""
    return await get(f"/steam/players/history?appid={appid}")

# === WHOIS ===
@server.tool()
async def whois_lookup(domain: str) -> dict:
    """Domain WHOIS/RDAP: registrar, dates, nameservers."""
    return await get(f"/whois/lookup?domain={domain}")

# === EMAIL ===
@server.tool()
async def email_validate(email: str) -> dict:
    """Validate email: MX, syntax, disposable, catch-all."""
    return await get(f"/email/validate?email={email}")

# === IP GEO ===
@server.tool()
async def ip_geolocation(ip: str) -> dict:
    """IP geolocation: country, city, ISP, timezone."""
    return await get(f"/ipgeo?ip={ip}")

# === CURRENCY ===
@server.tool()
async def currency_convert(amount: float, from_curr: str, to_curr: str) -> dict:
    """Convert between 170+ currencies in real-time."""
    return await get(f"/currency/convert?amount={amount}&from={from_curr}&to={to_curr}")

# === STOCK ===
@server.tool()
async def stock_price(symbol: str) -> dict:
    """Real-time stock quote: price, change, volume, 52-week high/low."""
    return await get(f"/stock/quote?symbol={symbol}")

# === COMPANY ===
@server.tool()
async def company_info(domain: str) -> dict:
    """Company registration info lookup by domain."""
    return await get(f"/company?domain={domain}")

# === QR CODE ===
@server.tool()
async def qrcode_generate(text: str, size: int = 200) -> dict:
    """Generate a QR code image URL for any text or URL."""
    return await get(f"/qrcode/generate?text={text}&size={size}")

# === BARCODE ===
@server.tool()
async def barcode_generate(text: str, barcode_type: str = "code128") -> dict:
    """Generate a barcode image URL."""
    return await get(f"/barcode/generate?text={text}&type={barcode_type}")

# === PDF TO TEXT ===
@server.tool()
async def pdf_to_text(url: str) -> dict:
    """Extract text from a PDF file URL."""
    return await get(f"/pdf/extract?url={url}")

# === UUID ===
@server.tool()
async def uuid_generate(count: int = 1) -> dict:
    """Generate random UUID v4 identifiers."""
    return await get(f"/uuid?count={count}")

# === RANDOM USER ===
@server.tool()
async def random_user(gender: str = "random", nationality: str = "us") -> dict:
    """Generate random fake user profiles for testing."""
    return await get(f"/random-user?gender={gender}&nat={nationality}")

# === PASSWORD ===
@server.tool()
async def password_strength(password: str) -> dict:
    """Check password strength: entropy, crack time, score."""
    return await get(f"/password?password={password}")

# === SENTIMENT ===
@server.tool()
async def sentiment_analysis(text: str) -> dict:
    """Analyze text sentiment: positive, negative, neutral."""
    return await get(f"/sentiment?text={text}")

# === LANGUAGE DETECT ===
@server.tool()
async def language_detect(text: str) -> dict:
    """Detect language of text among 55+ languages."""
    return await get(f"/lang/detect?text={text}")

# === PHONE LOOKUP ===
@server.tool()
async def phone_lookup(number: str) -> dict:
    """Phone number lookup: country, carrier, line type."""
    return await get(f"/phone?number={number}")

# === VAT VALIDATOR ===
@server.tool()
async def vat_validate(vat_number: str, country: str = "auto") -> dict:
    """Validate EU VAT numbers via VIES."""
    return await get(f"/vat?vat={vat_number}&country={country}")

# === USER AGENT PARSER ===
@server.tool()
async def ua_parse(user_agent: str) -> dict:
    """Parse User-Agent string: browser, OS, device."""
    return await get(f"/ua?ua={user_agent}")

# === MARKDOWN ===
@server.tool()
async def markdown_to_html(markdown: str) -> dict:
    """Convert Markdown text to HTML."""
    return await post("/markdown/convert", {"text": markdown})

# === SLUG ===
@server.tool()
async def slug_generate(text: str) -> dict:
    """Convert text to URL-friendly slug."""
    return await get(f"/slug?text={text}")

# === METADATA ===
@server.tool()
async def url_metadata(url: str) -> dict:
    """Extract metadata from a URL: title, description, image."""
    return await get(f"/metadata?url={url}")

# === PLACES SEARCH ===
@server.tool()
async def places_search(query: str, lat: float = 0, lng: float = 0) -> dict:
    """Search for places: restaurants, hotels, shops nearby."""
    return await get(f"/places/search?q={query}&lat={lat}&lng={lng}")

# SSE transport
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
