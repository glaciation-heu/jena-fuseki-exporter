from urllib.parse import urlencode, quote

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse


URL = "http://jena-fuseki.integration/slice/"
QUERY = """SELECT (COUNT(DISTINCT ?g) AS ?numGraphs)
WHERE {
  GRAPH ?g {
    # Optional condition: ?s ?p ?o .
  }
}"""


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
            URL,
            data=urlencode(
                {"query": QUERY},
                quote_via=quote,
            ),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    graphs_number = int(r.json()["results"]["bindings"][0]["numGraphs"]["value"])
    return graphs_number