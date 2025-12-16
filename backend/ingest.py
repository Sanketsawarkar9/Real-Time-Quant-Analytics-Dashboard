import sys
import os
import json
import asyncio
import websockets
from datetime import datetime

# --- Fix imports ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.database import init_db, insert_tick

# --- Binance settings ---
SYMBOLS = ["btcusdt", "ethusdt"]
BINANCE_WS = "wss://fstream.binance.com/ws"

# --- Initialize DB ---
init_db()

async def stream_symbol(symbol):
    url = f"{BINANCE_WS}/{symbol}@trade"
    async with websockets.connect(url) as ws:
        print(f"Connected to {symbol}")
        while True:
            msg = await ws.recv()
            data = json.loads(msg)

            tick = {
                "symbol": data["s"].lower(),
                "ts": datetime.utcfromtimestamp(data["T"] / 1000),
                "price": float(data["p"]),
                "size": float(data["q"]),
            }

            insert_tick(tick)

async def main():
    tasks = [stream_symbol(sym) for sym in SYMBOLS]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
