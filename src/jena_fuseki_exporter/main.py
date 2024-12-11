import asyncio
import logging
from urllib.parse import urlencode, quote

import httpx
from cachetools import cached, TTLCache
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cache_ttl: int = 300
    url: str = "http://jena-fuseki.integration/slice/"
    query: str = """SELECT (COUNT(DISTINCT ?g) AS ?numGraphs)
WHERE {
  GRAPH ?g {
    # Optional condition: ?s ?p ?o .
  }
}"""


settings = Settings()
lock = asyncio.Lock()
cache = TTLCache(maxsize=100_000, ttl=settings.cache_ttl)
app = FastAPI()


@app.get("/metrics")
async def root():
    try:
        graphs_number = await retrieve_cached()
    except Exception as e:
        logging.warn(e)
        raise HTTPException(status_code=502, detail="Bad Gateway: Upstream server error")
    metrics = 'jena_fuseki_exporter_graphs_count{dataset="slice"} ' + str(graphs_number)
    return PlainTextResponse(metrics)


async def retrieve_cached() -> int:
    if 0 in cache:
        return cache[0]
    async with lock:
        result = await retrieve()
        cache[0] = result
    return result


async def retrieve() -> int:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            settings.url,
            content=urlencode(
                {"query": settings.query},
                quote_via=quote,
            ),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        logging.info(f"Downstream call POST {settings.url}")
        graphs_number = int(r.json()["results"]["bindings"][0]["numGraphs"]["value"])
    return graphs_number