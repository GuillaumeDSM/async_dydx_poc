import time

import aiohttp
import json
import dydx3
import dydx3.errors
import dydx3.modules.public
import dydx3.helpers.requests
import dydx3.helpers.request_helpers


class AIOdYdXPublic(dydx3.modules.public.Public):
    def __init__(self, sync_public, aiorequest_factory):
        super().__init__(sync_public.host, api_timeout=sync_public.api_timeout)
        self.aiorequest_factory = aiorequest_factory

    def _get(self, request_path, params={}):
        return self.aiorequest_factory(
            dydx3.helpers.request_helpers.generate_query_path(self.host + request_path, params),
            'get',
            api_timeout=self.api_timeout,
        )

    def _put(self, endpoint, data):
        return self.aiorequest_factory(
            self.host + '/v3/' + endpoint,
            'put',
            {},
            data,
            self.api_timeout,
        )


class AIOdYdXClient:
    def __init__(self):
        self.aiosession = aiohttp.ClientSession()
        self.dydx3_client = dydx3.Client(
            # url from https://dydxprotocol.github.io/v3-teacher/#usage-2
            host="https://api.dydx.exchange",
        )
        self.dydx3_client._public = AIOdYdXPublic(self.dydx3_client._public, self._aiorequest)

    async def _aiorequest(self, uri, method, headers=None, data_values={}, api_timeout=None):
        async with getattr(self.aiosession, method)(
                uri,
                headers=headers,
                data=json.dumps(
                    dydx3.helpers.request_helpers.remove_nones(data_values)
                ),
                timeout=api_timeout
        ) as response:
            print(f"resp {time.time()}")
            if not str(response.status).startswith('2'):
                raise dydx3.errors.DydxApiError(response)

            if response.content:
                return dydx3.helpers.requests.Response(await response.json(), response.headers)
            else:
                return dydx3.helpers.requests.Response('{}', response.headers)

    def _patch_request_module(self):
        # other option with patching
        dydx3.modules.public.request = self._aiorequest

    async def get_candles(self, market, resolution):
        return await self.dydx3_client.public.get_candles(market, resolution=resolution)

    async def close(self):
        await self.aiosession.close()
