import time

import aiodydx
import asyncio

import dydx3


async def async_get_candles():
    MARKET_BTC_USD = "BTC-USD"
    client = aiodydx.AIOdYdXClient()
    try:
        t0 = time.time()
        await asyncio.gather(
            client.get_candles(MARKET_BTC_USD, resolution='1HOUR'),
            client.get_candles(MARKET_BTC_USD, resolution='1HOUR'),
            client.get_candles(MARKET_BTC_USD, resolution='1HOUR'),
            client.get_candles(MARKET_BTC_USD, resolution='1HOUR'),
            client.get_candles(MARKET_BTC_USD, resolution='1HOUR')
        )
        resp = await client.get_candles(MARKET_BTC_USD, resolution='1HOUR')
        candles = resp.data['candles']
        print(f"resp: {len(candles)} candles {round(time.time() - t0, 2)} s")
    finally:
        await client.close()


def sync_get_candles():
    MARKET_BTC_USD = "BTC-USD"
    client = dydx3.Client(
        # url from https://dydxprotocol.github.io/v3-teacher/#usage-2
        host="https://api.dydx.exchange",
    )
    t0 = time.time()
    client.public.get_candles(MARKET_BTC_USD, resolution='1HOUR')
    print(f"resp {time.time()}")
    client.public.get_candles(MARKET_BTC_USD, resolution='1HOUR')
    print(f"resp {time.time()}")
    client.public.get_candles(MARKET_BTC_USD, resolution='1HOUR')
    print(f"resp {time.time()}")
    client.public.get_candles(MARKET_BTC_USD, resolution='1HOUR')
    print(f"resp {time.time()}")
    client.public.get_candles(MARKET_BTC_USD, resolution='1HOUR')
    print(f"resp {time.time()}")
    resp = client.public.get_candles(MARKET_BTC_USD, resolution='1HOUR')
    candles = resp.data['candles']
    print(f"resp: {len(candles)} candles {round(time.time() - t0, 2)} s")

asyncio.run(async_get_candles())

sync_get_candles()
