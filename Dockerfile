# Imagen para los registros que construyen y prueban el servidor (Glama): stdio, sin red al arrancar.
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml LICENSE catalog.json llms.txt ./
COPY datos/municipios.csv datos/
COPY guides/servidor-mcp.md guides/
COPY scripts/ scripts/
RUN pip install --no-cache-dir . && rm -rf build
# nobody no tiene HOME (/nonexistent): la caché de certificados FNMT, SEPE y municipios va a /tmp
ENV CATALOGO_DIR=/app FUENTES_PUBLICAS_CACHE=/tmp/fuentes-publicas XDG_CACHE_HOME=/tmp/.cache
USER nobody
CMD ["mcp-catalogo"]
