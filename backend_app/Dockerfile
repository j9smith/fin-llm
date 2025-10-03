FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/backend_app
CMD ["uvicorn", "backend_app.app:app", "--host", "0.0.0.0", "--port", "8000"]
