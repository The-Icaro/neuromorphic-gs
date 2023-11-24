from dataclasses import dataclass
from json import loads, dumps
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List
from datetime import datetime, timedelta

from app.clients.base_api import BaseApiClient
from app.dtos.thingspeak import ThingspeakResponse


@dataclass
class ThingspeakApiClient(BaseApiClient):
    async def get_data_chunk(self, start: datetime, end: datetime) -> List[ThingspeakResponse]:
        start_str = start.strftime("%Y-%m-%d %H:%M:%S")
        end_str = end.strftime("%Y-%m-%d %H:%M:%S")
        
        response = self.get(
            "/channels/940553/feeds.json",
            params={"start": start_str, "end": end_str},
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

    async def get_data(self, size: int = 10000, chunk_loop: int = 5) -> List[ThingspeakResponse]:
        with ThreadPoolExecutor(max_workers=5) as executor:
            loop = asyncio.get_event_loop()
            tasks = []

            current_date = datetime.today()

            for _ in range(0, size, chunk_loop):
                end_date = current_date
                start_date = current_date - timedelta(hours=chunk_loop)

                current_date = start_date

                tasks.append(loop.run_in_executor(executor, self.get_data_chunk, start_date, end_date))

            responses = await asyncio.gather(*tasks)

        return responses
