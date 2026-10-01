# Imagen para los registros que construyen y prueban el servidor (Glama): stdio, sin red al arrancar.
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml LICENSE catalog.json llms.txt ./
COPY datos/municipios.csv datos/
COPY guides/servidor-mcp.md guides/
COPY scripts/ scripts/
RUN pip install --no-cache-dir . && rm -rf build
ENV CATALOGO_DIR=/app
USER nobody
CMD ["mcp-catalogo"]
