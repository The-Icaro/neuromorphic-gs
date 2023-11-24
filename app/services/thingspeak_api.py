from dataclasses import dataclass
from json import loads, dumps
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

from app.clients.base_api import BaseApiClient
from app.dtos.thingspeak import ThingspeakResponse


@dataclass
class ThingspeakApiClient(BaseApiClient):
    async def get_data_chunk(self, start: int, end: int) -> List[ThingspeakResponse]:
        response = self.get(
            "/channels/1293177/feeds.json",
            params={"start": start, "end": end},
        )
        if response.get("error"):
            raise response.get("error")

        json_body = loads(response.get("body"))
        for feed in json_body.get("feeds", []):
            for key, value in feed.items():
                if key.startswith("field") and value.lower() in ["nan"]:
                    feed[key] = 0.0

        cleaned_response = dumps(json_body)

        return ThingspeakResponse.schema().loads(cleaned_response)

    async def get_data(self, size: int = 10000, chunk_size: int = 100) -> List[ThingspeakResponse]:
        with ThreadPoolExecutor(max_workers=5) as executor:
            loop = asyncio.get_event_loop()
            tasks = []

            for start in range(0, size, chunk_size):
                end = min(start + chunk_size, size)
                tasks.append(loop.run_in_executor(executor, self.get_data_chunk, start, end))

            responses = await asyncio.gather(*tasks)

        return responses
