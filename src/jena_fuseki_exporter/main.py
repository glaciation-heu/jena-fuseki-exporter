from urllib.parse import urlencode, quote

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    url: str = "http://jena-fuseki.integration/slice/"
    query: str = """SELECT (COUNT(DISTINCT ?g) AS ?numGraphs)
WHERE {
  GRAPH ?g {
    # Optional condition: ?s ?p ?o .
  }
}"""


settings = Settings()
app = FastAPI()


@app.get("/metrics")
async def root():
    try:
       graphs_number = await retrieve_graphs_number()
    except:
        raise HTTPException(status_code=502, detail="Bad Gateway: Upstream server error")
    metrics = 'jena-dataset-graphs-number{dataset="slice"} ' + str(graphs_number)
    return PlainTextResponse(metrics)


async def retrieve_graphs_number() -> int:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            settings.url,
            data=urlencode(
                {"query": settings.query},
                quote_via=quote,
            ),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    graphs_number = int(r.json()["results"]["bindings"][0]["numGraphs"]["value"])
    return graphs_number