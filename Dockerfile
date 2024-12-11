FROM python:slim
WORKDIR /app
COPY requirements.lock src/ ./
RUN pip install uv &&\
    uv pip install --no-cache --system -r requirements.lock
CMD ["fastapi", "run", "jena_fuseki_exporter/main.py", "--port", "80"]