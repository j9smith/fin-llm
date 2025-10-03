FROM python:3.12-slim AS build
WORKDIR /app

ENV PIP_NO_CACHE_DIR=1

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt \
    && rm -rf /root/.cache

COPY . /app/backend_app

FROM python:3.12-slim AS runtime
WORKDIR /app

COPY --from=build /wheels /wheels
RUN pip install /wheels/* \
    && rm -rf /root/.cache

COPY --from=build /app/backend_app ./backend_app

CMD ["uvicorn", "backend_app.app:app", "--host", "0.0.0.0", "--port", "8000"]
