# Jena Fuseki Exporter

## Overview

The application exports information about the number of graphs from Apache Jena Fuseki to Prometheus. It was created forfor performance monitoring of the database.

```mermaid
sequenceDiagram
    actor User
    participant Grafana
    participant Prometheus
    participant Jena Fuseki Exporter
    participant Jena Fuseki Exporter
    loop Every 10 minutes
        Prometheus->>+Jena Fuseki Exporter: GET /metrics
        Jena Fuseki Exporter->>+Jena Fuseki: SPARQL query
        Jena Fuseki-->>-Jena Fuseki Exporter: Graphs count
        Jena Fuseki Exporter-->>-Prometheus: Graphs count
        Prometheus->>Prometheus: Save
    end
    User->>+Grafana: Show dashboard
    Grafana->>+Prometheus: PromQL query
    Prometheus-->>-Grafana: Graphs count timeseries
    Grafana-->>-User: Dashboard
```

## Development
How to start locally
1. `ray sync`
1. `. .venv/bin/activate`
1. `fastapi dev src/jena_fuseki_exporter/main.py`

The repo contains a GitHub action. It builds and publishes a container image, and publishes a Helm chart. To trigger it, set a Git tag.
