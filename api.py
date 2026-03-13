import base64
from io import BytesIO
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
from binance.client import Client

# Initialize FastAPI application
app = FastAPI(
    title="Advanced Crypto Analytics API",
    description="API for real-time crypto analytics using multiple serializers."
)

def fetch_klines(symbol: str, interval: str, limit: int) -> pd.DataFrame:
    """Fetch klines data from Binance API and format as a pandas DataFrame."""
    client = Client()
    raw = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(
        raw,
        columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume", "trades", "taker_buy_base",
            "taker_buy_quote", "ignore",
        ],
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)
    return df

class PriceSummary(BaseModel):
    """Pydantic model for the JSON summary response."""
    symbol: str
    interval: str
    latest_close: float
    max_high: float
    min_low: float

# Endpoint 1: JSON Serializer
@app.get("/summary", response_model=PriceSummary)
def summary_json(
    symbol: str = Query("ETHUSDT", description="Trading pair symbol"),
    interval: str = Query("15m", description="Klines interval"),
    limit: int = Query(20, le=100, description="Number of data points")
):
    """Return a statistical summary of the recent price action in JSON format."""
    df = fetch_klines(symbol=symbol, interval=interval, limit=limit)
    return PriceSummary(
        symbol=symbol,
        interval=interval,
        latest_close=float(df.iloc[-1]["close"]),
        max_high=float(df["high"].max()),
        min_low=float(df["low"].min())
    )

# Endpoint 2: PNG Image Serializer
@app.get("/volume_chart")
def volume_chart_png(
    symbol: str = Query("ETHUSDT", description="Trading pair symbol"),
    limit: int = Query(60, le=120, description="Number of minutes")
) -> Response:
    """Render a trading volume bar chart as a PNG image."""
    df = fetch_klines(symbol=symbol, interval="1m", limit=limit)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["green" if row["close"] >= row["open"] else "red" for _, row in df.iterrows()]
    ax.bar(df["timestamp"], df["volume"], color=colors, width=0.0005)
    
    ax.set_title(f"{symbol} Trading Volume (Past {limit}m)")
    ax.set_ylabel("Volume")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=100)
    plt.close(fig)
    buf.seek(0)
    
    return Response(content=buf.getvalue(), media_type="image/png")

# Endpoint 3: CSV Text Serializer
@app.get("/export_data")
def export_csv(
    symbol: str = Query("ETHUSDT", description="Trading pair symbol"),
    limit: int = Query(10, le=50, description="Number of rows to export")
) -> Response:
    """Export raw OHLCV market data as a downloadable CSV file."""
    df = fetch_klines(symbol=symbol, interval="1m", limit=limit)
    csv_data = df[["timestamp", "open", "high", "low", "close", "volume"]].to_csv(index=False)
    
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={symbol}_market_data.csv"}
    )

# Endpoint 4: HTML Serializer
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_html(symbol: str = Query("ETHUSDT", description="Trading pair symbol")) -> HTMLResponse:
    """Return an interactive HTML dashboard integrating text stats and an image chart."""
    data_summary = summary_json(symbol=symbol, interval="1m", limit=60)
    png_bytes = volume_chart_png(symbol=symbol, limit=60).body
    b64_img = base64.b64encode(png_bytes).decode("utf-8")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{symbol} Market Dashboard</title>
        <style>
            body {{ font-family: sans-serif; padding: 20px; }}
            table {{ border-collapse: collapse; width: 300px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Market Dashboard: {symbol}</h1>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Latest Close</td><td>${data_summary.latest_close:.2f}</td></tr>
            <tr><td>Max High (Past 60m)</td><td>${data_summary.max_high:.2f}</td></tr>
            <tr><td>Min Low (Past 60m)</td><td>${data_summary.min_low:.2f}</td></tr>
        </table>
        <h2>Volume Chart (Past 60m)</h2>
        <img src="data:image/png;base64,{b64_img}" alt="{symbol} Volume Chart" style="border: 1px solid #ccc;"/>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


if __name__ == "__main__":
    # Allow running the API server directly via `python api.py` for easy debugging.
    # Use `uvicorn api:app --reload` for production-like behavior.
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)